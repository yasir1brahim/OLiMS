from openerp import fields, models, api

class MessageDialogBox(models.TransientModel):
    _name = "olims.message_dialog_box"

    title = fields.Char()

    @api.multi
    def cancel_analysis_requests(self):
        self.env['olims.analysis_request'].browse(self._context.get('active_ids', 
        	[])).signal_workflow("cancel")
        return True

    @api.multi
    def unlink(self):
        analysis_id = self._context.get('active_ids', [])[0]
        self.env["olims.add_analysis"].browse(analysis_id).write({"state": 'unassigned'})
        ws_add_analysis_obj = self.env["olims.worksheet"].search([("AnalysisRequest", '=', analysis_id)])
        ws_add_analysis_obj.write({"AnalysisRequest": [(3, analysis_id)]})
        if ws_add_analysis_obj.id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'olims.worksheet',
                'res_id': ws_add_analysis_obj.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target' : 'current',
            }