# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright © 2017 Coop IT Easy (http://www.coopiteasy.be)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Houssine BAKKALI (https://github.com/houssine78)
# @author: Rémy TAYMANS <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

# TODO: scale_category is defined in beesdoo_product but this module do
#       not depend on it. Find a way to configure these fields.
ADDITIONAL_FIELDS = ['list_price', 'scale_category', 'image_medium']

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    scale_group_id = fields.Many2one(
        related="product_variant_ids.scale_group_id",
        string='Scale Group',
        store=True
    )
    scale_sequence = fields.Integer(
        related="product_variant_ids.scale_sequence",
        string='Scale Sequence',
        store=True
    )
    scale_tare_weight = fields.Float(
        related="product_variant_ids.scale_tare_weight",
        string='Scale Tare Weight',
        store=True,
        help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom."
    )

    # View Section
    @api.multi
    def send_scale_create(self):
        for product in self:
            # TODO: Should check if the product has a scale group
            product._send_to_scale_bizerba('create', True)
        return True

    @api.multi
    def send_scale_write(self):
        for product in self:
            # TODO: Should check if the product has a scale group
            product._send_to_scale_bizerba('write', True)
        return True

    @api.multi
    def send_scale_unlink(self):
        for product in self:
            # TODO: Should check if the product has a scale group
            product._send_to_scale_bizerba('unlink')
        return True

    # Custom Section
    def _send_to_scale_bizerba(self, action, send_product_image=False):
        log_obj = self.env['product.scale.log']
        log_obj.create({
            'log_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scale_system_id': self.scale_group_id.scale_system_id.id,
            'product_id': self.id,
            'action': action,
            'send_product_image': send_product_image,
        })

    def _check_vals_scale_bizerba(self, vals):
        system = self.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        for product_field in ADDITIONAL_FIELDS:
            if product_field not in system_fields:
                system_fields.append(product_field)
        vals_fields = vals.keys()
        return set(system_fields).intersection(vals_fields)

    def is_in_scale(self):
        """Return True if the current product should be in the scale
        system.
        """
        self.ensure_one()
        return self.active and self.sale_ok and self.scale_group_id

    def is_new_in_scale(self, vals):
        """Return True if the current product will be new in the scale
        system after the write.
        """
        return not self.is_in_scale() and self.will_be_in_scale(vals)

    def will_be_in_scale(self, vals):
        """Return True if the current product will be in the scale
        system after the write.
        """
        self.ensure_one()
        return (vals.get('active', self.active)
                and vals.get('sale_ok', self.sale_ok)
                and vals.get('scale_group_id', self.scale_group_id))

    # Overload Section
    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        if product.is_in_scale():
            product._send_to_scale_bizerba('create')
        return product

    @api.multi
    def write(self, vals):
        defered = {}
        for product in self:
            if product.is_new_in_scale(vals):
                # Product is new to the scale system: create it.
                defered[product.id] = 'create'
            elif product.is_in_scale() and product.will_be_in_scale(vals):
                # Product is in the scale system and will be in the
                # scale system after the write: if there is changes in
                # the fields related to the scale system, update it.
                if product._check_vals_scale_bizerba(vals):
                    defered[product.id] = 'write'
                # If scale_group has change, product must be updated.
                if ('scale_group_id' in vals
                        and vals['scale_group_id'] != product.scale_group_id):
                    # Remove it from previous group
                    product._send_to_scale_bizerba('unlink')
                    # Send it in the new group
                    defered[product.id] = 'create'
            elif product.is_in_scale() and not product.will_be_in_scale(vals):
                # Product is in the scale system and will no longer be
                # in the scale system after the write: delete it.
                product._send_to_scale_bizerba('unlink')

        res = super(ProductTemplate, self).write(vals)

        for product_id, action in defered.iteritems():
            product = self.browse(product_id)
            product._send_to_scale_bizerba(action, True)

        return res

    @api.multi
    def unlink(self):
        for product in self:
            if product.is_in_scale():
                self._send_to_scale_bizerba('unlink')
        return super(ProductTemplate, self).unlink()
