
from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel

schema = (
          fields.Char(string='Partition', required=True),
          fields.Char(string='Container', required=True),
          fields.Char(string='Preservation', required=True),
          )

class PartitionARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.partition_ar_template'
    
PartitionARTemplate.initialze(schema)