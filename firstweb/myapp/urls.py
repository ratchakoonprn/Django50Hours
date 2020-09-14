# myapp/urls.py
from django.urls import path, include
from  .views import *

urlpatterns = [
	path('', Home, name = 'home-page'),
	path('lastest/', Lastest, name = 'lastest-page'),
	path('about/', About, name = 'about-page'),
	path('contact/', Contact, name = 'contact-page'),
	path('scrapy/', Scrapy, name = 'scrapy-page'),
	path('addproduct/', AddProduct, name = 'addproduct-page'),
	path('allproducts/', Product, name = 'allproducts-page'),
	path('register/', Register, name = 'register-page'),
	path('addtocart/<int:pid>', AddtoCart, name = 'addtocart-page'),
	path('mycart/', MyCart, name = 'mycart-page'),
	path('mycart/edit/', MyCartEdit, name = 'mycartedit-page'),
	path('checkout/', Checkout, name = 'checkout-page'),
	path('orderlist/', OrderListPage, name = 'orderlist-page'),
	path('allorderlist/', AllOrderListPage, name = 'allorderlist-page'),
	path('uploadslip/<str:orderid>', UploadSlip, name = 'uploadslip-page'),
]
