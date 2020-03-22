from django.contrib             import admin
from django.urls                import path, include
from django.conf                import settings
from django.conf.urls.static    import static
from .                          import views
from .views                     import PhotoInsert
#from .views                     import PhotoBInsert
urlpatterns = [
    path('logout/',                             views.logout,                    {'next_page': settings.LOGOUT_REDIRECT_URL},  name='logout'),
    path('accounts/',                           include('django.contrib.auth.urls')),
    path('accounts/profile/' ,                  views.fromlogin ),
    path('admin/',                              admin.site.urls),
#
#
    path('advertupdate',             	        views.advert_update,                                                           name='advertupdate'),
    path('noteupdate',                          views.note_update,                                                             name='noteupdate'),
#
#
    path('photolist',                           views.photo_list,                                                              name='photolist'),
    path('photolistdeleted',                    views.photo_list_deleted,                                                      name='photolistdeleted'),
#
    path('photoinsert',                         PhotoInsert.as_view(),                                                         name='photoinsert'),
#
    path('photoauthorupdate/<int:pk>/',         views.photoauthor_update,                                                      name='photoauthorupdate'),
    path('photopriorityupdate/<int:pk>/',       views.photopriority_update,                                                    name='photopriorityupdate'),
    path('phototitleupdate/<int:pk>/',          views.phototitle_update,                                                       name='phototitleupdate'),
    path('photorestore/<int:pk>/',              views.photo_restore,                                                           name='photorestore'),
    path('photodelete/<int:pk>/',               views.photo_delete,                                                            name='photodelete'),
#
    path('photodeleteperm/<int:pk>/',           views.photo_delete_perm,                                                       name='photodeleteperm'),
#
#
    path('enquirylist',                         views.enquiry_list,                                                            name='enquirylist'),
    path('enquirylistdeleted',                  views.enquiry_list_deleted,                                                    name='enquirylistdeleted'),
#
    path('enquiryinsert',                       views.enquiry_insert,                                                          name='enquiryinsert'),
#
    path('enquirydelete/<int:pk>/',             views.enquiry_delete,                                                          name='enquirydelete'),
#
    path('enquirydeleteperm/<int:pk>/',         views.enquiry_deleteperm,                                                      name='enquirydeleteperm'),
#
#
    path('',                                    include('events.urls')),
    path('',                                    include('users.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    path('photoBlist',                           views.photoB_list,                                                              name='photoBlist'),
    path('photoBlistdeleted',                    views.photoB_list_deleted,                                                      name='photoBlistdeleted'),
#
    path('photoBinsert',                         PhotoBInsert.as_view(),                                                         name='photoBinsert'),
#
    path('photoBauthorupdate/<int:pk>/',         views.photoBauthor_update,                                                      name='photoBauthorupdate'),
    path('photoBpriorityupdate/<int:pk>/',       views.photoBpriority_update,                                                    name='photoBpriorityupdate'),
    path('photoBtitleupdate/<int:pk>/',          views.photoBtitle_update,                                                       name='photoBtitleupdate'),
    path('photoBrestore/<int:pk>/',              views.photoB_restore,                                                           name='photoBrestore'),
    path('photoBdelete/<int:pk>/',               views.photoB_delete,                                                            name='photoBdelete'),
#
    path('photoBdeleteperm/<int:pk>/',           views.photoB_delete_perm,                                                       name='photoBdeleteperm'),
#
#
"""
