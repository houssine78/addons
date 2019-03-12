# -*- coding: utf-8 -*-

from openerp import fields, models


class BelcotaxTemplate(models.Model):
    _name = "belcotax.template"

    name = fields.Char(string="name")
    fiscal_year = fields.Char(string="Fiscal year")
    record_templates = fields.One2many('belcotax.record.template',
                                       'belcotax_template',
                                       string="Record templates")


class BelcotaxRecordTemplate(models.Model):
    _name = "belcotax.record.template"

    name = fields.Char(string="name")
    belcotax_template = fields.Many2one('belcotax.template',
                                        string="Belcotax template")
    record_fields = fields.One2many('belcotax.fields.template',
                                    'record_template',
                                    string="Record fields")
    parent_record = fields.Many2one('belcotax.record.template',
                                    string="Parent record")
    has_fields = fields.Boolean(string="Has fields?")


class BelcotaxFieldsTemplate(models.Model):
    _name = "belcotax.fields.template"

    name = fields.Char(string="name")
    record_template = fields.Many2one('belcotax.record.template',
                                      string="Record template")
    type = fields.Selection([('num', 'Numeric'),
                            ('alpha', 'AlphaNumeric'),
                            ('date', 'Date')],
                            string="Field type")
