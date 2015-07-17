from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import login as django_login
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View, TemplateView
from main.models import Paste
import evepaste
import json
import pycrest


def login(request):
    return django_login(request, template_name='login.html')


def logout(request):
    django_logout(request)
    return redirect('/')


class OldPasteView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response(
            'paste.html', context,
            context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = {}
        raw_paste = request.POST.get('raw_paste', None)
        new_paste = Paste(raw_paste=raw_paste)
        parsed = evepaste.parse(raw_paste)
        new_paste.parsed = json.dumps(parsed)
        new_paste.save()
        return redirect('display', paste_id=new_paste.id)


class PasteView(TemplateView):
    template_name = 'paste.html'

    def get_public_crest_context(self):
        '''fetch some example stuff from public crest'''

        # declare and initialize the public connection object
        public_crest = pycrest.EVE()
        public_crest()

        tq_user_count = public_crest.userCounts.eve

        return {'tq_user_count': tq_user_count}

    def get_authed_crest_context(self):
        '''fetch some example stuff from authenticated crest'''

        # declare and initialize the authed connection object
        # (here we rudely fumble some of pycrest's private parts since we
        # already completed the auth process via python-social-auth)
        authed_crest = pycrest.eve.AuthedConnection(
            res=self.request.user._get_crest_tokens(),
            endpoint=pycrest.EVE()._authed_endpoint,
            oauth_endpoint=pycrest.EVE()._oauth_endpoint,
            client_id=settings.SOCIAL_AUTH_EVEONLINE_KEY,
            api_key=settings.SOCIAL_AUTH_EVEONLINE_SECRET,
        )
        authed_crest()

        # demo of accessing market data
        endpoint = pycrest.EVE()._authed_endpoint
        type_id = 34    # Tritanium
        region_id = 10000002    # The Forge
        type_url = '{0}types/{1}/'.format(endpoint, type_id)
        buy_orders_url = '{0}market/{1}/orders/buy/?type={2}'.format(
                endpoint, region_id, type_url)
        sell_orders_url = '{0}market/{1}/orders/sell/?type={2}'.format(
                endpoint, region_id, type_url)

        # sort appropriately by price
        sell_orders = sorted(sell_orders, key=lambda k: k['price'])
        buy_orders = sorted(buy_orders, key=lambda k: k['price'], reverse=True)

        # truncate to Top <limit> orders
        limit = 5
        if len(sell_orders) > limit:
            sell_orders = sell_orders[0:limit]
        if len(buy_orders) > limit:
            buy_orders = buy_orders[0:limit]

        return {
            'sell_orders': sell_orders,
            'buy_orders': buy_orders,
        }

    def get_context_data(self, **kwargs):
        context = super(PasteView, self).get_context_data(**kwargs)
        context['public_crest'] = self.get_public_crest_context()
        context['authed_crest'] = self.get_authed_crest_context()
        return context


class DisplayView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        paste_id = self.kwargs['paste_id']
        context['paste'] = Paste.objects.get(id=paste_id)
        context['parsed'] = json.loads(context['paste'].parsed)
        return render_to_response(
                'display.html', context,
                context_instance=RequestContext(request))
