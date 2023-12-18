from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
   prepopulated_fields={'slug':('category_name',)} #this field help detect text from 
   #category_name field to slug field in adminpannel
   list_display =('category_name','slug')

# Register your models here.

admin.site.register(Category,CategoryAdmin) #registering the category model in admin site or panel
