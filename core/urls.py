from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name="index"),
    path('categories/', views.categories, name="categories"),
    path('category/<uuid:category_id>/', views.category, name="category"),    
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('user/', views.user, name="user"),
    path('fooditem/<uuid:fooditem_id>/', views.fooditem, name="fooditem"),
    path('addreview/<uuid:fooditem_id>/', views.addreview, name="addreview"),
    path('like_fooditem/<uuid:fooditem_id>/', views.like_fooditem, name='like_fooditem'),
    path('search/', views.search, name="search"),
]
