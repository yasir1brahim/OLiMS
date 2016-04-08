from openerp import fields, models,osv
from base_olims_model import BaseOLiMSModel

schema = (
          fields.Many2one(comodel_name='olims.country',string='Country', required=True),
          fields.Many2one(comodel_name='olims.state',string='State',domain="[('Country', '=', Country)]", required=True),
          fields.Char(string='name', required=True),
          )

class District(models.Model, BaseOLiMSModel):
    _name='olims.district'
    
District.initialze(schema)
