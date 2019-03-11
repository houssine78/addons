# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
# Nicolas Jamoulle, <nicolas@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Default number of lines in journal items",
    "version": "9.0.1.0",
    "depends": [
        'account',
    ],
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "website": "www.coopiteasy.be",
    "description": """
        Allow to change d efault number of lines in journal items
    """,
    "data": [
        'views/account_journal_view.xml',
    ],
    'installable': True,
}
