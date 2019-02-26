# -*- coding: utf-8 -*-
#
#
#    Authors: Houssine BAKKALI
#    Copyright (c) 2014 Boss Consulting (http://www.boss-consulting.be)
#    All Rights Reserved
#
#    WARNING: This program as such is intended to be used by professional
#    programmers who take the whole responsibility of assessing all potential
#    consequences resulting from its eventual inadequacies and bugs.
#    End users who are looking for a ready-to-use solution with commercial
#    guarantees and support are strongly advised to contact a Free Software
#    Service Company.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    "name": "vies_client",
    "version": "1.0",
    "author": "Boss Consulting",
    "category": "Generic Modules/CRM",
    "website": "http://www.boss-consulting.be",
    
    "images": 
        [
        'static/img/Flag_VIES.png',
        ],
    
    "depends": [
        'base',
        'crm',
    ],
    'external_dependencies': {
        'python': ['lxml','suds'],
    },
    "description": """
VIES Client - 
==========================================

Intro

Main Features
-------------
* create a partner through its vat number and the info provide by the VIES webservices 
* 
* 
* 

Technical information
---------------------

You will need to install the suds python module to enable the webservice through soap client

Contributors
------------
* Houssine BAKKALI <houssine.bakkali@gmail.com>
""",
    "data": [
        'res_partner_view.xml',
        'wizard/vies_ws_wizard_view.xml',
    ],
    "demo": [],
    "license": "AGPL-3",
    "installable": True,
    'css': ['static/src/css/vie_client.css'],
}
