from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^input/$', views.input, name='input'),
    url(r'^(?P<username>\w+)/$', views.results, name='results'),
]