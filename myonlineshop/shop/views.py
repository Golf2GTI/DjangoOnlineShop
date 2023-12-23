from django.views.generic import ListView, DetailView, TemplateView, RedirectView, View
from .models import Product, Cart, CartItem, ProductImage, AuctionBid, Auction
from django.urls import reverse_lazy, reverse
from .forms import ProductForm, CustomUserCreationForm, ProductImageForm, AuctionBidForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
import logging
from django.contrib import messages
logger = logging.getLogger(__name__)


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filter by name or tags
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(tags__icontains=query)
            )

        # Filtering by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)

        # Filter by size
        size = self.request.GET.get('size')
        if size:
            queryset = queryset.filter(size=size)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_items = cart.cartitem_set.annotate(total_price=Sum('quantity'))
        total_quantity = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        context['total_quantity'] = total_quantity
        return context


class ProductDetailView(View):
    template_name = 'shop/product_detail.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        bid_form = AuctionBidForm()

        highest_bid = None
        if product.auction_type == 'auction':
            auction = Auction.objects.get(product=product)
            highest_bid = AuctionBid.objects.filter(auction=auction).order_by('-bid_amount').first()
        return render(request, self.template_name, {
            'product': product,
            'bid_form': bid_form,
            'highest_bid': highest_bid
        })

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        bid_form = AuctionBidForm(request.POST)

        if bid_form.is_valid():
            if product.auction_type == 'auction':
                auction = Auction.objects.get(product=product)
                new_bid = bid_form.save(commit=False)
                new_bid.user = request.user
                new_bid.auction = auction
                new_bid.save()
                return redirect('product_detail', pk=pk)

        return render(request, self.template_name, {
            'product': product,
            'bid_form': bid_form,
        })
@login_required
def product_create(request):
    ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3, max_num=10)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user

            # Handling auction details
            auction_type = product_form.cleaned_data['auction_type']
            if auction_type == 'auction':
                start_bid = product_form.cleaned_data['start_bid']
                product.start_bid = start_bid



            product.save()  # Save the product first

            if auction_type == 'auction':
                # Create an associated Auction object after the product is saved
                auction = Auction.objects.create(product=product, auction_type=auction_type)

            formset.instance = product
            formset.save()

            logger.info(f"Product created: {product.name} (ID: {product.id})")
            return redirect('product_list')
        else:
            logger.error(f"Product creation failed. Form errors: {product_form.errors}, {formset.errors}")
    else:
        product_form = ProductForm()
        formset = ProductImageFormSet()

    product_id = None
    if product_form.instance and product_form.instance.id:
        product_id = product_form.instance.id

    return render(request, 'shop/product_create.html',
                  {'product_form': product_form, 'formset': formset, 'product_id': product_id})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')  # Redirect to your home page
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_items = cart.cartitem_set.annotate(total_price=Sum('quantity'))

        total_quantity = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        context['cart'] = cart
        context['cart_items'] = cart_items
        context['total_quantity'] = total_quantity
        return context

class RemoveFromCartView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(pk=product_id)
        cart = Cart.objects.get(user=self.request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        else:
            cart_item.delete()
        return reverse('cart')

class AddToCartView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        product_id = kwargs['product_id']
        product = Product.objects.get(pk=product_id)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created and product.quantity > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
            return reverse('cart')
        else:
            messages.error(self.request,'There are only {{ product.quantity }} items in stock')
            return reverse('cart')


@login_required
def user_profile(request):
    user_products = Product.objects.filter(user=request.user)
    return render(request, 'shop/user_profile.html', {'user_products': user_products})

def auction_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Assuming there's a foreign key from AuctionBid to Product for bids
    current_bid = AuctionBid.objects.filter(product=product).order_by('-bid_amount').first()
    return render(request, 'auction_detail.html', {'product': product, 'current_bid': current_bid})
# Create your views here.
