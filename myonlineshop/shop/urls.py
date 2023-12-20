from django.urls import path
from .views import ProductListView, ProductDetailView, product_create, register, user_login, user_logout, CartView, AddToCartView, RemoveFromCartView, user_profile

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_create/', product_create, name='product_create'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('user_profile/', user_profile, name='profile'),
]