from django.contrib import admin
from .models import Account,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
   def thumbnail(self,object):
      return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
   thumbnail.short_description = 'profile picture'
   list_display=['thumbnail','user','city','state','country']

admin.site.register(UserProfile,UserProfileAdmin)

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