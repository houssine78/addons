# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#     Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Belcotax Declaration Base",
    "version": "9.0.1.0",
    "depends": ["base"],
    "author": "Coop IT Easy SCRLfs",
    "category": "Belgian Localisation",
    "description": """
    This module manages the basis record of the belcotax declaration. It
    generates the basis record of the bow file according the technical
    documentation provided from the belgian fiscal administration. You
    can find the document following the url :
    https://finances.belgium.be/fr/E-services/Belcotaxonweb/documentation-technique

    To be able to generate a valid bow file you'll need to install the module
    implementing the sheet (fiche) that you need. All the sheets are described
    in the referred document above.
    """,
    'data': [
        'security/belcotax_security.xml',
        # 'security/ir.model.access.csv',
        'data/belcotax_declaration_data.xml',
        'views/belcotax_template_views.xml',
    ],
    'application': True,
    'installable': True,
}
