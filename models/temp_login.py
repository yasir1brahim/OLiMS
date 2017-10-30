from openerp import fields, models,osv,api
from base_olims_model import BaseOLiMSModel

schema = (
          fields.Char(string='username', required=True),
          fields.Char(string='email', required=True),
          fields.Char(string='password', required=True),
          )

class Templogin(models.Model, BaseOLiMSModel):
    _name='olims.templogin'
    

    @api.multi
    def create_res_user(self, **kw):
    	context = self._context
    	contact_id = context['contact_id']
    	data = self.read()[0]
    	values = {}
    	values['name'] = data['username']
        values['login'] = data['email']
        values['password'] = data['password']
        res_user = self.env["res.users"]
        res = res_user.create(values)
        res_groups = self.env['res.groups']
        group = res_groups.search([('name', '=','Clients')])
        group.write({'users': [(4, res.id)]})
        contact_user = self.env["olims.contact"]
        contact_object = contact_user.search([('id', '=',contact_id)])
        contact_object.write({"user":res.id})


Templogin.initialze(schema)
