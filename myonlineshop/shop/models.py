from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Pants', 'Pants'),
        ('Jacket', 'Jacket'),
        ('Sweatshirts & Hoodies', 'Sweatshirts & Hoodies'),
        ('Shoes', 'Shoes'),
        ('Polo', 'Polo'),
        ('T-Shirt', 'T-Shirt'),
        ('Denim', 'Denim'),
        ('Shorts', 'Shorts')
        # Add more categories as needed
    ]

    SIZE_CHOICES = [
        ('KIDS', 'Kids'),
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        # Add more sizes as needed
    ]
    AUCTION_TYPE_CHOICES = [
        ('sell', 'Sell'),
        ('auction', 'Auction'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    outseam = models.CharField(max_length=10, blank=True, null=True)
    inseam = models.CharField(max_length=10, blank=True, null=True)
    waist = models.CharField(max_length=10, blank=True, null=True)
    bottom = models.CharField(max_length=10, blank=True, null=True)
    chest = models.CharField(max_length=10, blank=True, null=True)
    length = models.CharField(max_length=10, blank=True, null=True)
    sleeve = models.CharField(max_length=10, blank=True, null=True)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    auction_type = models.CharField(
        max_length=10,
        choices=AUCTION_TYPE_CHOICES,
        default='sell',
    )

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
class CustomUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_pics/')

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def total_price(self):
        return self.quantity * self.product.price

class Auction(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True)
    auction_type = models.CharField(max_length=10, choices=[('sell', 'Sell'), ('auction', 'Auction')])

    def __str__(self):
        return f"Auction for {self.product.name}"

class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of ${self.bid_amount} by {self.user.username}"

# Create your models here.
