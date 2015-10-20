
from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel

schema = (fields.Char(string='name',required=True),
          
          )

class EmailSubject(models.Model, BaseOLiMSModel): 
    _name='olims.email_subject'
    
EmailSubject.initialze(schema)
