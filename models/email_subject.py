
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Char(string='name',required=True),
          
          )
email_schema = (
	fields.Char(string='name'),
	fields.Many2one(string="client_id",
		comodel_name="olims.client"),
	fields.Many2one(string="invoice_client_id",
		comodel_name="olims.client"))

class EmailSubject(models.Model, BaseOLiMSModel):
    _name='olims.email_subject'

class Email(models.Model, BaseOLiMSModel):
	_name="olims.email"
	_rec_name = "name"
    
EmailSubject.initialze(schema)
Email.initialze(email_schema)
