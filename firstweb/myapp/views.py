#myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles import storage
from .models import Allproduct
#HttpResponse คือ ฟังก์ชันสำหรับทำให้แสดงข้อความหน้าเว็บได้

def Home(request):
	#return HttpResponse('สวัสดี<h1> Hello world</h1><h3>สบายดีไหม</h3>')
	#return render(request,'myapp/home.html')
	product1 = 'Data Mining Libraries'
	product2 = 'Data Processing and Modeling Libraries'
	product3 = 'Data Visualization Libraries'

	context = {'product1':product1,'product2':product2,'product3':product3}
	return render(request,'myapp/home.html', context)

def About(request):
	return render(request,'myapp/about.html')

def Contact(request):
	return render(request,'myapp/contact.html')

def Scrapy(request):
	return render(request,'myapp/scrapy.html')


def AddProduct(request):
	if request.method == 'POST':
		data = request.POST.copy() #ดึงข้อมูลจากหน้า addproduct.html
		name = data.get('name') # name เป็นชื่อที่ตั้งในส่วนของ attribute name ใน html
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')

		new = Allproduct() # สร้าง database
		new.name = name # database ที่มี field ที่ชื่อว่า name ให้มีค่าเท่ากับ ค่า name ที่ดึงมาจาก html
		new.price = price
		new.imageurl = imageurl
		new.save()

	return render(request,'myapp/addproduct.html')

def Product(request):
	#product = Allproduct.objects.all() #ดึงข้อมูลทั้งหมดมาจากฐานข้อมูลชื่อ AllProduct
	#product = product.order_by('name')
	#product = Allproduct.objects.all().order_by('id').reverse()
	product = Allproduct.objects.all().order_by('name')
	context = {'product':product} #โยนข้อมูลที่เราถึงมาจากบรรทัดข้างบนเพื่อแนบไปกับ context
	return render(request,'myapp/allproducts.html',context)
