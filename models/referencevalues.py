from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Many2one(string="Service",
                          comodel_name='olims.analysis_service',
                          domain="[('category', '=', Category)]"),
    fields.Many2one(comodel_name='olims.reference_sample', 
                    string='reference_sample_id', 
                    ondelete='cascade'),
    fields.Float(string="Expected Result"),
    fields.Float(string="Permitted Error"),
    fields.Float(string="Min"),
    fields.Float(string="Max"),
    fields.Many2one(string='Category',
                    comodel_name='olims.analysis_category'),
          )

class ReferenceValues(models.Model, BaseOLiMSModel): 
    _name='olims.reference_values'
    _rec_name = "Service"

ReferenceValues.initialze(schema)
