from django.shortcuts import render
from .models import Item

# Create your views here.
def shop_list(request):
    items = Item.objects.all()
    return render(request, 'shop/shop_index.html', {'items': items})
