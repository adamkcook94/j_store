from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Item, Item_Cat

# Create your views here.


def all_items(request):

    items = Item.objects.all()
    query = None
    item_cats = None

    if request.GET:
        if 'item_cat' in request.GET:
            item_cats = request.GET['item_cat'].split(',')
            items = items.filter(Item_Cat__name__in=item_cats)
            item_cats = Item_Cat.objects.filter(name__in=item_cats)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('items'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            items = items.filter(queries)

    context = {
        'items': items,
        'search_term': query,
        'current_cat': item_cats,
    }

    return render(request, 'items/items.html', context)


def items_description(request, item_id):

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    return render(request, 'items/item_description.html', context)
