from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer, Category, Fooditem, Review
from cart.models import Order,OrderItem,Cart,CartItem
from django.contrib import messages, auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    categories = Category.objects.all()
    fooditems = Fooditem.objects.filter(Q(new=True) | Q(bestseller=True) | Q(likes=True)).order_by('name')
    paginator = Paginator(fooditems, 8) 
    page_number = request.GET.get("page")
    paged_fooditems = paginator.get_page(page_number)
    context =  {'categories': categories,
                'fooditems':paged_fooditems }
    return render(request, 'core/index.html', context)

def categories(request):
    categories = Category.objects.all().order_by('name')
    context = {'categories':categories}
    return render(request, 'core/categories.html',context)

def category(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    fooditems = Fooditem.objects.filter(category=category).filter(available = True).order_by('name')
    context = {'category':category, 'fooditems':fooditems, 'categories': categories } 
    return render(request, 'core/category.html', context)


@login_required(login_url='login')
def user(request):
    categories = Category.objects.all()
    userinfo = Customer.objects.get(id=request.user.id)
    orders = Order.objects.filter(customer=request.user)


    fooditem = Fooditem.objects.first()
     
    orderdata = []
    for order in orders:
        orderitems = OrderItem.objects.filter(order=order)

        for orderitem in orderitems:
            orderitem.review_exists = Review.objects.filter(customer=request.user, fooditem=orderitem.fooditem).exists()

        orderdata.append({
            'order': order,
            'orderitems': orderitems,
        })
    
    if request.method == 'POST' and request.POST.get('form_type') == 'update_info':
        userinfo.customer = request.user
        userinfo.firstname = request.POST.get('firstname')
        userinfo.lastname = request.POST.get('lastname')
        userinfo.phone_number = request.POST.get('phone_number')
        userinfo.email = request.POST.get('email')
        userinfo.address = request.POST.get('address')
        userinfo.date_of_birth = request.POST.get('date_of_birth')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2:
            if password1 == password2:
                userinfo.set_password(password1)
                userinfo.save()
            else:
                messages.error(request,'Your Password Did Not Match')

        userinfo.save()
        messages.success(request, 'Your information has been updated successfully.')


    context = {
                'userinfo': userinfo, 
                'orders': orders, 
                'fooditem' : fooditem,
                'orderdata': orderdata,
                'categories' : categories
                }

    return render(request, 'core/user.html',context)



@login_required(login_url='login')
def addreview(request, fooditem_id):
    if request.method == 'POST'and request.POST.get('form_type') == 'post_review':
        fooditem_id = request.POST.get('fooditem_id')
        fooditem = Fooditem.objects.get(id=fooditem_id)
        userinfo = Customer.objects.get(id=request.user.id)

        existing_review = Review.objects.filter(customer=userinfo, fooditem=fooditem).exists()
        if existing_review:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        review_text = request.POST.get('comment')
        rating = request.POST.get('rating')

        if not userinfo:
            return redirect(request.META.get('HTTP_REFERER', '/'))


        if review_text and rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    Review.objects.create(
                        customer=userinfo, 
                        fooditem=fooditem,
                        comment=review_text,
                        rating=rating
                    )
                    messages.success(request, 'Your review has been posted successfully.')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    messages.error(request, 'Rating must be between 1 and 5.')
            except ValueError:
                messages.error(request, 'Invalid rating value.')
        else:
            messages.error(request, 'Both comment and rating are required.')




def fooditem(request,fooditem_id):
    fooditem = Fooditem.objects.get(id=fooditem_id)
    reviews = Review.objects.filter(fooditem=fooditem)
    categories = Category.objects.filter(id=fooditem.category_id) 
    context = {'fooditems':fooditem, 'categories':categories, 'reviews': reviews}
    return render(request, 'core/fooditem.html', context)

def like_fooditem(request,fooditem_id):
    if request.method == 'POST':
        if request.user.is_authenticated: 
            customer = request.user  
            fooditem = Fooditem.objects.get(id=fooditem_id)  

            if fooditem.likes.filter(id=customer.id).exists():
                fooditem.likes.remove(customer)
            else:
                fooditem.likes.add(customer)

    return redirect(request.META.get('HTTP_REFERER', '/'))



def search(request):
    categories = Category.objects.all()
    searchquery = Fooditem.objects.order_by('name')
    name = ''
    if 'searchmenu' in request.GET:
        searchmenu = request.GET['searchmenu']
        if searchmenu:
            searchquery = searchquery.filter(name__icontains=searchmenu)

    if 'searchmenu' in request.GET:
        name = request.GET['searchmenu']
        if name:
            searchquery = searchquery.filter(name__icontains=name)

    context = {'fooditems':searchquery, 'name':name, 'categories': categories } 
    return render(request, 'core/search.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        customer = auth.authenticate(email=email, password=password)

        if customer is not None:
            auth.login(request, customer)
            messages.success(request, 'You Are Logged In')
            return redirect('user')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else: 
        messages.error(request, 'UserName Or Password Is Incorrect')
        return render(request, 'core/login.html')

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if Customer.objects.filter(email=email).exists():
                messages.error(request, 'That Email Already Exists')
                return redirect('signup')
            else:
                customer = Customer.objects.create_user(firstname=firstname, lastname=lastname, email=email, phone_number=phone_number,password=password)

                auth.login(request, customer)
                messages.success(request, 'You Are Logged In')
                return redirect('index')

        else:
            messages.error(request, 'Password Do Not Match')
            return redirect('signup')


    else:
        return render(request, 'core/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.error(request, 'You Have Succesfully Logged Out')
        return redirect('index')


