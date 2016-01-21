
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Char(string='Label',required=True),
          
          )

class BatchLabel(models.Model, BaseOLiMSModel): 
    _name='olims.batch_label'
    _rec_name = 'Label'
    
BatchLabel.initialze(schema)
