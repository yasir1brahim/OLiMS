from openerp import fields, models,osv
from base_olims_model import BaseOLiMSModel

schema = (
          fields.Many2one(comodel_name='olims.country',string='Country', required=True),
          fields.Char(string='name', required=True),
          fields.Char(string='id', required=False),
          fields.Char(string='state_id', required=False),
          )

class State(models.Model, BaseOLiMSModel):
    _name='olims.state'
    _rec_name = 'name'
    
State.initialze(schema)
