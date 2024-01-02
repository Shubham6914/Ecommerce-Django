from django.contrib import admin
from .models import Product,Variation,ReviewRating,ProductGallery
import admin_thumbnails
# @admin.register(Product) 
@admin_thumbnails.thumbnail('image')
class producGalleryAdmin(admin.TabularInline):
    model=ProductGallery
    extra =1
admin.site.register(ProductGallery)

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display=['product','user','subject','review','rating','ip','status','created_at','updated_at']
admin.site.register(ReviewRating, ReviewRatingAdmin)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields  = {'slug':('product_name',)}
    inlines=[producGalleryAdmin]

admin.site.register(Product,ProductAdmin)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_active','created_date']
    list_editable=('is_active',)
    list_filter=['product','variation_category','variation_value']
    
