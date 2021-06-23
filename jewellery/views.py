from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, Item_Cat
from django.db.models.functions import Lower
from .forms import ItemForm

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

@login_required
def add_item(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only J Store employees can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Successfully added item.')
            return redirect(reverse('items_description', args=[item.id]))
        else:
            messages.error(request, 'Failed to add itme. Please ensure the form is valid.')
    else:
        form = ItemForm()

    template = 'items/add_item.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_item(request, item_id):
    """ Edit a item in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only J Store employees can do that.')
        return redirect(reverse('home'))
    
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated item')
            return redirect(reverse('items_description', args=[item.id]))
        else:
            messages.error(request, 'Failed to update item. Please ensure the form is valid.')
    else:
        form = ItemForm(instance=item)
        messages.info(request, f'You are editing {item.name}')

    template = 'items/edit_item.html'
    context = {
        'form': form,
        'item': item,
    }

    return render(request, template, context)

@login_required
def delete_item(request, item_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only J Store employees can do that.')
        return redirect(reverse('home'))
    
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Item deleted!')
    return redirect(reverse('all_items'))
