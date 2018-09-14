"""Client - the main organisational entity in bika.
"""

from openerp import fields, models, osv, api

from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.reference_field import ReferenceField
from fields.boolean_field import BooleanField
from fields.text_field import TextField
from fields.widget.widget import  TextAreaWidget, ReferenceWidget, StringWidget, BooleanWidget
from openerp.tools.translate import _
EMAIL_SUBJECT_OPTIONS = (
    ('ar', _('Analysis Request ID')),
    ('co', _('Order ID')),
    ('cr', _('Client Reference')),
    ('cs', _('Client SID')),
)
schema = (

    StringField('Name',
        required = 1,
        searchable = True,
        validators = ('uniquefieldvalidator',),
        widget = StringWidget(
            label=_("Name"),
        ),
    ),
    StringField('TaxNumber',
        widget = StringWidget(
            label=_("VAT number"),
        ),
    ),
    StringField('Phone',
        widget = StringWidget(
            label=_("Phone"),
        ),
    ),
    StringField('Fax',
        widget = StringWidget(
            label=_("Fax"),
        ),
    ),
    fields.One2many(string="email",
        comodel_name="olims.email",
        inverse_name="client_id",
        ),
    fields.One2many(string="invoice_email",
        comodel_name="olims.email",
        inverse_name="invoice_client_id",
        ),
          # # ~~~~~~~~~~ PhysicalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='physical_country',default=lambda self: self.env['olims.country'].search([('name','=','United States')]).id),
    fields.Many2one(comodel_name='olims.state',string='physical_state', domain="[('Country', '=', physical_country)]",default=lambda self: self.env['olims.state'].search([('name','=','Washington')]).id),
    fields.Many2one(comodel_name='olims.district',string='physical_district', domain="[('State', '=', physical_state)]"),
    fields.Char(string='physical_city'),
    fields.Char(string='physical_postalcode'),
    fields.Char(string='physical_address'),
    fields.Selection([('postal', 'PostalAddress'),('billing','BillingAddress')],string='physical_copy_from'),
           
          
          # # ~~~~~~~~~~ PostalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='postal_country',default=lambda self: self.env['olims.country'].search([('name','=','United States')]).id),
    fields.Many2one(comodel_name='olims.state',string='postal_state', domain="[('Country', '=', postal_country)]",default=lambda self: self.env['olims.state'].search([('name','=','Washington')]).id),
    fields.Many2one(comodel_name='olims.district',string='postal_district', domain="[('State', '=', postal_state)]"),
    fields.Char(string='postal_city'),
    fields.Char(string='postal_postalcode'),
    fields.Char(string='postal_address'),
    fields.Selection([('physical', 'PhysicalAddress'),('billing','BillingAddress')],string='postal_copy_from'),
          
          
       # # ~~~~~~~~~~ BillingAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='billing_country',default=lambda self: self.env['olims.country'].search([('name','=','United States')]).id),
    fields.Many2one(comodel_name='olims.state',string='billing_state', domain="[('Country', '=', billing_country)]",default=lambda self: self.env['olims.state'].search([('name','=','Washington')]).id),
    fields.Many2one(comodel_name='olims.district',string='billing_district', domain="[('State', '=', billing_state)]"),
    fields.Char(string='billing_city'),
    fields.Char(string='billing_postalcode'),
    fields.Char(string='billing_address'),
    fields.Selection([('physical','PhysicalAddress'),('postal', 'PostalAddress')],string='billing_copy_from'),
        
    StringField('AccountType',
        schemata = 'Bank details',
        widget = StringWidget(
            label=_("Account Type"),
        ),
    ),
    StringField('AccountName',
        schemata = 'Bank details',
        widget = StringWidget(
            label=_("Account Name"),
        ),
    ),
    StringField('AccountNumber',
        schemata = 'Bank details',
        widget = StringWidget(
            label=_("Account Number"),
        ),
    ),
    StringField('BankName',
        schemata = 'Bank details',
        widget = StringWidget(
            label=_("Bank name"),
        ),
    ),
    StringField('BankBranch',
        schemata = 'Bank details',
        widget = StringWidget(
            label=_("Bank branch"),
        ),
    ),


    StringField('ClientID',
        required=1,
        searchable = True,
        #validators = ('uniquefieldvalidator', 'standard_id_validator'),
        widget=StringWidget(
            label=_('Client ID'),
            description=_('ClientID is required.'),
        ),
    ),

    BooleanField('BulkDiscount',
        default = False,
        #write_permission = ManageClients,
        widget = BooleanWidget(
            label=_("Bulk discount applies"),
        ),
    ),

    BooleanField('MemberDiscountApplies',
        default = False,
        #write_permission = ManageClients,
        widget = BooleanWidget(
            label=_("Member discount applies"),
        ),
    ),
          
        
    
    fields.Selection(string='EmailSubject',
                   selection=EMAIL_SUBJECT_OPTIONS,
                   required=False,
                   help="Items to be included in email subject lines",
    #               schemata = 'Preferences',
                   default = 'ar',
    ),


    fields.Many2many(string='DefaultCategories',
                   comodel_name='olims.analysis_category',
#                    schemata="Method",
                   required=False,
                   help="Always expand the selected categories in client views",
    ),

    fields.Many2many(string='RestrictedCategories',
                   comodel_name='olims.analysis_category',
#                    schemata="Method",
                   required=False,
                   help="Show only selected categories in client views",
    ),
    fields.Selection(string='DefaultARSpecs',
        selection=( ('ar_specs', 'Analysis Request Specifications'),
                                 ('lab_sampletype_specs', 'Sample Type Specifications (Lab)'),
                                 ('client_sampletype_specs', 'Sample Type Specifications (Client)')),
        help="DefaultARSpecs_description",
    #     schemata = "Preferences",
        default = 'ar_specs',
     ),

    BooleanField('DefaultDecimalMark',
        default = True,
        #write_permission = ManageClients,
         widget = BooleanWidget(
            label=_("Default decimal mark"),
            description=_("The decimal mark selected in Bika Setup will be used."),
        ),
    ),



    fields.Selection(string='DecimalMark',
         selection=(
                    ('.', _('Dot (.)')),
                    (',', _('Comma (,)')),
                                    ),
         help="Decimal mark to use in the reports from this Client.",
    #     schemata = "Preferences",
         default = '.',
     ),
    fields.One2many('olims.analysis_request',
                                 'Client',
                                 string='Analysis_Request',
                                 domain=[('state','!=','pre_enter')]
    ),
    fields.One2many('olims.contact',
                                 'Client_Contact',
                                 string='Contact'
    ),
    fields.One2many('olims.analysis_spec',
                                 'ClientUID',
                                 string='Analysis Specification'
    ),
    fields.Many2many('olims.analysis_profile',
                                 # 'ClientProfile',
                                 string='Analysis_Profile',
                                 domain="[('Deactivated', '=', False)]"
    ),
    fields.One2many('olims.sample_point',
                                 'ClientSamplePoint',
                                 string='Sample Point'
    ),
    fields.One2many('olims.ar_template',
                                 'ClientARTemplate',
                                 string='AR Template'
    ),
    fields.One2many('olims.sr_template',
                                 'ClientSRTemplate',
                                 string='SR Template'
    ),
    fields.One2many('olims.supply_order',
                                 'Client',
                                 string='Supply Order'
    ),
    fields.One2many('olims.sample',
                                 'Client',
                                 string='Sample',
                                 domain=[('state','!=','pre_enter')]
    ),
    fields.One2many('res.users',
                                 'client_id',
                                 string='login_details',
                    ),
    BooleanField(string="payment_not_current",
        default=False),
    fields.Float(string='M_Discount',
        default=0.00
    ),
    fields.Float(string='Invoice_Discount',
        default=0.00
    ),

    BooleanField(string="Copy_Active_AProfiles",
            default = True
    ),
    BooleanField(string='is_client_user',
                compute='check_client_group',
                ),

)

class Client(models.Model, BaseOLiMSModel):
    _name='olims.client'
    _rec_name = 'Name'



    def action_bring_form_view(self,cr, uid,context):
        ir_model_data = self.pool.get('ir.model.data')
        form_id = ir_model_data.get_object_reference(cr, uid, 'olims', 'olims_client_form_view')[1]
        client = self.pool.get('olims.client')
        client_id = client.search(cr, uid,[])[0]

        return {
            'name': _('Confirm'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'olims.client',
            'res_id':client_id,
            'views': [(form_id, 'form')],
            'view_id': form_id,
            'target': 'current',

        }
    @api.onchange('login_details')
    def onchange_login_details(self):
        previous_contacts = []
        for record in self.login_details:
            if type(record.id) == int:
                previous_contacts.append(record.contact_id.id)
            if type(record.id)!= int:
                if record.contact_id.id not in previous_contacts:
                    pass
                elif record.contact_id.id in previous_contacts:
                    title = 'Duplicate Contact!'
                    message = 'Previous User for '+ record.contact_id.Firstname+ ' will be removed from system after save button is clicked'
                    return {

                        'warning': {

                            'title': title,

                            'message':message}

                    }



    @api.onchange('Copy_Active_AProfiles')
    def assign_all_active_profiles_to_client(self, cr, uid, context):
        if context.get('val_Copy_Active_AProfiles'):
            client_id =context.get('id')
            activatd_aprofile_ids = self.pool.get('olims.analysis_profile').search(cr, uid,
                                                                                  [('Deactivated', '=', False)])
            activatd_aprofile_ids_copy = activatd_aprofile_ids[:]
            query = "select olims_analysis_profile_id from  olims_analysis_profile_olims_client_rel where olims_client_id"\
                    "="+str(client_id)
            cr.execute(query)
            assigned_profiles = cr.fetchall()

            for id in assigned_profiles:
                if id[0] in activatd_aprofile_ids:
                    activatd_aprofile_ids.remove(id[0])

            if activatd_aprofile_ids:
                if assigned_profiles:
                    query = "delete from olims_analysis_profile_olims_client_rel where olims_client_id ="+str(client_id)
                    cr.execute(query)

                query = "insert into olims_analysis_profile_olims_client_rel values "
                values = []
                for id in activatd_aprofile_ids_copy :
                    values.append("({0},{1})".format(client_id, id))

                query+= ",".join(value for value in values)
                cr.execute(query)

            else:
                return {

                    'warning': {

                        'title': 'Warning!',

                        'message': 'All Active profiles are already assigned !'}

                }

    @api.onchange('physical_copy_from')
    def _onchange_physical(self):
        # set auto-changing field
        if self.physical_copy_from:
            setattr(self, 'physical_country', getattr(self,self.physical_copy_from+'_country'))
            setattr(self, 'physical_state', getattr(self,self.physical_copy_from+'_state'))
            setattr(self, 'physical_district', getattr(self,self.physical_copy_from+'_district'))
            setattr(self, 'physical_city', getattr(self,self.physical_copy_from+'_city'))
            setattr(self, 'physical_postalcode', getattr(self,self.physical_copy_from+'_postalcode'))
            setattr(self, 'physical_address', getattr(self,self.physical_copy_from+'_address'))

    @api.onchange('postal_copy_from')
    def _onchange_postal(self):
        # set auto-changing field
        if self.postal_copy_from:
            setattr(self, 'postal_country', getattr(self,self.postal_copy_from+'_country'))
            setattr(self, 'postal_state', getattr(self,self.postal_copy_from+'_state'))
            setattr(self, 'postal_district', getattr(self,self.postal_copy_from+'_district'))
            setattr(self, 'postal_city', getattr(self,self.postal_copy_from+'_city'))
            setattr(self, 'postal_postalcode', getattr(self,self.postal_copy_from+'_postalcode'))
            setattr(self, 'postal_address', getattr(self,self.postal_copy_from+'_address'))

    @api.onchange('billing_copy_from')
    def _onchange_billing(self):
        # set auto-changing field
        if self.billing_copy_from:
            print "billing running"
            setattr(self, 'billing_country', getattr(self,self.billing_copy_from+'_country'))
            setattr(self, 'billing_state', getattr(self,self.billing_copy_from+'_state'))
            setattr(self, 'billing_district', getattr(self,self.billing_copy_from+'_district'))
            setattr(self, 'billing_city', getattr(self,self.billing_copy_from+'_city'))
            setattr(self, 'billing_postalcode', getattr(self,self.billing_copy_from+'_postalcode'))
            setattr(self, 'billing_address', getattr(self,self.billing_copy_from+'_address'))

    @api.model
    def create(self, values):
        res = super(Client, self).create(values)
        activatd_Aprfile_ids = self.pool.get('olims.analysis_profile').search(self.env.cr, self.env.uid,
                                                                              [('Deactivated', '=', False)])

        values = []

        if activatd_Aprfile_ids:
            for id in activatd_Aprfile_ids:
                values.append("(" + str(res.id) + "," + str(id) + ")")
            query = "insert into olims_analysis_profile_olims_client_rel values "+",".join(value for value  in values)
            self.env.cr.execute(query)
        return res

    @api.multi
    def write(self,vals):
        res = super(Client, self).write(vals)
        if vals.get('login_details'):
            for val in vals.get('login_details'):
                if val[0] == 0:
                    res_groups = self.env['res.groups']
                    client_group = res_groups.search([('name', '=', 'Clients')])
                    client_users = self.env['res.users'].search(
                        [('client_id', '=', self.id), ('groups_id', 'not in', [client_group.id])])
                    user_ids = []
                    for object in client_users:
                        user_ids.append(object.id)
                    client_group.write({'users': [(4, user_ids)]})
                    contact_user = self.env["res.users"].search([('contact_id', '=', val[2].get('contact_id'))], order='id DESC', limit=2)
                    #limit set to 2 , first one will be newly added user, and second user in descending order will be previous user
                    if len(contact_user)>1:
                        contact_user[1].unlink() # delete previous user
                        contact = self.env["olims.contact"]
                        contact_object = contact.search([('id', '=', val[2].get('contact_id'))])
                        contact_object.write({"user": contact_user[0].id}) # set newly added user in contact
                    elif len(contact_user) == 1:
                        contact = self.env["olims.contact"]
                        contact_object = contact.search([('id', '=', val[2].get('contact_id'))])
                        contact_object.write({"user": contact_user[0].id})  # set newly added user in contact

        return res

    def unlink(self):
        for contact_record in self.Contact:
            contact_record.unlink()
        return super(Client, self).unlink()

    @api.model
    def _get_value_cash_as_default(self):
        payment_term_obj= self.env["olims.payment_term"]
        cash_value = payment_term_obj.search([("name", "=ilike", "Cash")], limit=1)
        if cash_value:
            return cash_value[0].id
        return False

    @api.multi
    def check_client_group(self):
        for record in self:
            if self.env.user.has_group('olims.group_clients'):
                record.is_client_user = True



    payment_term_id = fields.Many2one(string="Payment Terms",
        comodel_name="olims.payment_term", default=_get_value_cash_as_default)

Client.initialze(schema)
