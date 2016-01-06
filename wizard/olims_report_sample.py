# -*- coding: utf-8 -*-

from openerp import fields, models


class OlimsSampleReport(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.sample_report'
	_description = 'Sample Report'

	print_date = fields.Date(string='Print Date')

	def _print_report(self, data):
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'olims.report_sample', data=data)