from django                                 import forms
from .models                                import Site, Photo,  EnquiryB
#from .models                                import Site, Photo
#from .models                                import PhotoB

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

class PhotoauthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('author',)

class PhotopriorityUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('priority',)

class PhototitleUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title',)

"""
class PhotoBInsertForm(forms.ModelForm):
    class Meta:
        model = PhotoB
        fields = ('title', 'content', 'priority')

class PhotoBauthorUpdateForm(forms.ModelForm):
    class Meta:
        model = PhotoB
        fields = ('author',)

class PhotoBpriorityUpdateForm(forms.ModelForm):
    class Meta:
        model = PhotoB
        fields = ('priority',)

class PhotoBtitleUpdateForm(forms.ModelForm):
    class Meta:
        model = PhotoB
        fields = ('title',)

"""
class EnquiryInsertForm(forms.ModelForm):
    class Meta:
        model = EnquiryB
        fields = ('content',)
