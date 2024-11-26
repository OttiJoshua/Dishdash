from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
import uuid


class CustomerManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, phone_number, password=None):
        if not email:
            raise ValueError('The Email field is required')
      
        
        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, phone_number, email, password=None):
        if not email:
            raise ValueError('The Email field is required')

        user = self.create_user(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=200, unique=True) 
    address = models.TextField(max_length=500, blank=False)
    password = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    objects = CustomerManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone_number']

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    name = models.CharField(max_length=200)
    sub_description = models.TextField(max_length=800)
    description = models.TextField(max_length=800)
    image1 = models.ImageField(upload_to='category_images/')
    image2 = models.ImageField(upload_to='category_images/')
    image3 = models.ImageField(upload_to='category_images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('category', args=[str(self.id)])

    def __str__(self):
        return self.name
    
class Fooditem(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    name = models.CharField(max_length=200)
    intro = models.TextField(max_length=400)
    description = models.TextField(max_length=800)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fooditem_images/')
    price = models.IntegerField()
    option1 = models.CharField(max_length=200, null=True, blank=True)
    option2 = models.CharField(max_length=200, null=True, blank=True)
    option3 = models.CharField(max_length=200, null=True, blank=True)
    option4 = models.CharField(max_length=200, null=True, blank=True)
    option5 = models.CharField(max_length=200, null=True, blank=True)
    option6 = models.CharField(max_length=200, null=True, blank=True)
    off_price = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    likes = models.ManyToManyField(Customer, related_name='liked_items', blank=True)
    new = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)

    def get_options(self):
        return [self.option1, self.option2, self.option3, self.option4, self.option5, self.option6]  
       
    def __str__(self):
        return self.name


class Review(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    fooditem = models.ForeignKey(Fooditem,on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    rating = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Review by {self.customer.firstname} for {self.fooditem.name}'
    

