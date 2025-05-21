from django import forms
from .models import FoodItem

class DonorForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'quantity', 'expiry_date', 'image']
        widgets = {
            'expiry_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        } 