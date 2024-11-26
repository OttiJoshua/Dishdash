from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer','status')
    list_display_links = ('customer',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','fooditem','quantity')
    list_display_links = ('cart','fooditem')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','order_status','tracking_number')
    list_display_links = ('customer',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','fooditem','quantity')
    list_display_links = ('order','fooditem')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
