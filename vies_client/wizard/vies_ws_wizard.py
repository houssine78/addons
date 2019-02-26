# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
import logging
_logger = logging.getLogger(__name__)

try:
    import vatnumber
except ImportError:
    _logger.warning("VAT validation partially unavailable because the `vatnumber` Python library cannot be found. "
                                          "Install it to support more countries, for example with `easy_install vatnumber`.")
    vatnumber = None

from openerp.osv import fields, orm
from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import suds

vies_wsdl = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
"""The WSDL URL of the VAT Information Exchange System (VIES)."""

_vies_client = None

def _check_vies(vat):
    '''
    Check VAT number for EU member state using the SOAP Service
    '''
    import stdnum.eu.vat
    return bool(stdnum.eu.vat.check_vies(vat)['valid'])    
    
'''
Check VAT number for EU member state using the SOAP Service and get a more detailed response
'''

def _check_vat_approx(vat):
    import stdnum.eu.vat
    number = stdnum.eu.vat.compact(vat)
    global _vies_client
    if not _vies_client:
        from suds.client import Client
        from urllib import getproxies
        _vies_client = Client(vies_wsdl, proxy=getproxies())
    return _vies_client.service.checkVatApprox(number[:2], number[2:])

class vies_ws_wizard(orm.TransientModel):
    _name = "vies.ws.wizard"
    _description = "Vies webservices client wizard"

    _columns = {
        'name': fields.char('Name', select=True),
        'vat_number': fields.char('VAT Number', size=64, required=True),
        'street': fields.char('Street'),
        'street2': fields.char('Street2'),
        'zip': fields.char('Zip', size=24, change_default=True),
        'city': fields.char('City'),
        'country_id': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'customer': fields.boolean('Customer', help="Check this box if this contact is a customer."),
        'supplier': fields.boolean('Supplier', help="Check this box if this contact is a supplier. If it's not checked, purchase people will not see it when encoding a purchase order."),
        'mode': fields.char('Mode', size=32),
        'brut_address': fields.char('Address', size=128),
    }
    
    def get_country_id(self, cr, uid, country_code, context):
        return self.poolt.get('res.county').search(cr, uid, [('code','=',country_code)])
    
    def call_vies_webservice(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        data = self.read(cr, uid, ids, context=context)[0]
        format_ok = self.pool.get('res.partner').simple_vat_check(cr, uid, data['vat_number'][:2], data['vat_number'][2:], context)
        if format_ok:
            try:
                vies_result = _check_vat_approx(data['vat_number'])
                if bool(vies_result['valid']) :
                    data['name'] = vies_result['traderName']
                    country_code = vies_result['countryCode']
                    country_id = self.pool.get('res.country').search(cr, uid, [('code','=',country_code)])
                    if country_id and len(country_id) == 1 : 
                        data['country_id'] = country_id[0]
                    address  =  vies_result['traderAddress']
                    address = address.split('\n')
                    if country_code == 'BE':
                        data['zip'] = address[1][0:4].strip()
                        data['city'] = address[1][4:len(address[1])].strip()
                    else:
                        city_zip= address[1].split(' ')
                        data['zip'] = city_zip[0]
                        data['city'] = city_zip[1]
                    data['street'] = address[0]
                    data['brut_address'] = ''
                    for elem in address:
                        data['brut_address'] += elem + ' - '
                    self.write(cr,uid,ids,data,context)
                    model_data_ids = mod_obj.search(cr, uid, [('model','=','ir.ui.view'),('name', '=', 'vies_partner_view_wizard')], context=context)[0]
                    resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'], context=context)['res_id']
                    return {'context': context,
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'vies.ws.wizard',
                            'views': [(resource_id,'form')],
                            'res_id': ids[0],
                            'type': 'ir.actions.act_window',
                            'target': 'new',
                    }
                else:
                    raise except_orm(_("Warning"),_("The VAT Number you introduced doesn't exist ."))
            except suds.WebFault as detail:
                print detail
                #Server raised fault: 'MS_UNAVAILABLE'
                raise except_orm(_("Error"),_("The Vies server is busy, please try again later."))
        else:
            raise except_orm(_("Warning"),_("The format of the VAT Number you introduced isn't valid ."))
        
    def create_partner(self,cr, uid,ids, context):
        data = {}
        vies_partner = self.browse(cr, uid, ids, context=context)[0]
        data['name'] = vies_partner.name
        data['country_id'] = vies_partner.country_id.id
        data['zip'] = vies_partner.zip
        data['city'] = vies_partner.city
        data['street'] = vies_partner.street
        data['vat'] = vies_partner.vat_number
        data['customer'] = vies_partner.customer
        data['supplier'] = vies_partner.supplier
        data['vat_check_vies']=True
        self.pool.get('res.partner').create(cr, uid, data, context)
        self.unlink(cr,uid, ids,context)
        
        return {
            'type': 'ir.actions.act_window_close'
        }
        
    def update_partner(self, cr, uid, ids, context):
        data = {}
        vies_partner = self.browse(cr, uid, ids, context=context)[0]
        data['name'] = vies_partner.name
        data['country_id'] = vies_partner.country_id.id
        data['zip'] = vies_partner.zip
        data['city'] = vies_partner.city
        data['street'] = vies_partner.street
        data['vat'] = vies_partner.vat_number
        data['vat_check_vies']=True
        data['customer'] = vies_partner.customer
        data['supplier'] = vies_partner.supplier
        self.pool.get('res.partner').write(cr, uid, context.get('active_id'),data, context)
        self.unlink(cr,uid, ids,context)
        
        return {
            'type': 'ir.actions.act_window_close'
        }
        