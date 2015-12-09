
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Many2one(string='Sample Type', comodel_name='olims.sample_type'),
          fields.Boolean(string='Separate Container'),
          fields.Many2many(string='Preservation', comodel_name='olims.preservation'),
          fields.Many2many(string='Container', comodel_name='olims.container'),
          fields.Char(string='Required Volume'),
          )

class PartitionSetup(models.Model, BaseOLiMSModel): 
    _name='olims.partition_setup'
    
PartitionSetup.initialze(schema)