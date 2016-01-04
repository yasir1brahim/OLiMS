# -*- coding: utf-8 -*-

from openerp import fields, models


class OlimsDataEntryDayBook(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.data_entry_day_book'
	_description = 'Data entry day book'

	# print_date = fields.Date(string='Print Date')

	def _print_report(self, data):
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'OLiMS.report_dataentrydaybook', data=data)