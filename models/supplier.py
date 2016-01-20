# # ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from lims import bikaMessageFactory as _
# from lims.utils import t
# from lims.config import PROJECTNAME, ManageSuppliers
# from lims.content.bikaschema import BikaSchema
# from lims.content.organisation import Organisation
# from lims.interfaces import ISupplier
# from dependencies.dependency import *
# from dependencies.dependency import safe_unicode
# from dependencies.dependency import implements
#schema = Organisation.schema.copy() + ManagedSchema((


from dependencies.dependency import safe_unicode
from lims import bikaMessageFactory as _
from openerp import fields, models, api
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget, StringWidget
from base_olims_model import BaseOLiMSModel



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
    fields.Many2one(comodel_name='olims.country',string='physical_country'),
    fields.Many2one(comodel_name='olims.state',string='physical_state', domain="[('Country', '=', physical_country)]"),
    fields.Many2one(comodel_name='olims.district',string='physical_district', domain="[('State', '=', physical_state)]"),
    fields.Char(string='physical_city'),
    fields.Char(string='physical_postalcode'),
    fields.Char(string='physical_address'),
    fields.Selection([('postal', 'Postal Address'),('billing','Billing Address')],string='physical_copy_from'),
          
    # # ~~~~~~~~~~ PostalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='postal_country'),
    fields.Many2one(comodel_name='olims.state',string='postal_state', domain="[('Country', '=', postal_country)]"),
    fields.Many2one(comodel_name='olims.district',string='postal_district', domain="[('State', '=', postal_state)]"),
    fields.Char(string='postal_city'),
    fields.Char(string='postal_postalcode'),
    fields.Char(string='postal_address'),
    fields.Selection([('physical', 'Physical Address'),('billing','Billing Address')],string='postal_copy_from'),
          
    # # ~~~~~~~~~~ BillingAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='billing_country'),
    fields.Many2one(comodel_name='olims.state',string='billing_state', domain="[('Country', '=', billing_country)]"),
    fields.Many2one(comodel_name='olims.district',string='billing_district', domain="[('State', '=', billing_state)]"),
    fields.Char(string='billing_city'),
    fields.Char(string='billing_postalcode'),
    fields.Char(string='billing_address'),
    fields.Selection([('physical','Physical Address'),('postal', 'Postal Address')],string='billing_copy_from'),

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


    TextField('Remarks',
        searchable = True,
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type = "text/html",
        widget = TextAreaWidget(
            macro = "bika_widgets/remarks",
            label=_("Remarks"),
            append_only = True,
        ),
    ),
    StringField('Website',
        searchable=1,
        required=0,
        widget=StringWidget(
            visible={'view': 'visible', 'edit': 'visible'},
            label=_('Website.'),
        ),
    ),
    StringField('NIB',
        searchable=1,
        schemata = 'Bank details',
        required=0,
        widget=StringWidget(
            visible={'view': 'visible', 'edit': 'visible'},
            label=_('NIB'),
        ),
        validators=('NIBvalidator'),
    ),
    StringField('IBN',
        searchable=1,
        schemata ='Bank details',
        required=0,
        widget=StringWidget(
            visible={'view': 'visible', 'edit': 'visible'},
            label=_('IBN'),
        ),
        validators=('IBANvalidator'),
    ),
    StringField('SWIFTcode',
        searchable=1,
        required=0,
        schemata ='Bank details',
        widget=StringWidget(
            visible={'view': 'visible', 'edit': 'visible'},
            label=_('SWIFT code.'),
        ),
    ),
    fields.One2many('olims.supplier_contact',
                    'SupplierId',
                    string='SupplierContact',
    ),
    fields.One2many('olims.instrument',
                    'Supplier',
                    string='Instrument'
    ),
    fields.One2many('olims.reference_sample',
                    'Supplier',
                    string='Reference Sample'
    ),
)

#schema['AccountNumber'].write_permission = ManageSuppliers

class Supplier(models.Model, BaseOLiMSModel): #Organisation
    _name='olims.supplier'
    _rec_name = 'Name'
    # implements(ISupplier)
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    def Title(self):
        """ Return the Organisation's Name as its title """
        return safe_unicode(self.getField('Name').get(self)).encode('utf-8')

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

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

#registerType(Supplier, PROJECTNAME)
Supplier.initialze(schema)