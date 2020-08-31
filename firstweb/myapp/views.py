#myapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.staticfiles import storage
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#HttpResponse คือ ฟังก์ชันสำหรับทำให้แสดงข้อความหน้าเว็บได้

def Lastest(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3] #ดึงข้อมูลเพียง 3 ตัว
	preorder = Allproduct.objects.filter(quantity__lte=0)#กรองข้อมูลที่ค่า quantity <= 0
	context = {'product':product,'preorder':preorder} #โยนข้อมูลที่เราถึงมาจากบรรทัดข้างบนเพื่อแนบไปกับ context
	return render(request,'myapp/lastest.html', context)

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

def AddtoCart(request,pid):
	#localhost:8000/addtocart/3
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		#กรณีที่สินค้ามีซ้ำ
		newcart = Cart.objects.get(user=user, productid=str(pid)) #ตรวจว่าผู้ใช้งานคนนี้เคยสั่งสินค้านี้มาก่อนหรือไม่
		#print('EXISTS: ', pcheck.exists()) #check ว่า รหัสสินค้านี้มีอยู่ใน database หรือเปล่า
		newquan = newcart.quantity + 1 #ถ้า user เคยสั่งซื้อสินค้านี้อยู่ ก็ให้เพิ่มขึ้นอีก 1 รายการ
		newcart.quantity = newquan 
		calculate = newcart.price * newquan
		newcart.total = calculate
		newcart.save()

		#update จำนวนของตระกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user)
		#print('COUNT: ',count) #นับจำนวนรายการที่สั่งซื้อ กรณีที่รายการ 1 มีการสั่งซื้อจำนวนหลายๆ ตัว จะนับเป็น 1 รายการ
		count = sum([c.quantity for c in count]) #นับจำนวนรายการทั้งหมด
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		
		return redirect('allproducts-page')
	except:
		#กรณีที่ไม่มีสินค้าซ้ำ ต้องทำการสร้างสินค้าชิ้นใหม่นี้ขึ้นมา
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		count = Cart.objects.filter(user=user)
		#print('COUNT: ',count) #นับจำนวนรายการที่สั่งซื้อ กรณีที่รายการ 1 มีการสั่งซื้อจำนวนหลายๆ ตัว จะนับเป็น 1 รายการ
		count = sum([c.quantity for c in count]) #นับจำนวนรายการทั้งหมด
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('allproducts-page')

def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)
	
	context = {}

	if request.method == 'POST':
		#ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')

		item = Cart.objects.get(user=user, productid=productid)
		item.delete()
		context['status'] = 'delete'

		#รวมจำนวนสินค้าและราคาสินค้าาทั้งหมด
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count]) #นับจำนวนรายการทั้งหมด
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('allproducts-page')


	mycart = Cart.objects.filter(user = user)
	count = sum([c.quantity for c in mycart]) #รวมจำนวนสินค้า
	total = sum([c.total for c in mycart]) #รวมราคา

	context['mycart'] = mycart #โยนข้อมูลที่เราถึงมาจากบรรทัดข้างบนเพื่อแนบไปกับ context
	context['count'] = count
	context['total'] = total

	return render(request,'myapp/mycart.html',context)

def MyCartEdit(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	if request.method == 'POST':
		data = request.POST.copy()

		if data.get('clear') == 'clear':
			Cart.objects.filter(user=user).delete() #ลบรายการในตะกร้าสินค้าทั้งหมด
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0 #กำหนดให้ตัวเลขบน nav bar มีค่าเป็น 0
			updatequan.save()
			return redirect('mycart-page')

		editlist = []

		for k,v in data.items(): #k -> key, v-> value
			if k[:2] == 'pd': #if k < 2
				pid = int(k.split('_')[1]) #ตัดคำ index 1
				dt = [pid,int(v)]
				editlist.append(dt)

		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0], user=user) #productid
			edit.quantity = ed[1] #quantity
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()
		
		#update quantity on  nav bar
		count = Cart.objects.filter(user=user)
		#print('COUNT: ',count) #นับจำนวนรายการที่สั่งซื้อ กรณีที่รายการ 1 มีการสั่งซื้อจำนวนหลายๆ ตัว จะนับเป็น 1 รายการ
		count = sum([c.quantity for c in count]) #นับจำนวนรายการทั้งหมด
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycart-page')

	if request.method == 'POST':
		#ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')

		item = Cart.objects.get(user=user, productid=productid)
		item.delete()
		context['status'] = 'delete'

		#update ตัวเลขหลัง Order หลังจากที่ทำการลบข้อมูลออกจากตะกร้าสินค้า
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count]) #นับจำนวนรายการทั้งหมด
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycartedit-page')


	mycart = Cart.objects.filter(user = user)
	context['mycart'] = mycart #โยนข้อมูลที่เราถึงมาจากบรรทัดข้างบนเพื่อแนบไปกับ context

	return render(request,'myapp/mycartedit.html',context)

def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')

		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['adderss'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user = user)
			count = sum([c.quantity for c in mycart]) #รวมจำนวนสินค้า
			total = sum([c.total for c in mycart]) #รวมราคา

			context['mycart'] = mycart #โยนข้อมูลที่เราถึงมาจากบรรทัดข้างบนเพื่อแนบไปกับ context
			context['count'] = count
			context['total'] = total

			return render(request,'myapp/checkout2.html',context)

		

		if page == 'confirm':
			print('Confirm')
			# generate order number and save to Order Models 
			# save product in cart to OrderProduct models
			# clear cart
			# redirect to order list page


	return render(request,'myapp/checkout1.html')
