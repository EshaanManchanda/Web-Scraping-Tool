from django import forms

class ScrapeForm(forms.Form):
    url = forms.URLField(label='URL', max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}))
    item_selector = forms.CharField(label='Item Selector', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title_selector = forms.CharField(label='Title Selector', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price_selector = forms.CharField(label='Price Selector', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
