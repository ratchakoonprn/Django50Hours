#myapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.staticfiles import storage
from .models import Allproduct, Profile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
	if request.user.profile.usertype != 'admin': #หาก user ไม่ใช่ admin
		return redirect('home-page') #กลับไปยังหน้า home

	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy() #ดึงข้อมูลจากหน้า addproduct.html
		name = data.get('name') # name เป็นชื่อที่ตั้งในส่วนของ attribute name ใน html
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity') #quantity คือ Participants Avaliable
		unit = data.get('unit')

		new = Allproduct() # สร้าง database
		new.name = name # database ที่มี field ที่ชื่อว่า name ให้มีค่าเท่ากับ ค่า name ที่ดึงมาจาก html
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		################# Save Image #################
		file_image = request.FILES['imageupload'] #ไฟล์ที่ส่งมาเก็บการ request นั่นคือไฟล์ที่เรา upload
		file_image_name = request.FILES['imageupload'].name.replace(' ','') #ชื่อไฟล์ที่เราสั่ง upload ขึ้นมา ทั้งนี้ชื่อไฟล์อาจมีปัญหาได้หากมี space ดังนั้นเราจึง replace ด้วย ''
		print('FILE_IMAGE: ',file_image)
		print('IMAGE_NAME: ',file_image_name)
		fs = FileSystemStorage() #ดึงคลาสของ FileSystemStorage
		filename = fs.save(file_image_name,file_image)#สร้างตัวแปร filename เพื่อทำการบันทึกชื่อไฟล์และรูปภาพ
		upload_file_url = fs.url(filename)#ชื่อไฟล์ URL ว่าอะไร
		new.image = upload_file_url[6:]#เลข 6 คือการ slice string ของ url
		#ถ้า file = 'media/durian.jpg'
		#แล้ว file [6:] มันจะมีค่าเป็น durian.jpg (เอา index ตั้งแต่ 6 ขึ้นมาแสดง)
		#ทั้งนี้เพราะคำว่า media/ มี index ตั้งแต่ 0 - 5
		##############################################
		new.save()

	return render(request,'myapp/addproduct.html')

def Product(request):
	#product = Allproduct.objects.all() #ดึงข้อมูลทั้งหมดมาจากฐานข้อมูลชื่อ AllProduct
	#product = product.order_by('name')
	#product = Allproduct.objects.all().order_by('id').reverse()
	product = Allproduct.objects.all().order_by('name')
	context = {'product':product} #โยนข้อมูลที่เราถึงมาจากบรรทัดข้างบนเพื่อแนบไปกับ context
	return render(request,'myapp/allproducts.html',context)

def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name') 
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username = email #ให้ usename ใช้ email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		user = authenticate(username=email, password=password)
		login(request,user)

	return render(request,'myapp/register.html')