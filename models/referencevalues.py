from openerp import fields, models
from base_olims_model import BaseOLiMSModel
import logging
_logger = logging.getLogger(__name__)

schema = (fields.Many2one(string="Service",
                          comodel_name='olims.analysis_service'),
    fields.Many2one(comodel_name='olims.reference_sample', 
                    string='reference_sample_id', 
                    ondelete='cascade'),
    fields.Integer(string="Expected Result"),
    fields.Integer(string="Permitted Error"),
    fields.Integer(string="Min"),
    fields.Integer(string="Max"),
          )

class ReferenceValues(models.Model, BaseOLiMSModel): 
    _name='olims.reference_values'
    _rec_name = "Service"

ReferenceValues.initialze(schema)
