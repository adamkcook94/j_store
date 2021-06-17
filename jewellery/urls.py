from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_items, name='all_items'),
    path('<item_id>', views.items_description, name='items_description'),
]
