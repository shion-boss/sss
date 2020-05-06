from django import forms
from .models import user_meta

class user_meta_form(forms.ModelForm):
    class Meta:
        model=user_meta
        fields=['username']

class card_form(forms.Form):
    number=forms.CharField(min_length=16,max_length=20,
        widget=forms.TextInput(attrs={
               'placeholder':'数字のみ入力可能です。',
               'pattern':'^[0-9]+$'}))
    cvc=forms.CharField(max_length=3,widget=forms.TextInput(attrs={
           'pattern':'^[0-9]+$'}))
    exp_month=forms.CharField(max_length=2,widget=forms.TextInput(attrs={
           'pattern':'^[0-9]+$'}))
    exp_year=forms.CharField(max_length=4,widget=forms.TextInput(attrs={
           'pattern':'^[0-9]+$'}))


class meta_form(forms.ModelForm):
    class Meta:
        model=user_meta
        fields=['name','photo','plofile']
