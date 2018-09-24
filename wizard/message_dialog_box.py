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
    def bulk_verify_analysis_requests(self):
        active_ids = self._context.get('active_ids', [])
        self.env['olims.analysis_request'].bulk_verify_request(context=self.env.context, ids_to_verify=active_ids)
        return True


    @api.multi
    def publish_analysis_request(self):
        active_ids = self._context.get('active_ids', [])
        self.env['olims.analysis_request'].browse(active_ids).signal_workflow('publish')
        return True

    @api.multi
    def send_ar_COA(self):
        active_ids = self._context.get('active_ids', [])
        return self.env['olims.analysis_request'].browse(active_ids).action_report_send()



    @api.multi
    def unlink(self):
	try:
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
	except:
		pass

    @api.multi
    def unlink_analyses_of_ar(self):
        analysis_id = self._context.get('active_ids', [])[0]
        ar_analysis_obj = self.env["olims.ar_analysis"].browse(analysis_id)
        analysis_request_obj = self.env["olims.analysis_request"].search([("Analyses", '=', analysis_id)])
        for record in ar_analysis_obj:
            manage_result_services = self.env['olims.manage_analyses'].search(["|",
                ("Service", "=", record.Services.id), ("LabService", "=", record.Services.id),
                "|",("manage_analysis_id", "=", analysis_request_obj.id),
                ("lab_manage_analysis_id", "=", analysis_request_obj.id)])

            add_analysis_obj = self.env["olims.add_analysis"].search([("analysis", "=", record.Services.id),
                ("add_analysis_id", "=", analysis_request_obj.id)])

            ws_manage_results_obj = self.env["olims.ws_manage_results"].search([("analysis", "=", record.Services.id),
                ("request_analysis_id", "=", analysis_request_obj.id)])

            ws_manage_results_obj.unlink()
            manage_result_services.unlink()
            add_analysis_obj.unlink()
        ar_analysis_obj.unlink()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'olims.analysis_request',
            'res_id': analysis_request_obj.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target' : 'current',
        }
    @api.multi
    def create_temp_login(self, value_dict=None):
        values = {}
        if value_dict is None:
            context = self._context
            values['name'] = context['temp_login_name']
            values['login'] = context['temp_login']
            values['password'] = context['temp_login_password']
            values['client_id'] =  context['temp_login_client']
            values['contact_id'] =  context['temp_login_contact']
        else:
            values['name'] = value_dict['temp_login_name']
            values['login'] = value_dict['temp_login']
            values['password'] = value_dict['temp_login_password']
            values['client_id'] = value_dict['temp_login_client']
            values['contact_id'] = value_dict['temp_login_contact']
        res_user = self.env["res.users"]
        old_client_user = res_user.search([('contact_id', '=', values['contact_id']), ('client_id', '=',\
                                                                                            values['client_id'])])
        if old_client_user:
            old_client_user.unlink()

        res = res_user.create(values)
        res_groups = self.env['res.groups']
        group = res_groups.search([('name', '=', 'Clients')])
        group.write({'users': [(4, res.id)]})
        contact_user = self.env["olims.contact"]
        contact_object = contact_user.search([('id', '=', values['contact_id'])])
        contact_object.write({"user": res.id})
        return res

