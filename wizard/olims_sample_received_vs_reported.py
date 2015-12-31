# -*- coding: utf-8 -*-

from openerp import fields, models


class OlimsSampleReceivedvsReported(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.sample_received_vs_reported'
	_description = 'Sample Received vs Reported'

	printed_date = fields.Datetime(string='Printed Date')

	def _print_report(self, data):
		data['form'].update(self.read(['printed_date'])[0])
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'OLiMS.report_sample_received_vs_reported', data=data)