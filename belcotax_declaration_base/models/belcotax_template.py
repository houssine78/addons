# -*- coding: utf-8 -*-

from openerp import fields, models


class BelcotaxTemplate(models.Model):
    _name = "belcotax.template"

    name = fields.Char(string="name")


class BelcotaxRecordTemplate(models.Model):
    _name = "belcotax.record.template"

    name = fields.Char(string="name")
    record_fields = fields.One2many('belcotax.fields.template',
                                    'record_template',
                                    string="Record fields")
    parent_record = fields.Many2one('belcotax.record.template',
                                    string="Parent record")


class BelcotaxFieldsTemplate(models.Model):
    _name = "belcotax.fields.template"

    name = fields.Char(string="name")
    record_template = fields.Many2one('belcotax.record.template',
                                      string="Record template")
    type = fields.Selection([('num', 'Numeric'),
                            ('alpha', 'AlphaNumeric'),
                            ('date', 'Date')],
                            string="Field type")
