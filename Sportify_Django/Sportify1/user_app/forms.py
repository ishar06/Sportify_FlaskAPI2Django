from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Address
import re

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be 10 digits.',
                code='invalid_phone'
            )
        ]
    )
    
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            # Check password length
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            
            # Check for uppercase
            if not any(c.isupper() for c in password):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")
            
            # Check for lowercase
            if not any(c.islower() for c in password):
                raise forms.ValidationError("Password must contain at least one lowercase letter.")
            
            # Check for digit
            if not any(c.isdigit() for c in password):
                raise forms.ValidationError("Password must contain at least one number.")
            
            # Check for special character
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise forms.ValidationError("Password must contain at least one special character.")
        
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'house_street', 'landmark', 'pincode', 'state', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'house_street': forms.TextInput(attrs={'class': 'form-control'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
