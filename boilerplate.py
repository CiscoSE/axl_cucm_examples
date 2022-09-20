# Copyright (c) 2022 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin

from requests import Session
from requests.auth import HTTPBasicAuth

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from lxml import etree

import tabulate

disable_warnings(InsecureRequestWarning)

username = 'administrator'
password = 'ciscopsdt'

host = '10.10.20.1'
port = 8443

wsdl = 'axlsqltoolkit/schema/current/AXLAPI.wsdl'
location = f"https://{host}:{port}/axl/"
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)

transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()

client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item['envelope'], encoding="unicode", pretty_print=True))
name = input("What's the name")
try:
    #resp = service.addUser(user={
    #    'lastName': "Test",
    #    'userid': "user99",
    #    'presenceGroupName': {
    #        'uuid': "{AD243D17-98B4-4118-8FEB-5FF2E1B781AC}"
    #    }
    #})

    #resp = service.updateUser(uuid="{0ED24848-D9EE-0CB9-FAEC-3E5DF3944AB7}", newUserid="user94", firstName="Mark")
    resp = service.listUser(searchCriteria={
                                'firstName': "%"
                            },
                            returnedTags={
                                'firstName' : "",
                                'userid': "",
                                'lastName': ""
                            })
    rows = []
    for user in resp['return'].user:
        rows.append([
            user.userid,
            user.firstName,
            user.lastName
        ])
    print(tabulate.tabulate(rows))
    #resp = service.listUser(searchCriteria={
    #            'firstName': "%"
    #        },
    #            returnedTags={
    #                'firstName': "",
    #                'userid': ""
    #            })
    #resp = service.listPresenceGroup(searchCriteria={
    #    'name': "%"
    #},
    #        returnedTags={
    #            'name': "",
    #            'description': ""
    #        })
except Fault:
    show_history()