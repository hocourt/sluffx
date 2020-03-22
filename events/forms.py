from django                                 import forms
from django.forms.widgets                   import CheckboxSelectMultiple
from .models                                import Event,Notice
from users.models                           import Person
#from django.contrib.auth.models             import User

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('e_date', 'detail_public', 'attendees')
    def __init__(self, *args, **kwargs):
        super(AttendeeForm, self).__init__(*args, **kwargs)
        self.fields["attendees"].widget = CheckboxSelectMultiple()
        self.fields["attendees"].queryset = Person.objects.filter(status__lte=60).exclude(status=10).order_by('display_name')

class HostForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('e_date', 'detail_public', 'hosts')
    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        self.fields["hosts"].widget = CheckboxSelectMultiple()
        self.fields["hosts"].queryset = Person.objects.filter(status__lte=60).exclude(status=10).order_by('display_name')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('e_date', 'detail_public', 'detail_private', 'photo_cover')

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('notice',)
