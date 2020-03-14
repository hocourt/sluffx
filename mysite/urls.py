from django.contrib             import admin
from django.urls                import path, include
from django.conf                import settings
from django.conf.urls.static    import static

from .                          import views
from .views                     import PhotoInsert
#from .views                     import PhotoUpdate
#from .views                     import PhotoDelete

urlpatterns = [
    path('logout/',                     views.logout,                    {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('accounts/',                   include('django.contrib.auth.urls')),
    path('accounts/profile/' ,          views.fromlogin ),
    path('admin/',                      admin.site.urls),
#
    path('advertupdate',             	views.advert_update,                                                                name='advertupdate'),
    path('noteupdate',                  views.note_update,                                                                 name='noteupdate'),
    #path('notedelete',                  views.note_delete,                                                                 name='notedelete'),
    #path('contactus',             	views.contactus,                                                            name='contactus'),
#
    path('photolist',                   views.photo_list,                                                                  name='photolist'),
    path('photolistdeleted',            views.photo_list_deleted,                                                          name='photolistdeleted'),
    path('photoinsert',                 PhotoInsert.as_view(),                                                             name='photoinsert'),
    #path('photoupdate/<int:pk>/',       PhotoUpdate.as_view(),                                                             name='photoupdate'),
    path('photoupdate/<int:pk>/',       views.photo_update,                                                              name='photoupdate'),
    path('photorestore/<int:pk>/',      views.photo_restore,                                                             name='photorestore'),
    path('photodelete/<int:pk>/',       views.photo_delete,                                                              name='photodelete'),
    path('photodeleteperm/<int:pk>/',   views.photo_delete_perm,                                                         name='photodeleteperm'),
#
#
    path('enquirylist',                  views.enquiry_list,                                                                 name='enquirylist'),
    path('enquiryinsert',                  views.enquiry_insert,                                                                 name='enquiryinsert'),
#
    path('',                            include('events.urls')),
    path('',                            include('users.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
