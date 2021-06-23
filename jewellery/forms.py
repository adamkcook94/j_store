from django import forms
from .models import Item, Item_Cat


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item_cats = Item_Cat.objects.all()
        friendly_names = [(ic.id, ic.get_friendly_name()) for ic in item_cats]

        self.fields['Item_Cat'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
