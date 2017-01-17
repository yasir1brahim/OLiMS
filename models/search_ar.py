# worksheet search on analysis basis.

from openerp import models, fields, api, netsvc

class SerachWroksheet(models.TransientModel):
    _name = "olims.search_wroksheet"

    @api.multi
    def _selection_services(self):
        list_of_name = []
        items_types_object = self.env['olims.analysis_service'].search([])
        for name in items_types_object:
            list_of_name.append((name.id,name.Service))
        return list_of_name

    @api.multi
    def _selection_type(self):
        list_of_name = [('analysis','Analysis Request'),('worksheet','Worksheet')]
        return list_of_name
    analysis_field = fields.Selection(_selection_services, 'Search in', default='', required=True)
    selection_type = fields.Selection(_selection_type, 'Search in', default='analysis', required=True)
    Result_field = fields.Char('Result')

    @api.multi
    def search_ar_data(self):
        data = self.read()[0]
        ids_list = []
        analysis_field = data['analysis_field']
        res_query = ('result_string','=',Result) if data['Result_field'] else ('id','>',0)
        if data['selection_type'] =='worksheet':
        	ids_list_ws_manage_res = self.env['olims.ws_manage_results'].search([('analysis', '=', int(analysis_field)),res_query])
	        ws_res_ids = []
	        for item in ids_list_ws_manage_res:
	        	ws_res_ids.append(item.id)
	        ids_list_ws = self.env['olims.worksheet'].search([('ManageResult', 'in', ws_res_ids )])
	        ws_id_list =[]
	        for ws_id in ids_list_ws:
	        	ws_id_list.append(ws_id.id)
	       	if len(ws_id_list) > 0:
	            return{
	                'views': [[False, 'tree'],[False, "form"]],
	                'res_model': 'olims.worksheet',
	                'type': 'ir.actions.act_window',
	                'domain': [['id', 'in', ws_id_list]],
	            }
	        else:
	            return{
	                'views': [[False, "form"]],
	                'res_model': 'olims.search_wroksheet',
	                'type': 'ir.actions.act_window',
	                'target' : 'inline'
	            }
        else:
	    	res_query = ('result_string','=',Result) if data['Result_field'] else ('id','>',0)
	    	ids_list_ws_ar_res = self.env["olims.manage_analyses"].search(["|",("Service","=",int(analysis_field))
                    ,("LabService","=",int(analysis_field)), res_query])

	    	manage_analy_list = []
	    	for ar_id in ids_list_ws_ar_res:
	        	manage_analy_list.append(ar_id.id)

	        manage_analy_list
	        ids_list_ar_res = self.env["olims.analysis_request"].search(["|",("Field_Manage_Result","in",manage_analy_list),("Lab_Manage_Result","in",manage_analy_list)])

	        ar_ids = []
	        for ids in ids_list_ar_res:
	        	ar_ids.append(ids.id)

	        if len(ar_ids) > 0:
	            return{
	                'views': [[False, 'tree'],[False, "form"]],
	                'res_model': 'olims.analysis_request',
	                'type': 'ir.actions.act_window',
	                'domain': [['id', 'in', ar_ids]],
	            }
	        else:
	            return{
	                'views': [[False, "form"]],
	                'res_model': 'olims.search_wroksheet',
	                'type': 'ir.actions.act_window',
	                'target' : 'inline'
	            }