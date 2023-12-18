from .models import Category



def menu_links(request):  #this function will fetch all the categoris from database
    links = Category.objects.all()
    return dict(links=links)