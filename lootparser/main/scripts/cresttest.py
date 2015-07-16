#!/usr/bin/env python

import pycrest


def getByAttrVal(objlist, attr, val):
    ''' Searches list of dicts for a dict with dict[attr] == val '''
    matches = [getattr(obj, attr) == val for obj in objlist]
    index = matches.index(True)  # find first match, raise ValueError if not found
    return objlist[index]


def getAllItems(page):
    ''' Fetch data from all pages '''
    ret = page().items
    while hasattr(page(), 'next'):
        page = page().next()
        ret.extend(page().items)
    return ret


# instance of class used for exploring public crest data
eve = pycrest.EVE()

# initialize connection
eve()

# URI of region The Forge
the_forge = getByAttrVal(eve.regions().items, 'name', 'The Forge')

# URI of item Caldari Fuel Block
caldari_fuel_block = getByAttrVal(
        getAllItems(eve.itemTypes), 'name', 'Caldari Fuel Block').href

# List of orders for Caldari Fuel Block in The Forge
orders = getAllItems(the_forge().marketSellOrders(type=caldari_fuel_block))

print orders
