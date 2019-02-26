# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Enterprise Management Solution
#    Copyright (C) 2014 Boss Consulting sprl (<http://openerp.com>).
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

import time
from openerp.osv import fields,osv

class res_partner(osv.Model):
    _inherit = 'res.partner'

    _columns = {
        'vat_check_vies':fields.boolean('vat check'),
                }
    
    _defaults = {
        'vat_check_vies': False,   
    }

    def open_wizard_vies(self, cr, uid, ids, context):
        res_partner =  self.pool.get('res.partner').browse(cr,uid, ids[0])
        mod_obj = self.pool.get('ir.model.data')
        model_data_ids = mod_obj.search(cr, uid, [('model','=','ir.ui.view'),('name', '=', 'vies_ws_wizard')], context=context)[0]
        resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'], context=context)['res_id']
        ctx = context.copy()
        ctx.update({'default_vat_number': res_partner.vat, 'default_mode' : 'update_partner'})
        return {
            'context': ctx,
            'res_model':'vies.ws.wizard',
            'view_type':'form',
            'view_mode':'form',
            'type': 'ir.actions.act_window',
            'view_id': resource_id,
            'target': 'new',
        }
        

      
    
    

