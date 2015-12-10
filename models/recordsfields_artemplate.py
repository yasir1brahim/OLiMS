from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel

schema = (fields.Many2one(string='Services',
                   comodel_name='olims.analysis_service',
                   relation='recordfield_service'),
          fields.Boolean(string='Hidden',readonly=False),
          fields.Float(string='Price', default=0.00,readonly=True),
        fields.Many2one(string='Partition',
                  comodel_name='olims.partition_ar_template'),
          )

class RecodrdsFieldARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.records_field_artemplates'

    @api.onchange('Services')
    def _onchange_service(self):
        # set auto-changing field
        if self.Services:
            self.Hidden = self.Services.Hidden
            self.Price = self.Services.Price

RecodrdsFieldARTemplate.initialze(schema)