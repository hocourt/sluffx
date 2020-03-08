from django.contrib import admin
from .models     import Event
from .models     import Notice
admin.site.register(Event)
admin.site.register(Notice)