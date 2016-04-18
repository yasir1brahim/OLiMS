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

class pdf_template_db(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context): 
		super(pdf_template_db, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
			    'time': time,
			    'get_formatted_desc_db': self._get_formatted_desc_db
			})

	def _get_formatted_desc_db(self, desc):
		s = MLStripper()
		s.feed(desc)
		desc = s.get_data()
		return desc
		

class report_pdf_template_document(osv.AbstractModel):
    _name = 'report.labpal.pdf_db_template'
    _inherit = 'report.abstract_report'
    _template = 'labpal.pdf_db_template'
    _wrapped_report_class = pdf_template_db