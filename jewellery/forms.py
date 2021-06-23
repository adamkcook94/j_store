from django import forms
from .models import Item, Item_Cat


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Item_Cat.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['item_cat'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'