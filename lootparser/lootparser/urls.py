from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from main.views import PasteView, DisplayView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^paste/$', PasteView.as_view(), name='paste'),
    url(r'^paste/(?P<paste_id>\d+)/$', DisplayView.as_view(), name='display'),
)
