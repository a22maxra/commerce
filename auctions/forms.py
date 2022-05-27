from django.forms import ModelForm, Textarea
from django import forms
from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = (
            'title',
            'description',
            'category',
            'image',
            'start'
        )
        labels = {
            'title': '',
            'description': '',
            'category': '',
            'image': '',
            'start': ''
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control m-1', 'placeholder': 'Title'}),
            'description': Textarea(attrs={'class':'form-control m-1', 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class':'form-control m-1', 'placeholder': 'Category'}),
            'image': forms.TextInput(attrs={'class':'form-control m-1', 'placeholder': 'Image'}),
            'start': forms.NumberInput(attrs={'class':'form-control m-1', 'placeholder': '$ Starting Price'})
        }