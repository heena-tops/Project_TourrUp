from django.contrib import admin
from .models import User,Package,Inq,Image,Cart

# Register your models here.

admin.site.register(User)
admin.site.register(Package)
admin.site.register(Inq)
admin.site.register(Image)
admin.site.register(Cart)
