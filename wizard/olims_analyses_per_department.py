# -*- coding: utf-8 -*-

from openerp import fields, models


class OlimsAnalysespPerDepartment(models.TransientModel):
	_inherit = "olims.common_olims_report"
	_name = 'olims.analyses_per_department_report'
	_description = 'Analyses summary per department'

	groupby = fields.Selection(string='Group By',
								selection=(('Day','Day'),
									('Week','Week'),
									('Month','Month'),
									('Year', 'Year'))
								)

	def _print_report(self, data):
		data['form'].update(self.read(['groupby'])[0])
		data = self.pre_print_report(data)
		return self.env['report'].get_action(self, 'OLiMS.report_analyses_per_department', data=data)