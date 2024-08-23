from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('categories/', views.categories, name="categories"),
    path('category/', views.category, name="category"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
]
# <uuid:cartegory_id>/