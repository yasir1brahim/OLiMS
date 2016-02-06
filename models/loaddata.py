from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from openerp import _
from openerp.exceptions import Warning



class LoadData(models.Model): 
    _name='olims.loaddata'

    demo = fields.Boolean(string='Demo')
    select_data = fields.Selection(string='Select existing file',
    	selection=(('setupdata','OLiMS:Demo Data'),),
    	default='setupdata',
    	required=True,
    	select=True)

    def load_demo_data(self,cr,uid,ids,context=None):
        module_object = self.pool.get('ir.module.module')
        users_login_obj = self.pool.get('olims.users_login_detail')
        users_data_ids = users_login_obj.search(cr, uid, [], context=None)
        module_obj = module_object.search(cr, uid, [('name', '=', 'olims')], context=None)
        for values in module_object.browse(cr, uid, module_obj, context=None):
        	if values.demo == False:
        		module_object.write(cr, uid, module_obj, {'demo':True}, context=None)
        		module_object.button_immediate_upgrade(cr, uid, module_obj, context=None)
        		# module_object.write(cr, uid, module_obj, {'demo':False}, context=None)

        	else:
        		raise Warning(_('Data is already loaded.'))

        # print 'asdf'

    @api.model
    def create(self, values):
    	self.search([('id', '>', 0)]).unlink()
    	values.update({'demo':True})
    	res = super(LoadData, self).create(values)
    	return res

class UserLoginDetail(models.Model):
	_name = 'olims.users_login_detail'

	login_user = fields.Char('Login ID')
	login_password = fields.Char('Password')

