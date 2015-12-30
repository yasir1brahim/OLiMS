# -*- coding: utf-8 -*-

from openerp import api, fields, models
AR_STATES = (
    ('sample_registered','Sample Registered'),
    ('not_requested','Not Requested'),
    ('to_be_sampled','To Be Sampled'),
    ('sampled','Sampled'),
    ('to_be_preserved','To Be Preserved'),
    ('sample_due','Sample Due'),
    ('sample_received','Received'),
    ('attachment_due','Attachment Outstanding'),
    ('to_be_verified','To be verified'),
    ('verified','Verified'),
    ('published','Published'),
    ('invalid','Invalid'),
    )
CACELL_STATES = (
    ('active','Active'),
    ('cancelled','Cancelled'),
    )
WORKSHEET_STATES = (
    ('assigned','Assigned'),
    ('unassigned','Unassigned'),
    )

class OLiMSCommonOLiMSReport(models.TransientModel):
    _name = 'olims.common_olims_report'
    _description = 'OLiMS Common OLiMS Report'
    _inherit = "olims.common_report"

    rec_date_from = fields.Datetime(string='From')
    rec_date_to = fields.Datetime(string='to')
    analysis_state = fields.Selection(string="Analysis State",selection=AR_STATES)
    cancellation_state = fields.Selection(string="Cancellation State",selection=CACELL_STATES)
    worksheet_state = fields.Selection(string="Worksheet State",selection=WORKSHEET_STATES)
    client_id = fields.Many2one(string='Client',
        comodel_name='olims.client')


    @api.multi
    def pre_print_report(self, data):
        data['form'].update(self.read(['rec_date_from','rec_date_to', 'analysis_state', \
            'cancellation_state','worksheet_state','client_id'])[0])
        return data