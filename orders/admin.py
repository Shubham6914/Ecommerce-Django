from django.contrib import admin
from .models import Payment,Order,OrderProduct



class OrderProducInline(admin.TabularInline):
   readonly_fields = ['payment','user','product','quantity','product_price','ordered']
   model= OrderProduct
   extra=0
class OrderAdmin(admin.ModelAdmin):
   list_display=['order_number','full_name','phone_number','email','full_address',
                 'country','state','order_total','tax','status','is_ordered','ip','created_at',]
   list_filter = ['status','is_ordered']
   search_fields = ['order_number','first_name','last_name','phone_number','email']
   list_per_page = 20
   inlines = [OrderProducInline]
   

# class OrderProduct(admin.ModelAdmin):
#    list_display=['order','user','product','variation','color','size',
#                  'quantity','product_price','ordered','created_at','updated_at']


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)