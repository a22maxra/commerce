from django.forms import ModelForm, Textarea
from django import forms
from .models import Listing, Bid, Comment

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


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('offer',)
        labels = {'offer': ''}
        widgets = { 
            'offer': forms.NumberInput(attrs={'class':'form-control m-1', 'placeholder': '$ Amount', 'min':0})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        labels = {'message': ''}
        widgets = { 
            'message': forms.Textarea(attrs={'rows': 4, 'class':'form-control m-1', 'placeholder': 'Write something...'}),
        }