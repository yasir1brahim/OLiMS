
from openerp import fields, models
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.file_field import FileField
from fields.widget.widget import  DateTimeWidget, FileWidget, StringWidget
from base_olims_model import BaseOLiMSModel
from lims import bikaMessageFactory as _




schema = (fields.Many2one(string='analysis_service_id', comodel_name='olims.analysis_service'),
          fields.Char(string='Range min', required=True),
          fields.Char(string='Range max', required=True),
          fields.Char(string='Uncertainty value', required=True),
          )

class UncertintyService(models.Model, BaseOLiMSModel): 
    _name='olims.uncertinty_service'
    
UncertintyService.initialze(schema)