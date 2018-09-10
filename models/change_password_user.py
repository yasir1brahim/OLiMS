from openerp import fields, models, api


class change_password_user(models.TransientModel):
    _inherit = "change.password.user"

    """
    over riding odoo base's model definition to change ondelete=cascade for user_id column, as it not working by the \
    base's class definition and we need to put it in our custom module. 
    
    """
    user_id = fields.Many2one('res.users', string='User', required=1, ondelete='cascade')