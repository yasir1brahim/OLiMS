# -*- coding: utf-8 -*-

from openerp import fields, models


class OlimsAnalysespPerformedAndPublished(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.analyses_performed_pertotal_report'
	_description = 'Analyses performed and published as percentage of total'

	groupby = fields.Selection(string='Group By',
								selection=(('Day','Day'),
									('Week','Week'),
									('Month','Month'),
									('Year', 'Year'))
								)

	def _print_report(self, data):
		data['form'].update(self.read(['groupby'])[0])
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'olims.report_analysesperformedpertotal', data=data)