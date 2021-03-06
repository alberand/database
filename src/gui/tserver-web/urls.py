from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.MainPage.as_view(), name='index'),
        url(r'^GlobalMap/$', views.GlobalMap.as_view(), 
            name='GlobalMap'),
        url(r'^(?P<ses_id>[a-zA-Z0-9]+)/$', views.SessionPage.as_view(), 
            name='Session'),
        url(r'^(?P<ses_id>[a-zA-Z0-9]+)/Map$', views.MapPage.as_view(), 
            name='Map'),
        url(r'^(?P<ses_id>[a-zA-Z0-9]+)/download$', views.download_file, 
            name='ses_down'),
        url(r'^(?P<ses_id>[a-zA-Z0-9]+)/delete$', views.deleteSession, 
            name='ses_delete'),
        url(r'^(?P<ses_id>[a-zA-Z0-9]+)/(?P<new_name>[a-zA-Z0-9 ]+)/rename$', 
            views.renameSession, name='ses_rename'),
]
