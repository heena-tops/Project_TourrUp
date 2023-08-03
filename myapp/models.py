from django.db import models

# Create your models here.


class User(models.Model):
	usertype=models.CharField(max_length=100,default="customer")
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	pswd=models.CharField(max_length=100)
	dob=models.DateTimeField()
	age=models.IntegerField()
	gender=models.CharField(max_length=100)
	address=models.CharField(max_length=100)

	def __str__(self):
		return self.fname+" - "+self.usertype

class Package(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	pname=models.CharField(max_length=100)
	destination=models.CharField(max_length=100)
	pimage=models.ImageField(blank=True,null=True,upload_to='images/')
	price=models.IntegerField()
	start_date=models.DateTimeField()
	t_option=models.CharField(max_length=100)
	other_services=models.CharField(max_length=100)
	duration=models.CharField(max_length=100)
	description=models.CharField(max_length=900)

	def __str__(self):
		return self.pname+' - '+str(self.price)+" - "+self.user.fname

class Image(models.Model):
	package=models.ForeignKey(Package,on_delete=models.CASCADE)
	img1=models.ImageField(blank=True,null=True,upload_to='images/')
	img2=models.ImageField(blank=True,null=True,upload_to='images/')
	img3=models.ImageField(blank=True,null=True,upload_to='images/')
	img4=models.ImageField(blank=True,null=True,upload_to='images/')
	img5=models.ImageField(blank=True,null=True,upload_to='images/')
	img6=models.ImageField(blank=True,null=True,upload_to='images/')

class Inq(models.Model):
	customer=models.ForeignKey(User,on_delete=models.CASCADE)
	package=models.ForeignKey(Package,on_delete=models.CASCADE)
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	contact=models.IntegerField()
	message=models.CharField(max_length=500)

	def __str__(self):
		return self.package.pname+" - "+self.fname

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	package=models.ForeignKey(Package,on_delete=models.CASCADE)
	total_amount=models.IntegerField()
	payment_status=models.BooleanField(default=False)
	cart_status=models.BooleanField(blank=True,null=True)
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)


	def __str__(self):
		return self.package.pname+" - "+str(self.total_amount)+" - "+self.user.fname


