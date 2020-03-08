#from django.conf             import settings
#from django.conf.urls.static import static
#from django.conf.urls        import url
from django.urls              import  path
#from django.urls              import  re_path
from django.conf              import settings
from django.conf.urls.static  import static
from .                        import views
from .views                   import EventInsert, EventUpdate, EventDelete

urlpatterns = [
    path('',                                              views.event_list,                   name='homepage'),
    path('eventlist/<slug:periodsought>/)',               views.event_list,                   name='eventlist'),
    path('eventdetail/,int:pk>/)',                        views.event_detail,                 name='eventdetail'),
#
    path('eventinsert',                                   EventInsert.as_view(),                name='eventinsert'),
    path('eventrestore/<int:pk>/)',                       views.restore,                      name='eventrestore'),
    path('eventrepeat/<int:pk>/)',                        views.event_repeat,                 name='eventrepeat'),
#
    path('eventupdate/<int:pk>/)',                        EventUpdate.as_view(),                 name='eventupdate'),
    path('bookinto/<int:pk>/)',                           views.bookinto,                     name='bookinto'),
    path('leave/<int:pk>/)',                              views.leave,                        name='leave'),
    path('hostsupdate/<int:pk>/)',                        views.hosts_update,                 name='hostsupdate'),
    path('attendeesupdate/<int:pk>/)',                    views.attendees_update,             name='attendeesupdate'),
#
    path('eventdelete/<int:pk>/)',                        EventDelete.as_view(),                name='eventdelete'),
    path('eventdeleteperm/<int:pk>/)',                    views.event_deleteperm,             name='eventdeleteperm'),
#
    path('noticeupdate',                                  views.notice_update,                name='noticeupdate'),
    path('noticedelete',                                  views.notice_delete,                name='noticedelete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
