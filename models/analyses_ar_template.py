
from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel

schema = (
          fields.One2many(string='service_uid', comodel_name ='olims.analysis_service'),
          fields.One2many(string='service_uid', comodel_name ='olims.analysis_service'),
          fields.Char(string='service_uid', required=True),
          fields.Char(string='partition', required=True),
          )

class PartitionARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.partition_ar_template'
    
PartitionARTemplate.initialze(schema)