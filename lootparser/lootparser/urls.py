from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt

from main.views import PasteView, DisplayView, OldPasteView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', login_required(PasteView.as_view(), redirect_field_name=None)),
    url(r'^login/$', 'main.views.login', name='user_login'),
    url(r'^logout/$', 'main.views.logout', name='user_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^paste/$', OldPasteView.as_view(), name='paste'),
    url(r'^paste/(?P<paste_id>\d+)/$', DisplayView.as_view(), name='display'),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
