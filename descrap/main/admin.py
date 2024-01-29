from django.contrib import admin
from .models import Contact
from .models import Document
from .models import Useraddress
from .models import MyUser

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','message']


@admin.register(Document)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','image']

@admin.register(Useraddress)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['username','add']

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','is_staff','is_active','is_admin']

