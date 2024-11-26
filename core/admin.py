from django.contrib import admin
from .models import Customer, Category, Fooditem,Review


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','firstname','lastname','phone_number')
    list_display_links = ('id','firstname','lastname')
    search_fields = ('firstname','lastname','address')
    list_per_page = 20

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    list_display_links = ('name','id')
    

class FooditemAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','available','new','bestseller')
    list_display_links = ('name',)
    list_filter = ('category', 'price', 'new', 'available', 'bestseller')
    list_editable = ('new', 'available', 'bestseller')
    search_fields = ('name',)
    list_per_page = 10

    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer','fooditem','date', 'rating',)
    list_display_links = ('customer','fooditem')
    list_filter = ( 'customer','fooditem', 'date', 'rating',)
    list_per_page = 20



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Fooditem, FooditemAdmin)
admin.site.register(Review, ReviewAdmin)