from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blogs, name='blogs'),
    
    # Address management URLs
    path('addresses/', views.address_list, name='address_list'),
    path('address/add/', views.address_create, name='address_create'),
    path('address/edit/<int:pk>/', views.address_edit, name='address_edit'),
    path('address/delete/<int:pk>/', views.address_delete, name='address_delete'),
    path('address/set-default/<int:pk>/', views.set_default_address, name='set_default_address'),
]
