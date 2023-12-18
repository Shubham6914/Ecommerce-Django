from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.

''' this class is used to make password fiel read only and also used to diplay fields
in table format in admin panel '''
class AccountAdmin(UserAdmin):
   list_display = ('email','first_name','last_name','username',
                   'last_login','date_joined','is_active','is_staff')
   
   list_display_links = ('email','first_name','last_name')
   readonly_fields = ('last_login','date_joined')
   ordering = ('-date_joined',)
   filter_horizontal = ()
   list_filter =()
   fieldsets = ()

admin.site.register(Account,AccountAdmin) #this is for registering the model in admin panel 