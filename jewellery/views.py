from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Item, Item_Cat

# Create your views here.


def all_items(request):

    items = Item.objects.all()
    query = None
    item_cats = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                items = items.annotate(lower_name=Lower('name'))
            if sortkey == 'item_cat':
                sortkey = 'item_cat__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            items = items.order_by(sortkey)

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

    current_sorting = f'{sort}_{direction}'

    context = {
        'items': items,
        'search_term': query,
        'current_cat': item_cats,
        'current_sorting': current_sorting,
    }

    return render(request, 'items/items.html', context)


def items_description(request, item_id):

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    return render(request, 'items/item_description.html', context)
