from openerp import fields, models

class PaymentTerm(models.Model): 
    _name='olims.payment_term'
    _rec_name = 'name'

    name = fields.Char("Payment Term")
