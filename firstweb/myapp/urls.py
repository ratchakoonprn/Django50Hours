# myapp/urls.py
from django.urls import path, include
from  .views import *

urlpatterns = [
	path('', Home, name = 'home-page'),
	path('about/', About, name = 'about-page'),
	path('contact/', Contact, name = 'contact-page'),
	path('scrapy/', Scrapy, name = 'scrapy-page'),
	path('addproduct/', AddProduct, name = 'addproduct-page'),
	path('allproducts/', Product, name = 'allproducts-page'),
]
