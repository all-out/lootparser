from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View, ListView, DetailView

from main.models import Paste
from functions import get_values

import datetime
import json
import re
import requests


class PasteView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response(
                'create_paste.html', context,
                context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = {}

        # get the evepraisal URL from our form
        ep_link = request.POST.get('ep_link', None)

        # Try to parse form input.  If the regex fails to find satisfactory
        # link, an AttributeError is caught and the form is reloaded.
        try:

            # use a regex to get the evepraisal id from the URL and look up
            # whether this paste already exists in the database
            regex = r'(?<=\/)\d+$'
            ep_id = int(re.search(regex, ep_link).group())
            paste, created = Paste.objects.get_or_create(ep_id=ep_id)

            # if paste has never been seen before, we have fields to populate:
            if True:
                print '\n\n DEBUGGING (PASTED IS UPDATED ON EVERY CALL)'

                # populate the paste's ep_link field with the evepraisal URL
                paste.ep_link = ep_link

                # pull the json from evepraisal's API
                response = requests.get(ep_link + '.json')

                # format the json response into a python dictionary
                response_dict = response.json()

                # populate evepraisal fields of the paste object with the dict
                paste.ep_kind = response_dict['kind']
                paste.ep_market_id = response_dict['market_id']
                paste.ep_market_name = response_dict['market_name']
                paste.ep_totals_buy = response_dict['totals']['buy']
                paste.ep_totals_sell = response_dict['totals']['sell']
                paste.ep_totals_volume = response_dict['totals']['volume']

                # dump the python dictionary into a json-formatted string and
                # save the string into the ep_json field
                paste.ep_json = json.dumps(response_dict)

                # get timestamp, convert it to datetime field and save it
                timestamp = response_dict['created']
                paste.created = datetime.datetime.fromtimestamp(timestamp)

                # pass the response dictionary off to get the eve-central
                # values for blueloot and salvage (from the appropriate
                # stations, regardless of where the evepaste was taken)
                blueloot_value, salvage_value = get_values(response_dict)

                # populate the paste's blueloot, salvage, and total fields
                paste.blueloot_value = blueloot_value
                paste.salvage_value = salvage_value
                paste.total_value = blueloot_value + salvage_value

                # save the updated paste object to the database
                paste.save()

            # redirect to the paste's display page
            return redirect('display', paste_id=paste.ep_id)

        except AttributeError, e:
            print e
            return render_to_response(
                    'create_paste.html', context,
                    context_instance=RequestContext(request))


class PasteList(ListView):
    queryset = Paste.objects.all().order_by('-created')
    template_name = 'pastes.html'
    context_object_name = 'pastes'


class PasteDetail(DetailView):
    model = Paste
    template_name = 'paste.html'
    context_object_name = 'paste'


class DisplayView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        paste_id = self.kwargs['paste_id']
        context['paste'] = Paste.objects.get(ep_id=paste_id)
        return render_to_response(
                'display.html', context,
                context_instance=RequestContext(request))
