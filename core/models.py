from django.db import models
from datetime import datetime

class Customer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=200) 
    address = models.TextField(max_length=200, blank=False)
    password = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=55)
    image1 = models.ImageField(upload_to='category_images/')
    image2 = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name
    
class Fooditem(models.Model):
    name = models.CharField(max_length=200)
    intro = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fooditem_images/')
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    likes = models.ManyToManyField(Customer, related_name='liked_items', blank=True)
    new = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)
     
    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    fooditem = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.customer.firstname}'
    
    @property
    def order_address(self):
        return self.customer.address

    @property
    def order_phone_number(self):
        return self.customer.phone_number