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
    StringField('Email Address',
        schemata = 'Address',
        widget = StringWidget(
            label=_("Email Address"),
        ),
        validators = ('isEmail',)
    ),
          # # ~~~~~~~~~~ PhysicalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='physical_country',default=lambda self: self.env['olims.country'].search([('name','=','United States')]).id),
    fields.Many2one(comodel_name='olims.state',string='physical_state', domain="[('Country', '=', physical_country)]"),
    fields.Many2one(comodel_name='olims.district',string='physical_district', domain="[('State', '=', physical_state)]"),
    fields.Char(string='physical_city'),
    fields.Char(string='physical_postalcode'),
    fields.Char(string='physical_address'),
    fields.Selection([('postal', 'PostalAddress'),('billing','BillingAddress')],string='physical_copy_from'),
           
          
          # # ~~~~~~~~~~ PostalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='postal_country',default=lambda self: self.env['olims.country'].search([('name','=','United States')]).id),
    fields.Many2one(comodel_name='olims.state',string='postal_state', domain="[('Country', '=', postal_country)]"),
    fields.Many2one(comodel_name='olims.district',string='postal_district', domain="[('State', '=', postal_state)]"),
    fields.Char(string='postal_city'),
    fields.Char(string='postal_postalcode'),
    fields.Char(string='postal_address'),
    fields.Selection([('physical', 'PhysicalAddress'),('billing','BillingAddress')],string='postal_copy_from'),
          
          
       # # ~~~~~~~~~~ BillingAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='billing_country',default=lambda self: self.env['olims.country'].search([('name','=','United States')]).id),
    fields.Many2one(comodel_name='olims.state',string='billing_state', domain="[('Country', '=', billing_country)]"),
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
                                 string='Analysis_Request'
    ),
    fields.One2many('olims.contact',
                                 'Client_Contact',
                                 string='Contact'
    ),
    fields.One2many('olims.analysis_spec',
                                 'ClientUID',
                                 string='Analysis Specification'
    ),
    fields.One2many('olims.analysis_profile',
                                 'ClientProfile',
                                 string='Analysis Profile'
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
                                 string='Sample'
    ),

)

class Client(models.Model, BaseOLiMSModel):
    _name='olims.client'
    _rec_name = 'Name'

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

Client.initialze(schema)
