from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('about/', views.about, name='about'),
    
    # Корзина
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # Заказы
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    # Успешное оформление заказа
    path('checkout/success/<int:order_id>/', views.checkout_success, name='checkout_success'),

    # Редактирование профиля
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]