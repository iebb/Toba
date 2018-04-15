from django.conf.urls import url, include
from rest_framework import routers
from todo import views
from rest_framework.urlpatterns import format_suffix_patterns


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    #url(r'^users/$', views.UserList.as_view()),
	#url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

	url(r'^summary/$', views.UserInfo.as_view()),
	
    url(r'^list/$', views.TodoList.as_view()),
	url(r'^detail/(?P<pk>[0-9]+)/$', views.TodoDetail.as_view()),

    url(r'^add/$', views.TodoAdd.as_view()),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.TodoEdit.as_view()),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.TodoDelete.as_view()),
    url(r'^progress/(?P<pk>[0-9]+)/$', views.TodoProgress.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)