
from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel

schema = (fields.Char(string='Keyword', required=True),
          fields.Char(string='Field Title', required=True),
          fields.Char(string='Default value'),
          fields.Char(string='Unit'),
          fields.Boolean(string='Hidden Field'),
          fields.Boolean(string='Apply wide'),
          )

class InterimFieldServices(models.Model, BaseOLiMSModel): 
    _name='olims.interimfield'
    
InterimFieldServices.initialze(schema)