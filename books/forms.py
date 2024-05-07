from django import forms
from django.contrib.auth import get_user_model

from .models import Review


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.book = kwargs.pop('book', None)
        super(CreateReviewForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        review = super().save(commit=False)
        review.author = self.user
        review.book = self.book
        if commit:
            review.save()
        return review
