from django.shortcuts import render, get_object_or_404
from .models import Item

# Create your views here.


def all_items(request):

    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'items/items.html', context)


def items_description(request, item_id):

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    return render(request, 'items/item_description.html', context)
