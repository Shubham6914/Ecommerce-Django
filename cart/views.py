from django.shortcuts import render
from store.models import ReviewRating,Product
# Create your views here.

def home(request):
   products = Product.objects.all().filter(is_available=True).order_by('created_date')
   
   # get the review 
   for product in products:
      reviews = ReviewRating.objects.filter(product_id=product.id,status=True)

   context = {
      'products':products,
      'reviews':reviews,
   }
   return render(request, 'cart/home.html',context)