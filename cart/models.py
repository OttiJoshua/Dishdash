from django.db import models
import uuid
from core.models import Fooditem  
from core.models import Customer  



class Cart(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Cart {self.id} by {self.customer.firstname}'

    

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.fooditem.name}'

    def get_price(self):
        return self.quantity * self.fooditem.price




class Order(models.Model):
    orderstatus = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Shipping', 'Shipping'),
        ('Cancelled', 'Cancelled'),
    ]
    paymentmode = [
        ('POD', 'POD'),
        ('Paystack', 'Paystack'),
    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200, null=False)
    lname = models.CharField(max_length=200, null=False)
    order_email = models.EmailField(max_length=200, null=False)
    order_number = models.CharField(max_length=40, null=False)
    order_address = models.TextField(max_length=800, null=False)
    state = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    order_total = models.IntegerField(null=False)
    payment_mode = models.CharField(max_length=250, choices=paymentmode, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    order_status = models.CharField(max_length=200, choices=orderstatus, default= 'Pending' )
    tracking_number = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} with {self.tracking_number}'

    

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.quantity} x {self.fooditem.name}'

    def get_price(self):
        return self.quantity * self.fooditem.price


