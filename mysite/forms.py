from django                                 import forms
from .models                                import Sitesettings, Photo, Note

class SiteadminForm(forms.ModelForm):
    class Meta:
        model = Sitesettings
        fields = ( 'private_site', 'advert' ,'contact_info' ,'status' , 'reversevideo' , 'datecolor' , 'detailcolor' , 'attendeescolor' , 'backgroundcolor' , 'datecolor_rev' , 'detailcolor_rev' , 'attendeescolor_rev' , 'backgroundcolor_rev' ,     'notes' )

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'cover', 'priority')

class PhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'priority')

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('note_content',)
