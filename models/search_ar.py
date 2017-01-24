# worksheet search on analysis basis.

from openerp import models, fields, api
from openerp.tools.translate import _

class SerachWroksheet(models.TransientModel):
    _name = "olims.search_wroksheet"
    _rec_name = "selection_type"

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
    condition_type10 = fields.Selection([('=','='),('<','<'),('>','>'),('<=','<='),('>=','>=')], 'Condition', default='=')
    logical_cond = fields.Selection([('and','AND'),('or','OR')],'Logical Operator',default='or')
    analysis_service_ids10 = fields.Selection(_selection_services, string='Analysis')
    selection_type = fields.Selection(_selection_type, 'Search in', default='analysis')
    Result_field10 = fields.Char('Result')

    analysis_service_ids1 = fields.Selection(_selection_services, string='Analysis')
    condition_type1 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field1 = fields.Char('Result')

    analysis_service_ids2 = fields.Selection(_selection_services, string='Analysis')
    condition_type2 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field2 = fields.Char('Result')

    analysis_service_ids3 = fields.Selection(_selection_services, string='Analysis')
    condition_type3 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field3 = fields.Char('Result')

    analysis_service_ids4 = fields.Selection(_selection_services, string='Analysis')
    condition_type4 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field4 = fields.Char('Result')

    analysis_service_ids5 = fields.Selection(_selection_services, string='Analysis')
    condition_type5 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field5 = fields.Char('Result')

    analysis_service_ids6 = fields.Selection(_selection_services, string='Analysis')
    condition_type6 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field6 = fields.Char('Result')

    analysis_service_ids7 = fields.Selection(_selection_services, string='Analysis')
    condition_type7 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field7 = fields.Char('Result')

    analysis_service_ids8 = fields.Selection(_selection_services, string='Analysis')
    condition_type8 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field8 = fields.Char('Result')

    analysis_service_ids9 = fields.Selection(_selection_services, string='Analysis')
    condition_type9 = fields.Selection([('=', '='), ('<', '<'), ('>', '>'), ('<=', '<='), ('>=', '>=')], 'Condition',
                                      default='=')
    Result_field9 = fields.Char('Result')

    @api.multi
    def search_ar_data(self, **kw):
        data = self.read()[0]
        ids_list = []
        select_type = data['selection_type']
        logical_cond = data['logical_cond']
        work_sheetids = []
        ar_ids = []
        for x in range(1, 11):
            ws_id_list = []
            analysis_field = data['analysis_service_ids'+str(x)]
            if analysis_field==False:
                continue
            res = data['Result_field'+str(x)]
            condition_type = data['condition_type'+str(x)]

            if res:
                res_query_ws = ('result', condition_type, res)
                res_query_ar = ('Result', condition_type, res)
            else:
                res_query_ws = ('id','>',0)
                res_query_ar = ('id','>',0)
            if select_type =='worksheet':
                ids_list_ws_manage_res = self.env['olims.ws_manage_results'].search([
                    ('analysis', '=', int(analysis_field)), (res_query_ws)])
                ws_res_ids = []
                for item in ids_list_ws_manage_res:
                    ws_res_ids.append(item.id)
                ids_list_ws = self.env['olims.worksheet'].search([('ManageResult', 'in', ws_res_ids)])
                for ws_id in ids_list_ws:
                    ws_id_list.append(ws_id.id)
                work_sheetids.append(ws_id_list)
            else:
                ids_list_ws_ar_res = self.env["olims.manage_analyses"].search(["|",("Service","in",analysis_field)
                        ,("LabService","=",int(analysis_field)), res_query_ar])
                manage_analy_list = []
                for ar_id in ids_list_ws_ar_res:
                    manage_analy_list.append(ar_id.id)
                manage_analy_list
                ids_list_ar_res = self.env["olims.analysis_request"].search(["|",("Field_Manage_Result","in",manage_analy_list),("Lab_Manage_Result","in",manage_analy_list)])
                ar_ids = []
                for ids in ids_list_ar_res:
                    ar_ids.append(ids.id)
                work_sheetids.append(ar_ids)
        if logical_cond=='and':
            result = list(reduce(set.intersection, map(set, work_sheetids)))
        else:
            result = list(reduce(set.union, map(set, work_sheetids)))
        if select_type =='worksheet':
            if len(result) > 0:
                return{
                  'name':_('WorkSheets'),
                    'views': [[False, 'tree'],[False, "form"]],
                    'res_model': 'olims.worksheet',
                    'target': 'current',
                    'type': 'ir.actions.act_window',
                    'domain': [['id', 'in', result]],
                }
            else:
                return{
                    'views': [[False, "form"]],
                    'res_model': 'olims.search_wroksheet',
                    'type': 'ir.actions.act_window',
                    'target' : 'inline'
                    }
        else:
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