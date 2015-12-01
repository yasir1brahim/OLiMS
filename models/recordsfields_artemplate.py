from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Many2many(string='Services Analysis',
                   comodel_name='olims.analysis_service',
                   relation='recordfield_service'),
          fields.Boolean(string='Hidden'),
          fields.Float(string='Price', default=0.00),
        fields.Many2one(string='Partition',
                  comodel_name='olims.partition_ar_template'),
          )

class RecodrdsFieldARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.records_field_artemplates'
    
RecodrdsFieldARTemplate.initialze(schema)