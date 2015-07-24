from lxml import html
import requests


def get_values(response_dict):
    '''Takes a dictionary created from the json given by evepraisal.  Returns
    a tuple of the form (total_blueloot_value, total_salvage_value).'''

    #
    # CONSTANTS:
    #

    ec_marketdata_url = 'http://api.eve-central.com/api/marketstat'

    system = {
        'Jita': 30000142,
        'Amarr': 30002187,
        'Dodixie': 30002659,
        'Rens': 30002510,
        'Hek': 30002053,
    }

    #
    # DEAL WITH SLEEPER LOOT
    #

    # make a dictionary of only "Sleeper Components" (groupID 880)
    blueloot = {item['typeID']: item['quantity']
                for item in response_dict['items']
                if item['groupID'] == 880}

    # make blueloot URL parameter payload dictionary
    blueloot_payload = {
        'usesystem': system['Amarr'],
        'typeid': [key for key in blueloot.keys()]
    }

    # make blueloot price request and create a document tree
    blueloot_response = requests.get(ec_marketdata_url, blueloot_payload)
    blueloot_tree = html.fromstring(blueloot_response.content)

    # initialize blueloot total to zero
    blueloot_value = 0

    # for every typeid of blueloot
    for (typeid, quantity) in blueloot.items():

        # create path, use it to get typeid's price from the tree
        # note! blueloot price is MAX AMARR BUY ORDER
        path = '//*[@id="%d"]/buy/max/text()' % typeid
        price = float(blueloot_tree.xpath(path)[0])

        # calculate value of the stack of this typeid
        typeid_stack_value = price * quantity

        # update the total value
        blueloot_value += typeid_stack_value

    print 'total blueloot value', blueloot_value

    #
    # DEAL WITH SALVAGE
    #

    # make a dictionary of everything else (not groupID 880)
    salvage = {item['typeID']: item['quantity']
               for item in response_dict['items']
               if item['groupID'] != 880}

    # make salvage URL parameter payload dictionary
    salvage_payload = {
        'usesystem': system['Dodixie'],
        'typeid': [key for key in salvage.keys()]
    }

    # make salvage price request and create a document tree
    salvage_response = requests.get(ec_marketdata_url, salvage_payload)
    salvage_tree = html.fromstring(salvage_response.content)

    # initialize salvage total to zero
    salvage_value = 0

    # for every typeid of salvage
    for (typeid, quantity) in salvage.items():

        # create path, use it to get typeid's price from the tree note!
        # salvage price is AVERAGE OF MAX DODIXIE BUY AND MIN DODIXIE SELL
        # ORDERS
        buy_path = '//*[@id="%d"]/buy/max/text()' % typeid
        sell_path = '//*[@id="%d"]/sell/min/text()' % typeid
        buy_price = float(salvage_tree.xpath(buy_path)[0])
        sell_price = float(salvage_tree.xpath(sell_path)[0])
        price = (buy_price + sell_price) / 2.0

        # calculate value of the stack of this typeid
        typeid_stack_value = price * quantity

        # update the total value
        salvage_value += typeid_stack_value

    print 'total salvage value', salvage_value

    return (blueloot_value, salvage_value)
