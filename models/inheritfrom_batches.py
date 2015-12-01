from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField

schema = (StringField('name',
              required=0,        
    ),
    StringField('ObjectId',
    ),
    StringField('Description',
    ),
)

class InheritFromBatch(models.Model, BaseOLiMSModel):
    _name = 'olims.inherit_from_batch'
    
InheritFromBatch.initialze(schema)