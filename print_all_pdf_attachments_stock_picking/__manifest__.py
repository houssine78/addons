# Copyright 2021 Eezee-IT (<http://www.eezee-it.com> - info@eezee-it.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Print all stock picking pds attachments',
    'version': '14.0.1.0.1',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Stock',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'print_all_pdf_attachments'
    ],
    'data': [
        'report/print_picking_pdf.xml',
        'report/all_picking_pdf.xml'
    ],
    'installable': True,
}
