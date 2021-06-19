from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from jewellery.models import Item
# Create your views here.


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    item = get_object_or_404(Item, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {item.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {item.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    item = get_object_or_404(Item, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {item.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {item.name} from bag.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_item(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    item = get_object_or_404(Item, pk=item_id)
    try:
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'Removed {item.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing {e} from bag')
        return HttpResponse(status=500)
