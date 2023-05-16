from django.contrib import admin
from aouth_app.models import UserDetails

# Register your models here.

@admin.register(UserDetails)
class AdminUserDetail(admin.ModelAdmin):
    list_display = ['id','f_name','l_name','email_id','phone_number','address','created_date']




