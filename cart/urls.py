from django.urls import path
from . import views

urlpatterns= [
    path('', views.cart, name="cart"),
    path('cart_add/<uuid:fooditem_id>/', views.cart_add, name="cart_add"),
    path('cart_delete/<int:cartitem_id>/', views.cart_delete, name="cart_delete"),
    path('cart_update/<int:cartitem_id>/<int:quantity>/', views.cart_update, name="cart_update"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/', views.payment, name="payment"),
    path('placeorder/', views.placeorder, name="placeorder"),
]