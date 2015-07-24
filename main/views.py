from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View

from main.models import Paste

from lxml import html
import datetime
import json
import re
import requests


class PasteView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render_to_response(
                'paste.html', context,
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
            if created:

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

                # make a dictionary of only "Sleeper Components" (groupID 880)
                blueloot = {item['typeID']: item['quantity']
                            for item in response_dict['items']
                            if item['groupID'] == 880}

                # make a dictionary of everything else (not groupID 880)
                salvage = {item['typeID']: item['quantity']
                           for item in response_dict['items']
                           if item['groupID'] != 880}

                # prepare params for blue loot price request from EveCentral
                ec_marketdata_url = 'http://api.eve-central.com/api/marketstat'
                amarr_station_id = 30002187
                blueloot_payload = {
                    'usesystem': amarr_station_id,
                    'typeid': [key for key in blueloot.keys()]
                }

                # make blue loot price request and create a document tree
                response = requests.get(ec_marketdata_url, blueloot_payload)
                tree = html.fromstring(response.content)

                # initialize total to zero
                blue_loot_value = 0

                # for every typeid of blue loot
                for (typeid, quantity) in blueloot.items():

                    # create path, use it to get typeid's price from the tree
                    path = '//*[@id="%d"]/buy/max/text()' % typeid
                    price = float(tree.xpath(path)[0])

                    # calculate value of the stack of this typeid
                    typeid_value = price * quantity

                    # update the total value
                    blue_loot_value += typeid_value

                print 'total blue loot value', blue_loot_value

                # save the updated paste object to the database
                paste.save()

            # redirect to the paste's display page
            return redirect('display', paste_id=paste.ep_id)

        except AttributeError, e:
            print e
            return render_to_response(
                    'paste.html', context,
                    context_instance=RequestContext(request))


class DisplayView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        paste_id = self.kwargs['paste_id']
        context['paste'] = Paste.objects.get(ep_id=paste_id)
        return render_to_response(
                'display.html', context,
                context_instance=RequestContext(request))
