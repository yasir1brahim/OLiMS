from openerp import fields, models,osv,api
from base_olims_model import BaseOLiMSModel

schema = (
          fields.Char(string='username'),
          fields.Char(string='email', required=True),
          fields.Char(string='password', required=True),
          )

class Templogin(models.Model, BaseOLiMSModel):
    _name='olims.templogin'

    @api.multi
    def open_temp_login_confirm_dialog(self, **kw):
        view_id = self.env['ir.ui.view'].search([('name', '=', 'Temp Login Confirmation')])
        context = self.env.context.copy()

        contact_id = context['contact_id']
        contact_obj = self.env['olims.contact'].search([('id', '=', contact_id)])
        data = self.read()[0]
        values = {}
        values['name'] = contact_obj.name
        values['login'] = data['email']
        values['password'] = data['password']
        values['client_id'] = contact_obj.Client_Contact.id
        values['contact_id'] = contact_id

        context.update(
            {'temp_login_name': data['username'], 'temp_login': data['email'], 'temp_login_password': data['password'], \
             'temp_login_client': contact_obj.Client_Contact.id, 'temp_login_contact': contact_id})
        return {
            'name': ('Confirmation'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'olims.message_dialog_box',
            'view_id': [view_id.id],
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': context,
        }

    @api.multi
    def create_temp_login(self, **kw):
        context = self.env.context.copy()
        data = self.read()[0]
        values = {}
        values.update({'temp_login_name': data['username'] ,'temp_login': data['email'],'temp_login_password': \
            data['password'], 'temp_login_client': context.get('client_id'), 'temp_login_contact': \
            context.get('contact_id')})
        return self.env['olims.message_dialog_box'].create_temp_login(values)


Templogin.initialze(schema)
