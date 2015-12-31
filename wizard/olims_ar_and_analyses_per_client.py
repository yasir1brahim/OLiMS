# -*- coding: utf-8 -*-

from openerp import fields, models

class OlimsAnalysisRequestAndAnalysisPerClient(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.ar_and_analysis_per_client_report'
	_description = 'Analysis requests and analyses per client'

	client = fields.Many2one(string='Client',
		comodel_name='olims.client')

	def _print_report(self, data):
		data['form'].update(self.read(['client'])[0])
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'OLiMS.report_ar_and_analyses_per_client', data=data)