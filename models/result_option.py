
from openerp import fields, models
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.file_field import FileField
from fields.widget.widget import  DateTimeWidget, FileWidget, StringWidget
from base_olims_model import BaseOLiMSModel
from lims import bikaMessageFactory as _




schema = (fields.Many2one(string='service_resultoption_id', comodel_name='olims.analysis_service'),
          fields.Char(string='Result Value', required=True),
          fields.Char(string='Display Value', required=True),
          )

class ResultOption(models.Model, BaseOLiMSModel): 
    _name='olims.result_option'
    
ResultOption.initialze(schema)