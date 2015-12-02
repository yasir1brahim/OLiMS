
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Char(string='name',required=True),
          
          )

class BatchLabel(models.Model, BaseOLiMSModel): 
    _name='olims.batch_label'
    
BatchLabel.initialze(schema)
