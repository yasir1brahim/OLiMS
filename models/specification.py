from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.text_field import TextField
from fields.fixed_point_field import FixedPointField
schema = (fields.Many2one(string='Service',
                comodel_name='olims.analysis_service',
                domain="[('category', '=', Category)]"
#                 relation='analysis_service_specification'
    ),
    FixedPointField('Min'),
    FixedPointField('Max'),
    FixedPointField('< Min'),
    FixedPointField('> Max'),
    FixedPointField('Permitted Error'),
    TextField('Range Remarks'),
    fields.Many2one(string='Category',
                    comodel_name='olims.analysis_category',
                    ),
)

class Specifications(models.Model, BaseOLiMSModel):
    _name = "olims.specification"
    
Specifications.initialze(schema)