from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.text_field import TextField
from fields.fixed_point_field import FixedPointField
schema = (fields.Many2one(string='Service',
                comodel_name='olims.analysis_service',
#                 relation='analysis_service_specification'
    ),
    FixedPointField('Min'),
    FixedPointField('Max'),
    FixedPointField('< Min'),
    FixedPointField('> Max'),
    FixedPointField('Permitted Error'),
    TextField('Range remarks:'),
)

class Specifications(models.Model, BaseOLiMSModel):
    _name = "olims.specification"
    
Specifications.initialze(schema)