# -*- coding: utf-8 -*-

from openerp import fields, models

class OlimsAnalysisPerServiceReport(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.analysis_per_service_report'
	_description = 'Analysis Per Service Report'

	client = fields.Many2one(string='Client',
		comodel_name='olims.client')

	def _print_report(self, data):
		data['form'].update(self.read(['client'])[0])
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'olims.report_analysisper_service', data=data)