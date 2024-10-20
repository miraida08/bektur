from django_filters import FilterSet
from .models import Product
class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'active': ['exact'],
            'price': ['gt', 'lt'],



        }






