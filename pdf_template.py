from openerp.osv import osv
from openerp.report import report_sxw
import logging
import re
import time
from HTMLParser import HTMLParser



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class pdf_template(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context): 
		super(pdf_template, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
			    'time': time,
			    'get_formatted_desc': self._get_formatted_desc
			})

	def _get_formatted_desc(self, desc):
		s = MLStripper()
		s.feed(desc)
		desc = s.get_data()
		return desc
	
		

class report_pdf_template_document(osv.AbstractModel):
    _name = 'report.olims.labpal_experiment_template'
    _inherit = 'report.abstract_report'
    _template = 'olims.labpal_experiment_template'
    _wrapped_report_class = pdf_template