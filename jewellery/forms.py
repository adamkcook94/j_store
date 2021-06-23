from django import forms
from .widgets import CustomClearableFileInput
from .models import Item, Item_Cat


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'
    
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item_cats = Item_Cat.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in item_cats]

        self.fields['Item_Cat'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
