
from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel

schema = (
          fields.Many2one(string='Container', comodel_name ='olims.container'),
          fields.Many2one(string='Preservation', comodel_name ='olims.preservation'),
          fields.Char(string='Partition'),
          )

class PartitionARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.partition_ar_template'
    
PartitionARTemplate.initialze(schema)