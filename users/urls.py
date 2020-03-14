#from django.conf             import settings
#from django.conf.urls.static import static
from django.conf.urls        import url
from django.urls             import  path
from .                       import views

urlpatterns = [
## Person
    # transactions that merely view the database
    path('memberlist',                                                                   views.member_list,        name='memberlist'),
    path('memberdetail/<int:pk>/)',                                                  views.member_detail,           name='memberdetail'),
    #path(r'branchlist',                                                                   views.branch_list,        name='branchlist'),
    # transactions that update the database using 'get'               
    path('promote/<int:pk>/)',                                                        views.promote,                name='promote'),
    path('demote/<int:pk>/)',                                                         views.demote,                 name='demote'),
    url(r'usercolours/(?P<type>[a-z]+)/(?P<color>[#a-zA-Z0-9]+)/(?P<whence>[a-z]+)',     views.user_colours,        name='usercolours'),
    url(r'defaultcolours/(?P<type>[a-z]+)/(?P<color>[#a-zA-Z0-9]+)/(?P<whence>[a-z]+)',  views.default_colours,     name='defaultcolours'),
    path('unsubscribe/<slug:confirmed>/)',                                             views.unsubscribe,           name='unsubscribe'),
    path('memberdelete/<int:pk>/<slug:confirmed>/)',                             views.member_delete,               name='memberdelete'),
    # transactions that update the database in two stages, using forms
    path('memberinsert',                                                                 views.member_insert,       name='memberinsert'),
    path('contactinsert',                                                                views.contact_insert,      name='contactinsert'),
    path('password/',                                                                      views.password,          name='password'),
    path('displayname/',                                                                   views.display_name,      name='displayname'),
    path('memberupdate/<int:pk>/)',                                                  views.member_amend,            name='memberupdate'),
## Message    
    # transactions that merely view the database
    path('messagelist',                                                                   views.message_list,        name='messagelist'),
    # transactions that update the database using 'get'               
    path('memberdelete/<int:pk>/<slug:confirmed>/)',                             views.member_delete,               name='memberdelete'),
    # transactions that update the database in two stages, using forms
    path('memberinsert',                                                                 views.member_insert,       name='memberinsert'),
]
