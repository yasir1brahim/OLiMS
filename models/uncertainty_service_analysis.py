
from openerp import fields, models
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.file_field import FileField
from fields.widget.widget import  DateTimeWidget, FileWidget, StringWidget
from models.base_olims_model import BaseOLiMSModel
from lims import bikaMessageFactory as _




schema = (
          fields.Char(string='intercept_min', required=True),
          fields.Char(string='intercept_max', required=True),
          fields.Char(string='errorvalue', required=True),
          )

class UncertintyService(models.Model, BaseOLiMSModel): 
    _name='olims.uncertinty_service'
    
UncertintyService.initialze(schema)