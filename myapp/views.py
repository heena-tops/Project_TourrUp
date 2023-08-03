from django.shortcuts import render,redirect
from .models import User,Package,Inq,Image,Cart
from django.conf import settings
from django.core.mail import send_mail
import random
import razorpay

# Create your views here.

def index(request):
	package=Package.objects.all()
	return render(request,'index.html',{'package':package})

def about(request):
	return render(request,'about.html')

def contact(request):
	return render(request,'contact.html')

def elements(request):
	return render(request,'elements.html')

def all_packages(request):
	package=Package.objects.all()
	return render(request,'all_packages.html',{'package':package})

def signup(request):

	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",user)
			msg1="Email Already Exist !!!"
			return render(request,'signup.html',{'msg1':msg1})

		except:
			if request.POST['pswd']==request.POST['cpswd']:
				User.objects.create(
				usertype=request.POST['usertype'],
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				pswd=request.POST['pswd'],
				dob=request.POST['dob'],
				age=request.POST['age'],
				gender=request.POST['gender'],
				address=request.POST['address'],
				)
				msg="Registration done ....."
				return render(request,'login.html',{'msg':msg})
			else:
				msg1="Password and Confirm Password Doesn't Matched !!!!"
				return render(request,'signup.html',{'msg1':msg1})
	else:
		return render(request,'signup.html')


def login(request):

	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],pswd=request.POST['pswd'])
			request.session['fname']=user.fname
			request.session['email']=user.email
			request.session['usertype']=user.usertype

			if user.usertype=="customer":
				return render(request,'index.html')
			else:
				return render(request,'seller_index.html')
		except:
			msg1="Username or Password is incorrect !!!"
			return render(request,'login.html',{'msg1':msg1})

	else:
		return render(request,'login.html')

def logout(request):
	del request.session['email']
	del request.session['fname']
	return redirect('login')

def fpswd(request):
	if request.method=="POST":
		try:

			user=User.objects.get(email=request.POST['email'])

			subject = 'Forgot Password OTP'
			otp=random.randint(1000,9999)
			message = f'Hi {user.fname}, thank you for registering in Myapp. Yor OTP is : {otp}'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )

			return render(request,'verify_otp.html',{'email':user.email,'otp':str(otp)})

		except:
			msg1="You are Not a registered User !!!"
			return render(request,'fpswd.html',{'msg1':msg1})
	else:
		return render(request,'fpswd.html')

def verify_otp(request):
	if request.method=="POST":
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>Type : ",otp)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>Type : ",uotp)

		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>Type : ",type(otp))
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>Type : ",type(uotp))

		if uotp==otp:
			return render(request,'set_pswd.html',{'email':email})
		else:
			msg1="OTP Doesn't Matched !!!"
			return render(request,'verify_otp.html',{'msg1':msg1})
	else:
		return render(request,'verify_otp.html')

def set_pswd(request):
	if request.method=="POST":

		email=request.POST['email']
		npswd=request.POST['npswd']
		cnpswd=request.POST['cnpswd']

		if npswd==cnpswd:
			user=User.objects.get(email=email)
			user.pswd=npswd
			user.save()
			return redirect('login')
		else:
			msg1="New Password and Confirm New Password Doesn't Matched !!!!"
			return render(request,'set_pswd.html',{'msg1':msg1})

	else:
		return render(request,'set_pswd.html')

def seller_index(request):
	try:
		seller=User.objects.get(email=request.session['email'])
		packages=Package.objects.filter(user=seller)
		return render(request,'seller_index.html',{'package':packages})

	except:	
		return render(request,'seller_index.html')

def change_pswd(request):
	if request.method=="POST":
		
		seller=User.objects.get(email=request.session['email'])

		opswd=request.POST['opswd']
		npswd=request.POST['npswd']
		cnpswd=request.POST['cnpswd']

		if opswd==seller.pswd:
			if npswd==cnpswd:
				seller.pswd=npswd
				seller.save()
				return redirect('login')
			else:
				msg1="New Password and Confirm Password Not Matched !!!"
				return render(request,'change_pswd.html',{'msg1':msg1})
		else:
			msg1="Old Password Not Matched !!!"
			return render(request,'change_pswd.html',{'msg1':msg1})

	else:
		return render(request,'change_pswd.html')

def our_services(request):
	seller=User.objects.get(email=request.session['email'])
	print(">>>>>>>>>>>>>>>>By GET METHOD  : ",seller)
	package=Package.objects.filter(user=seller)
	print(">>>>>>>>>>>>>>>>>>>>>>By FILTER METHOD : ",package)
	return render(request,'our_services.html',{'package':package})

def about_seller(request):
	return render(request,'about_seller.html')

def add_packages(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])

		Package.objects.create(
			user=User.objects.get(email=user.email),
			pname=request.POST['pname'],
			destination=request.POST['destination'],
			pimage=request.FILES['package_image'],
			price=request.POST['price'],
			start_date=request.POST['date'],
			t_option=request.POST['transport'],
			other_services=[request.POST.get('food'),request.POST.get('rooms'),request.POST.get('accomodation'),request.POST.get('guide')],
			duration=request.POST['duration'],
			description=request.POST['package_description']
			)
		msg1="Package Added.............."
		return render(request,'add_packages.html',{'msg':msg1})

	else:
		return render(request,'add_packages.html')


def package_details(request,pk):
	seller=User.objects.get(email=request.session['email'])
	package=Package.objects.get(pk=pk,user=seller)
	return render(request,'package_details.html',{'package':package})

def update_package(request,pk):
	seller=User.objects.get(email=request.session['email'])
	package=Package.objects.get(pk=pk,user=seller)

	if request.method=="POST":
		package.user=seller
		package.pname=request.POST['pname']
		package.destination=request.POST['destination']
		package.pimage=request.FILES['package_image']
		package.price=request.POST['price']
		package.start_date=request.POST['date']
		package.t_option=request.POST['transport']
		package.other_services=[request.POST.get('food'),request.POST.get('rooms'),request.POST.get('accomodation'),request.POST.get('guide')]
		package.duration=request.POST['duration']
		package.description=request.POST['package_description']
		package.save()
		return render(request,'package_details.html',{'package':package})
	else:
		return render(request,'update_package.html',{'package':package})

def delete_package(request,pk):
	seller=User.objects.get(email=request.session['email'])
	package=Package.objects.get(pk=pk,user=seller)

	package.delete()

	return redirect('our_services')

def customer_inq(request):
	inq=Inq.objects.all()
	return render(request,'customer_inq.html',{'inq':inq})

def more_images(request,pk):
	package=Package.objects.get(pk=pk)

	if request.method=="POST":
		Image.objects.create(
			package=package,
			img1=request.FILES['img1'],
			img2=request.FILES['img2'],
			img3=request.FILES['img3'],
			img4=request.FILES['img4'],
			img5=request.FILES['img5'],
			img6=request.FILES['img6'],
			)
		return render(request,'seller_index.html')

	else:
		return render(request,'more_images.html',{'package':package})


#=================Customer Side====================================


def about_package(request,pk):
	package=Package.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		cart=Cart.objects.get(user=user,package=package,cart_status=True)
		image=Image.objects.get(package=package)
		return render(request,'about_package.html',{'package':package,'image':image,'cart':cart})
	except:
		pass
	try:
		image=Image.objects.get(package=package)
		return render(request,'about_package.html',{'package':package,'image':image})
	except:
		pass
	try:
		cart=Cart.objects.get(user=user,package=package)
		return render(request,'about_package.html',{'package':package,'cart':cart})	
	except:
		pass
	return render(request,'about_package.html',{'package':package})


def send_inquery(request,pk):
	
	if request.method=="POST":

		package=Package.objects.get(pk=pk)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",package)

		inq=Inq.objects.create(
			customer=User.objects.get(email=request.session['email']),
			package=package,
			fname=request.POST['fname'],
			lname=request.POST['lname'],
			email=request.POST['email'],
			contact=request.POST['contact'],
			message=request.POST['msg'],
			)

		return redirect('seller_index')

	else:
		return render(request,'about_package.html')

def my_packages(request):
	user=User.objects.get(email=request.session['email'])
	try:
		cart=Cart.objects.filter(user=user,payment_status=False)
		r_pay=0
		net_price=0
		cart_count=0
		for i in cart:
			cart_count+=1
			net_price+=i.package.price

		client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
		payment = client.order.create({ "amount": net_price*100, "currency": "INR", "receipt": "order_rcptid_11" })
		r_pay=net_price*100
		return render(request,'my_packages.html',{'cart':cart,'net_price':net_price,'r_pay':r_pay})
	except:
		return render(request,'my_packages.html')



def add_to_my_packages(request,pk):
	user=User.objects.get(email=request.session['email'])	
	package=Package.objects.get(pk=pk)

	if request.method=="POST":
		cart=Cart.objects.create(
			user=user,
			package=package,
			total_amount=package.price,
			payment_status=False,
			cart_status=True,
			)
		return redirect('my_packages')
	else:
		return redirect('index')

def remove_from_my_packages(request,pk):
	user=User.objects.get(email=request.session['email'])
	package=Package.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,package=package)
	cart.delete()
	return redirect('my_packages')

def success(request):
	order_id=request.GET.get('order_id')
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,cart_status=True)
	for i in cart:
		i.payment_status=True
		i.cart_status=False
		i.save()
		i.delete()
		
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",cart)
	return render(request,'success.html')


# to create data in database in django

# .create() : to create new record in table 
#Syntax : modelname.objects.create()

#to retrive data from database

# .get() : to retrive data from data table  (It will return single object)
# Syntax : modelname.objects.get() 

# .filter() : to retrive dataset from data table  (It will return Queryset (multiple objects))
# Syntax : modelname.objects.filter()

# .all() : to fetch all the objects from data table w/o any condition
# Syntax : modelname.objects.all()