from django import forms
from .models import Product, CustomUser, ProductImage, AuctionBid
from django.contrib.auth.forms import UserCreationForm

class AuctionBidForm(forms.ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['bid_amount']
class ProductForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False)
    auction_type = forms.ChoiceField(choices=Product.AUCTION_TYPE_CHOICES)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags and not tags.startswith('#'):
            raise forms.ValidationError('Tags must start with "#"')
        return tags

    class Meta:
        model = Product
        fields = ['name', 'description', 'start_bid', 'price','category', 'size', 'image',
                  'outseam', 'inseam', 'waist', 'bottom', 'chest', 'length', 'sleeve', 'auction_type']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'profile_picture')

