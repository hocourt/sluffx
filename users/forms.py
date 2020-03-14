from django                                 import forms
#from django.forms.widgets                   import CheckboxSelectMultiple
#from django.utils                           import timezone
#from django.contrib.auth.models             import User
from .models                                import Person
#from django.contrib.auth.forms              import SetPasswordForm, PasswordChangeForm

class InsertMemberForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name','password', 'cover')

class InsertContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('display_name',)

class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ( 'display_name', 'status', 'authorname', 'cover')

class PasswordForm(forms.Form):
    password = forms.CharField(label='New password', max_length=20)

class DisplaynameForm(forms.Form):
    display_name = forms.CharField(max_length=20)

class UserOptionsForm(forms.ModelForm):
     class Meta:
        model = Person
        fields = ('username',)

class UpdateContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ( 'display_name', 'status', 'authorname')




