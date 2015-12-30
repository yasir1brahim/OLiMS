# -*- coding: utf-8 -*-

from openerp import fields, models

class OlimsAnalysisPerSampleTypeReport(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.analysis_per_sample_type_report'
	_description = 'Analysis Per Sample Type Report'

	client = fields.Many2one(string='Client',
		comodel_name='olims.client')

	def _print_report(self, data):
		data['form'].update(self.read(['client'])[0])
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'OLiMS.report_analysisper_sample_type', data=data)