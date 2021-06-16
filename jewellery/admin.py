from django.contrib import admin
from .models import Item, Item_Cat

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'metal',
        'brand',
        'price',
        'description',
        'image',
    )

class Item_CatAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Item, ItemAdmin)  
admin.site.register(Item_Cat, Item_CatAdmin)
