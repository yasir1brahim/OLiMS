# worksheet search on analysis basis.

from openerp import models, fields, api
from openerp.tools.translate import _

class SerachWroksheet(models.TransientModel):
    _name = "olims.search_wroksheet"
    _rec_name = "selection_type"

    @api.multi
    def _selection_type(self):
        list_of_name = [('analysis','Analysis Request'),('worksheet','Worksheet')]
        return list_of_name
    analysis_service_ids = fields.Many2many(comodel_name="olims.analysis_service", string='Search in', required=True)
    selection_type = fields.Selection(_selection_type, 'Search in', default='analysis', required=True)
    Result_field = fields.Char('Result')

    @api.multi
    def search_ar_data(self):
        data = self.read()[0]
        ids_list = []
        analysis_field = data['analysis_service_ids']
        if data['Result_field']:
        	if data['Result_field'].find('>') >= 0:
        		result_val = float(data['Result_field'].split(">")[1])
        		res_query_ws = ('result','>', result_val)
        		res_query_ar = ('Result','>', result_val)
        	elif data['Result_field'].find('<') >= 0:
        		result_val = float(data['Result_field'].split("<")[1])
        		res_query_ws = ('result','<', result_val)
        		res_query_ar = ('Result','<', result_val)
        	else:
        		result_val = float(data['Result_field'])
        		res_query_ws = ('result','=', result_val)
        		res_query_ar = ('Result','=', result_val)
        else:
        	res_query_ws = ('id','>',0)
        	res_query_ar = ('id','>',0)
        if data['selection_type'] =='worksheet':
        	ids_list_ws_manage_res = self.env['olims.ws_manage_results'].search([
        		('analysis', 'in', analysis_field),res_query_ws])
	        ws_res_ids = []
	        for item in ids_list_ws_manage_res:
	        	ws_res_ids.append(item.id)
	        ids_list_ws = self.env['olims.worksheet'].search([('ManageResult', 'in', ws_res_ids )])
	        ws_id_list =[]
	        for ws_id in ids_list_ws:
	        	ws_id_list.append(ws_id.id)
	       	if len(ws_id_list) > 0:
	            return{
	            	'name':_('WorkSheets'),
	                'views': [[False, 'tree'],[False, "form"]],
	                'res_model': 'olims.worksheet',
	                'target': 'current',
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
	    	ids_list_ws_ar_res = self.env["olims.manage_analyses"].search(["|",("Service","in",analysis_field)
                    ,("LabService","in",analysis_field), res_query_ar])

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
	            	'name':_('Analysis Requests'),
	                'views': [[False, 'tree'],[False, "form"]],
	                'res_model': 'olims.analysis_request',
	                'target': 'current',
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