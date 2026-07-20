from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'price',
            'stock_quantity',
        ]

class RestockForm(forms.Form):
     quantity_received = forms.IntegerField(
        min_value=1,
        label="Quantity Received"
    )
     
class SoldForm(forms.Form):
    sold_quantity = forms.IntegerField(
        min_value=1,
        label="Sold Quantity"
    )


