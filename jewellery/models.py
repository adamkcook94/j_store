from django.db import models

# Create your models here.


class Item_Cat(models.Model):

    class Meta:
        verbose_name_plural = 'Item_Cats'
       
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Item(models.Model):
    Item_Cat = models.ForeignKey(
        'Item_Cat', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=254, null=True, blank=True)
    metal = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=1000)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
