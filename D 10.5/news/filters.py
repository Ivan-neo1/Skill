
from django.forms import DateInput
from django_filters import FilterSet, DateFilter

from .models import Post



class PostFilter(FilterSet):
    date = DateFilter(field_name='time_in', widget=DateInput(attrs={'type': 'date'}), label='Позже указанной даты',
                      lookup_expr='date__gte')

    class Meta:
        model = Post

        fields = {

            'header': ['icontains'],

            'author': ['exact'],

        }