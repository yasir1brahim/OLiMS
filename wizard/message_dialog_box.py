from openerp import fields, models, api

class MessageDialogBox(models.TransientModel):
    _name = "olims.message_dialog_box"

    title = fields.Char()

    @api.multi
    def cancel_analysis_requests(self):
        self.env['olims.analysis_request'].browse(self._context.get('active_ids', 
        	[])).signal_workflow("cancel")
        return True