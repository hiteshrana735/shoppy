from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index, name="home"),
    path('signup', views.signup , name='signup'),
    path('login/', views.login , name='login'),
    path('logout', views.logout, name="logout"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]
