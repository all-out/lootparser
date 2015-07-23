#!/usr/bin/env python

import mechanize
import re

# sample paste strings
paste_string = 'Gallente Frigate    1    Spaceship Command            0,01 m3'
paste_string = 'Nanite Repair Paste\t499\tNanite Repair Paste\t\t\t4,99 m3'

# pre-filled station IDs
jita = [30000142]
amarr = [30002187]
dodixie = [30002659]
rens = [30002510]
hek = [30002053]
universe = [-1]

# create a browser object, give it a google chrome user-agent, and open
# the evepraisal site with it.
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
br.open('http://evepraisal.com/')

# list the forms on the page
# for i, form in enumerate(br.forms()):
#   print "form name:", form.name, 'form index:', i
#   print form

# form name: None
# <POST http://evepraisal.com/estimate application/x-www-form-urlencoded
#   <TextareaControl(raw_textarea=)>
#   <HiddenControl(load_full=1) (readonly)>
#   <SubmitButtonControl(<None>=) (readonly)>
#   <IgnoreControl(<None>=<None>)>
#   <SelectControl(<None>=[])>
#   <SelectControl(<None>=[*30000142])>
#   <SelectControl(<None>=[*30002187])>
#   <SelectControl(<None>=[*30002659])>
#   <SelectControl(<None>=[*30002510])>
#   <SelectControl(<None>=[*30002053])>
#   <SelectControl(<None>=[*-1])>>

# select the form (unnamed in this case; index 0)
# br.form = list(br.forms())[0]
br.select_form(nr=0)

br.form.controls[0]._value = paste_string
br.form.controls[4]._value = dodixie

# br.form.set_value(paste_string, nr=0)  # set the paste value
# br.form.set_value(dodixie, nr=4)       # set the station value


# submit form
response = br.submit()
print response.read()
br.back()
