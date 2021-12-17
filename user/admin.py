from django.contrib import admin
from .models import *

# Register your models here.
class UserManager(admin.ModelAdmin):
    list_display = ['id','username','password','created_time','update_time']
    list_display_links = ['id','username']
    list_editable = ['password']
admin.site.register(User,UserManager)