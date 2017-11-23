"""
    AnalysisRequests often use the same configurations.
    AnalysisProfile is used to save these common configurations (templates).
"""
from openerp import fields, models, api
from openerp.tools.translate import _
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.fixed_point_field import FixedPointField
from fields.widget.widget import StringWidget, AnalysisProfileAnalysesWidget, \
                                 TextAreaWidget, ComputedWidget, \
                                 BooleanWidget, DecimalWidget

# ~~~~~ Useful code that need to be converted in Odoo style ~~~~~~ 
schema = (StringField('Profile',
              required=1,        
    ),
    TextField('Description',
        widget = TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),                 
    StringField('ProfileKey',
        widget = StringWidget(
            label = _("Profile Keyword"),
            description = _("The profile's keyword is used to uniquely identify " + \
                          "it in import files. It has to be unique, and it may " + \
                          "not be the same as any Calculation Interim field ID."),
        ),
    ),
          
          
    
    fields.Many2many(string='Service', comodel_name='olims.records_field_artemplates', required=True,\
                     relation='records_field_service_relation',\
                     help='The analyses included in this profile, grouped per category',
        ),
    fields.Many2many(string='Client', comodel_name='olims.client',\
                     relation='olims_rel_analysis_profile_client',\
                     help='Specify the clint for this Analysis Profile',
        ),
    TextField('Remarks',
        searchable = True,
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            macro = "bika_widgets/remarks",
            label = _("Remarks"),
            append_only = True,
        ),
    ),
    StringField('CommercialID',
        searchable=1,
        required=0,
        schemata='Accounting',
        widget=StringWidget(
            visible={'view': 'visible', 'edit': 'visible'},
            label=_('Commercial ID'),
            description=_("The profile's commercial ID for accounting purposes."),
        ),
    ),
    BooleanField('Deactivated',
        default=False,
        schemata='Accounting',
        widget=BooleanWidget(
            label=_("Use Analysis Profile Deactivate"),
        )
    ),

    # When it's set, the system uses the analysis profile's price to quote and the system's VAT is overridden by the
    # the analysis profile's specific VAT
    BooleanField('UseAnalysisProfilePrice',
        default=False,
        schemata='Accounting',
        widget=BooleanWidget(
            label=_("Use Analysis Profile Price"),
            description=_("When it's set, the system uses the analysis profile's price to quote and the system's VAT is"
                          " overridden by the analysis profile's specific VAT"),
        )
    ),
    # The price will only be used if the checkbox "use analysis profiles' price" is set.
    # This price will be used to quote the analyses instead of analysis service's price.
    FixedPointField('AnalysisProfilePrice',
        schemata="Accounting",
        default=0.00,
        widget=DecimalWidget(
            label = _("Price (excluding VAT)"),
            visible={'view': 'visible', 'edit': 'visible'},
        ),
    ),
    
    FixedPointField('AnalysisProfileVAT',
        schemata = "Accounting",
        default = 14.00,
        widget = DecimalWidget(
            label=_("VAT %"),
            description=_(
                "Enter percentage value eg. 14.0. This percentage is applied on the Analysis Profile only, overriding "
                "the systems VAT"),
                visible={'view': 'visible', 'edit': 'visible'},
        )
    ),
    # When the checkbox "use analysis profiles' price" is set, the AnalysisProfilesVAT should override
    # the system's VAT

    # This VAT amount is computed using the AnalysisProfileVAT instead of systems VAT
    #TODO
    fields.Float(compute='computeVATAmount',string='VATAmount'),
   
   fields.Float(compute='computeTotalPrice',string='TotalPrice'),
   fields.Many2one(string='ClientProfile',
                   comodel_name='olims.client'),
   StringField(string="status", compute="compute_status")
)

     
class AnalysisProfile(models.Model, BaseOLiMSModel):
    _name = "olims.analysis_profile"
    _rec_name = 'Profile'

    def computeVATAmount(self):
        """ Compute AnalysisProfileVATAmount
        """
        for record  in self:
            price, vat = record.getAnalysisProfileVAT(), record.getAnalysisProfilePrice(), 
            record.VATAmount =  float(vat) * float(price)  / 100
            

    def computeTotalPrice(self):
        """
        Computes the final price using the VATAmount and the subtotal price
        """
        for reccord  in self:
            price, vat = reccord.getAnalysisProfilePrice(), reccord.getVATAmount()
            reccord.TotalPrice =  float(price)+float(vat)

    @api.depends("Deactivated")
    def compute_status(self):
        for record in self:
            if record.Deactivated:
                record.status = "Deactive"
            else:
                record.status = "Active"


AnalysisProfile.initialze(schema)
