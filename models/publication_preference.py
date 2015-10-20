
from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel

schema = (fields.Char(string='name',required=True),
          
          )

class PublicationPreference(models.Model, BaseOLiMSModel): 
    _name='olims.publication_preference'
    
PublicationPreference.initialze(schema)
