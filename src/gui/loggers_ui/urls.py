from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.MainPageView.as_view(), name='index'),
        url(r'^(?P<ses_id>[0-9]+)/$', views.PackagesList.as_view(), 
            name='Session'),
        url(r'^(?P<ses_id>[0-9]+)/download$', views.downloadfile, 
            name='ses_down'),
]
