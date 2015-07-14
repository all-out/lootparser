from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from main.views import PasteView, DisplayView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^paste/$', PasteView.as_view()),
    url(r'^paste/(?P<paste_id>\d+)/$', csrf_exempt(DisplayView.as_view())),
)
