from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from main.views import Paste

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^paste/', 'main.views.paste'),    # default paste
    url(r'^paste/', csrf_exempt(Paste.as_view())),
)
