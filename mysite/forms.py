from django                                 import forms
from .models                                import Site, Photo,  Enquiry

class advertUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ( 'advert' ,'contact_info' )

class noteUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('note',)

class PhotoInsertForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'cover', 'priority')

class PhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'priority')

class EnquiryInsertForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ('content',)
