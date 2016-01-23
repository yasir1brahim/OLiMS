
from openerp import fields, models
from base_olims_model import BaseOLiMSModel


schema = (fields.Many2one(string='analysis_service_id', comodel_name='olims.analysis_service'),
          fields.Char(string='Range min', required=True),
          fields.Char(string='Range max', required=True),
          fields.Char(string='Uncertainty value', required=True),
          )

class UncertintyService(models.Model, BaseOLiMSModel): 
    _name='olims.uncertinty_service'
    
UncertintyService.initialze(schema)