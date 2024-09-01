from django import forms
from .models import Invoice, Product, UserProfile

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['number', 'date', 'first_name', 'last_name', 'bank_account', 'billing_address', 'company_name']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'count', 'price']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'billing_address', 'bank_account']


ProductFormSet = forms.inlineformset_factory(Invoice, Product, form=ProductForm, extra=2)
