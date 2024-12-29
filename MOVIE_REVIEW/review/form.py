from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields= '_all_'

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields= 'rating, comment'