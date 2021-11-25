# Copyright 2021 Eezee-IT (<http://www.eezee-it.com>)
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, _
from odoo.exceptions import UserError

from collections import OrderedDict

import base64
import io
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    print_all_pdf_attachments = fields.Boolean()

    def retrieve_all_attachments(self, record):
        return self.env['ir.attachment'].search([
            ('res_model', '=', self.model),
            ('res_id', '=', record.id),
            ('mimetype', '=', 'application/pdf')
        ])

    def _retrieve_stream_from_all_attachments(self, attachments):
        streams = []
        for attachment in attachments:
            streams.append(io.BytesIO(base64.decodebytes(attachment.datas)))
        return self._merge_pdfs(streams)

    def _render_qweb_pdf(self, res_ids=None, data=None):
        if not self.print_all_pdf_attachments:
            return super(IrActionsReport, self)._render_qweb_pdf(res_ids, data)

        self_sudo = self.sudo()

        save_in_attachment = OrderedDict()
        # Maps the streams in `save_in_attachment` back to the records they came from
        stream_record = dict()
        if res_ids:
            record_ids = self.env[self_sudo.model].browse(res_ids)
            for record_id in record_ids:
                attachments = self_sudo.retrieve_all_attachments(record_id)
                if attachments:
                    stream = self_sudo._retrieve_stream_from_all_attachments(attachments)
                    save_in_attachment[record_id.id] = stream
                    stream_record[stream] = record_id

        if save_in_attachment and res_ids and len(save_in_attachment) == 1:
            _logger.info('The PDF report has been generated from all the pdf attachments.')
            return list(save_in_attachment.values())[0], 'pdf'
        raise UserError(_('No pdf attachments to print'))
