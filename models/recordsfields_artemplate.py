from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from openerp.tools.translate import _

schema = (fields.Many2one(string='Services',
                   comodel_name='olims.analysis_service',
                   domain="[('category', '=', Category)]",
                   relation='recordfield_service'),
          fields.Boolean(string='Hidden',readonly=False),
          fields.Float(string='Price', default=0.00,compute='_ComputeServicePriceField'),
        fields.Many2one(string='Partition',
                  comodel_name='olims.partition_ar_template'),
        fields.Many2one(string='Category',
                    comodel_name='olims.analysis_category'),
          )
analysis_schema = (fields.Many2one(string='Priority',
                                   comodel_name='olims.ar_priority'),
                   fields.Many2one(string='Partition',
                                   comodel_name='olims.ar_partition'),
                   fields.Float(string="Error"),
                   fields.Float(string="Min"),
                   fields.Float(string="Max"),
                   fields.Many2one(string='analysis_request_id', comodel_name ='olims.analysis_request'),
                    fields.Integer(string='analysis_order', compute='calc_analysis_ordering', store= False),
                   )

class RecodrdsFieldARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.records_field_artemplates'

    @api.onchange('Services')
    def _ComputeServicePriceField(self):
        # set auto-changing field
        for item in self:
            if item.Services:
                item.Price = item.Services.Price
    @api.onchange('Services')
    def _OnChangeGetServiceHiddenField(self):
        # set auto-changing field
        if self.Services:
            self.Hidden = self.Services.Hidden
class ARAnalysis(models.Model, BaseOLiMSModel):
    _inherit = 'olims.records_field_artemplates'
    _name = 'olims.ar_analysis'

    @api.multi
    def show_delete_warring_message_form(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        form_id = ir_model_data.get_object_reference('olims', 'view_delete_message_dialog_box')[1]
        return {
            'name': _('Confirm'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'olims.message_dialog_box',
            'views': [(form_id, 'form')],
            'view_id': form_id,
            'target': 'new',
        }

    @api.onchange('Services')
    def set_min_max_values(self):
      for item in self:
        item.Min = item.Services.Min
        item.Max = item.Services.Max

    @api.depends("Services")
    def calc_analysis_ordering(self):
        count = 0
        self_records = []
        service_list = []
        for record in self:
            self_records.append(record)
        for record in self_records:
            for ap in record.analysis_request_id.AnalysisProfile:
                for ap_service in ap.Service:
                    service_list.append(ap_service.Services)
        for record in  service_list:
            for rec in self:
                if rec.Services.id == record.id:
                   count = count+1
                   rec.analysis_order = count
                   break
                else:
                    continue


RecodrdsFieldARTemplate.initialze(schema)
ARAnalysis.initialze(analysis_schema)