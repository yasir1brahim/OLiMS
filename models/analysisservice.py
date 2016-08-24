# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.reference_field import ReferenceField
from fields.boolean_field import BooleanField
from fields.integer_field import IntegerField
from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.widget.widget import *
from openerp import fields, models, api
from openerp.exceptions import Warning

SERVICE_POINT_OF_CAPTURE =(
                           ('field', _('Field')),
                           ('lab', _('Lab')),
                           )

ATTACHMENT_OPTIONS = (
                      ('r', 'Required'),
                      ('p', 'Permitted'),
                      ('n', 'Not Permitted')
                      )

schema = (StringField('Service',
        required=1,
        widget=StringWidget(
            label=_('Title'),
            description=_('Title is required.'),
        ),
    ),
    TextField('Description',
        widget=TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    StringField('ShortTitle',
                schemata="Description",
                widget=StringWidget(
                    label = _("Short title"),
                    description=_(
                        "If text is entered here, it is used instead of the " + \
                        "title when the service is listed in column headings. " + \
                        "HTML formatting is allowed.")
                ),
    ),
    BooleanField('ScientificName',
                 schemata="Description",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Scientific name"),
                     description = _(
                        "If enabled, the name of the analysis will be " + \
                        "written in italics."),
                 ),
    ),
    StringField('Unit',
                schemata="Description",
                widget=StringWidget(
                    label = _("Unit"),
                    description=_(
                        "The measurement units for this analysis service' results, " + \
                        "e.g. mg/l, ppm, dB, mV, etc."),
                ),
    ),
    IntegerField('Precision',
                 schemata="Analysis",
                 widget=IntegerWidget(
                     label = _("Precision as number of decimals"),
                     description=_(
                         "Define the number of decimals to be used for this result."),
                 ),
    ),
    IntegerField('ExponentialFormatPrecision',
                 schemata="Analysis",
                 default = 7,
                 widget=IntegerWidget(
                     label = _("Exponential format precision"),
                     description=_(
                         "Define the precision when converting values to exponent " + \
                         "notation.  The default is 7."),
                 ),
    ),
    FixedPointField('LowerDetectionLimit',
                    schemata="Analysis",
                    default=0.0,
                    precision=7,
                    widget=DecimalWidget(
                        label = _("Lower Detection Limit (LDL)"),
                        description = _("The Lower Detection Limit is " + \
                                        "the lowest value to which the " + \
                                        "measured parameter can be " + \
                                        "measured using the specified " + \
                                        "testing methodology. Results " + \
                                        "entered which are less than " + \
                                        "this value will be reported " + \
                                        "as < LDL")
                    ),
    ),
    FixedPointField('UpperDetectionLimit',
                schemata="Analysis",
                default=1000000000.0,
                precision=7,
                widget=DecimalWidget(
                    label = _("Upper Detection Limit (UDL)"),
                    description = _("The Upper Detection Limit is the " + \
                                    "highest value to which the " + \
                                    "measured parameter can be measured " + \
                                    "using the specified testing " + \
                                    "methodology. Results entered " + \
                                    "which are greater than this value " + \
                                    "will be reported as > UDL")
                ),
    ),
    # LIMS-1775 Allow to select LDL or UDL defaults in results with readonly mode
    # https://jira.bikalabs.com/browse/LIMS-1775
    # Some behavior controlled with javascript: If checked, the field
    # "AllowManualDetectionLimit" will be displayed.
    # See browser/js/bika.lims.analysisservice.edit.js
    #
    # Use cases:
    # a) If "DetectionLimitSelector" is enabled and
    # "AllowManualDetectionLimit" is enabled too, then:
    # the analyst will be able to select an '>', '<' operand from the
    # selection list and also set the LD manually.
    #
    # b) If "DetectionLimitSelector" is enabled and
    # "AllowManualDetectionLimit" is unchecked, the analyst will be
    # able to select an operator from the selection list, but not set
    # the LD manually: the default LD will be displayed in the result
    # field as usuall, but in read-only mode.
    #
    # c) If "DetectionLimitSelector" is disabled, no LD selector will be
    # displayed in the results table.
    BooleanField('DetectionLimitSelector',
        schemata="Analysis",
        default=False,
        widget=BooleanWidget(
            label = _("Display a Detection Limit selector"),
            description = _("If checked, a selection list will be " + \
                            "displayed next to the analysis' result " + \
                            "field in results entry views. By using " + \
                            "this selector, the analyst will be able " + \
                            "to set the value as a Detection Limit " + \
                            "(LDL or UDL) instead of a regular result"),
        ),
    ),
    # Behavior controlled with javascript: Only visible when the
    # "DetectionLimitSelector" is checked
    # See browser/js/bika.lims.analysisservice.edit.js
    # Check inline comment for "DetecionLimitSelector" field for
    # further information.
    BooleanField('AllowManualDetectionLimit',
             schemata="Analysis",
             default=False,
             widget=BooleanWidget(
                label = _("Allow Manual Detection Limit input"),
                description = _("Allow the analyst to manually " + \
                                "replace the default Detection Limits " + \
                                "(LDL and UDL) on results entry views"),
             ),
    ),
    BooleanField('ReportDryMatter',
                 schemata="Analysis",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Report as Dry Matter"),
                     description = _("These results can be reported as dry matter"),
                 ),
    ),
    # ~~~~~~~~~~ Using Odoo fields.Selection field due to SelectionWidget ~~~~~~~~~~
    fields.Selection(string='AttachmentOption',
                selection=ATTACHMENT_OPTIONS,
#                 schemata="Analysis",
                default='p',
                help="Indicates whether file attachments, e.g. microscope images, " + \
                        "are required for this analysis and whether file upload function " + \
                        "will be available for it on data capturing screens",
    ),
    StringField('Keyword',
                schemata="Description",
                required=1,
                searchable=True,
                validators=('servicekeywordvalidator'),
                widget=StringWidget(
                    label = _("Analysis Keyword"),
                    description=_(
                        "The unique keyword used to identify the analysis service in " + \
                        "import files of bulk AR requests and results imports from instruments. " + \
                        "It is also used to identify dependent analysis services in user " + \
                        "defined results calculations"),
                ),
    ),
    # Allow/Disallow manual entry of results
    # Behavior controlled by javascript depending on Instruments field:
    # - If InstrumentEntry not checked, set checked and readonly
    # - If InstrumentEntry checked, set as not readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('ManualEntryOfResults',
                 schemata="Method",
                 default=True,
                 readonly=True,
                 widget=BooleanWidget(
                     label = _("Allow manual entry of results"),
                     description=_("Select if the results for this Analysis " + \
                                   "Service can be set manually."),
                 )
    ),
    # Allow/Disallow instrument entry of results
    # Behavior controlled by javascript depending on Instruments field:
    # - If no instruments available, hide and uncheck
    # - If at least one instrument selected, checked, but not readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('InstrumentEntryOfResults',
                 schemata="Method",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Allow instrument entry of results"),
                     description=_("Select if the results for this Analysis " + \
                                   "Service can be set using an Instrument."),
                 )
    ),
    # Instruments associated to the AS
    # List of instruments capable to perform the Analysis Service. The
    # Instruments selected here are displayed in the Analysis Request
    # Add view, closer to this Analysis Service if selected.
    # - If InstrumentEntry not checked, hide and unset
    # - If InstrumentEntry checked, set the first selected and show
    fields.Many2many(string='Instruments',
                   comodel_name='olims.instrument',
#                    schemata="Method",
                   required=False,
                   help="More than one instrument can do an " + \
                                    "Analysis Service. The instruments " + \
                                    "selected here are displayed in the " + \
                                    "Analysis Request creation view for its " + \
                                    "selection when this Analysis Service is " + \
                                    "selected.",
    ),
    # Default instrument to be used.
    # Gets populated with the instruments selected in the multiselection
    # box above.
    # Behavior controlled by js depending on ManualEntry/Instruments:
    # - Populate dynamically with selected Instruments
    # - If InstrumentEntry checked, set first selected instrument
    # - If InstrumentEntry not checked, hide and set None
    # See browser/js/bika.lims.analysisservice.edit.js
    
    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
#                    schemata="Method",
                    required=False,
    ),
    # Manual methods associated to the AS
    # List of methods capable to perform the Analysis Service. The
    # Methods selected here are displayed in the Analysis Request
    # Add view, closer to this Analysis Service if selected.
    # Use getAvailableMethods() to retrieve the list with methods both
    # from selected instruments and manually entered.
    # Behavior controlled by js depending on ManualEntry/Instrument:
    # - If InsrtumentEntry not checked, show
    # See browser/js/bika.lims.analysisservice.edit.js
    fields.Many2many(string='Methods',
        comodel_name='olims.method',
        help="The Analysis Service can be performed by " + \
                            "using more than one Method. The methods " + \
                            "selected here are displayed in the " + \
                            "Analysis Request creation view for its " + \
                            "selection when this Analaysis Service " + \
                            "is selected. Only methods with 'Allow " + \
                            "manual entry of results' enabled are " + \
                            "displayed.",
#         schemata = "Method",
        required = False,
    ),
    # Default method to be used. This field is used in Analysis Service
    # Edit view, use getMethod() to retrieve the Method to be used in
    # this Analysis Service.
    # Gets populated with the methods selected in the multiselection
    # box above or with the default instrument's method.
    # Behavior controlled by js depending on ManualEntry/Instrument/Methods:
    # - If InstrumentEntry checked, set instrument's default method, and readonly
    # - If InstrumentEntry not checked, populate dynamically with
    #   selected Methods, set the first method selected and non-readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    fields.Many2one(string='_Method',
        comodel_name='olims.method',
#         schemata = "Method",
        required = 0,
        help="If 'Allow instrument entry of results' " + \
                        "is selected, the method from the default instrument " + \
                        "will be used. Otherwise, only the methods " + \
                        "selected above will be displayed.",
    ),
    # Allow/Disallow to set the calculation manually
    # Behavior controlled by javascript depending on Instruments field:
    # - If no instruments available, hide and uncheck
    # - If at least one instrument selected, checked, but not readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('UseDefaultCalculation',
                 schemata="Method",
                 default=True,
                 widget=BooleanWidget(
                     label = _("Use default calculation"),
                     description=_("Select if the calculation to be used is the " + \
                                   "calculation set by default in the default " + \
                                   "method. If unselected, the calculation can " + \
                                   "be selected manually"),
                 )
    ),
    # Default calculation to be used. This field is used in Analysis Service
    # Edit view, use getCalculation() to retrieve the Calculation to be used in
    # this Analysis Service.
    # The default calculation is the one linked to the default method
    # Behavior controlled by js depending on UseDefaultCalculation:
    # - If UseDefaultCalculation is set to False, show this field
    # - If UseDefaultCalculation is set to True, show this field
    # See browser/js/bika.lims.analysisservice.edit.js
    fields.Many2one(string='_Calculation',
                   comodel_name='olims.calculation',
#                    schemata="Method",
                   required=False,
                   help="Default calculation to be used from the " + \
                                    "default Method selected. The Calculation " + \
                                    "for a method can be assigned in the Method " + \
                                    "edit view.",
    ),
    # Default calculation is not longer linked directly to the AS: it
    # currently uses the calculation linked to the default Method.
    # Use getCalculation() to retrieve the Calculation to be used.
    # Old ASes (before 3008 upgrade) can be linked to the same Method,
    # but to different Calculation objects. In that case, the Calculation
    # is saved as DeferredCalculation and UseDefaultCalculation is set to
    # False in the upgrade.
    # Behavior controlled by js depending on UseDefaultCalculation:
    # - If UseDefaultCalculation is set to False, show this field
    # - If UseDefaultCalculation is set to True, show this field
    # See browser/js/bika.lims.analysisservice.edit.js
    #     bika/lims/upgrade/to3008.py
    fields.Many2one(string='DeferredCalculation',
                   comodel_name='olims.calculation',
#                    schemata="Method",
                   required=False,
                   help="If required, select a calculation for the analysis here. " + \
                            "Calculations can be configured under the calculations item " + \
                            "in the LIMS set-up",
    ),
    fields.Many2many(string='InterimFields',
                    comodel_name='olims.interimfield',
                          #        schemata='Method',
    ),
    fields.Char(string='Days', required=False),
    fields.Char(string='Hours', required=False),
    fields.Char(string='Minutes', required=False),
    FixedPointField('DuplicateVariation',
                    schemata="Method",
                    widget=DecimalWidget(
                        label = _("Duplicate Variation %"),
                        description=_(
                            "When the results of duplicate analyses on worksheets, " + \
                            "carried out on the same sample, differ with more than " + \
                            "this percentage, an alert is raised"),
                    ),
    ),
    BooleanField('Accredited',
                 schemata="Method",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Accredited"),
                     description=_(
                         "Check this box if the analysis service is included in the " + \
                         "laboratory's schedule of accredited analyses"),
                 ),
    ),
    
    fields.Selection(string='PointOfCapture',
                selection=SERVICE_POINT_OF_CAPTURE,
#                 schemata="Description",
                required=1,
                default='lab',
                help="The results of field analyses are captured during sampling " + \
                        "at the sample point, e.g. the temperature of a water sample " + \
                        "in the river where it is sampled. Lab analyses are done in " + \
                        "the laboratory",
    ),
    fields.Many2one(string='category',
                   comodel_name='olims.analysis_category',
#                    schemata="Description",
                   required=True,
                   help="The category the analysis service belongs to",
    ),
    FixedPointField('Price',
                    schemata="Description",
                    default=0.00,
                    widget=DecimalWidget(
                        label = _("Price (excluding VAT)"),
                    ),
    ),
    # read access permission
    FixedPointField('BulkPrice',
                    schemata="Description",
                    default=0.00,
                    widget=DecimalWidget(
                        label = _("Bulk price (excluding VAT)"),
                        description=_(
                            "The price charged per analysis for clients who qualify for bulk discounts"),
                    ),
    ),
    fields.Float(compute='computeVATAmount',string='VATAmount'),
    fields.Float(compute='computeTotalPrice',string='TotalPrice'),
    FixedPointField('VAT',
                    schemata="Description",
                    default_method='getDefaultVAT',
                    widget=DecimalWidget(
                        label = _("VAT %"),
                        description = _("Enter percentage value eg. 14.0"),
                    ),
    ),
    fields.Many2one(string='Department',
                   comodel_name='olims.department',
#                    schemata="Description",
                   required=False,
                   help="The laboratory department",
    ),
    fields.One2many(string='Uncertainties',
                       comodel_name='olims.uncertinty_service',
                       inverse_name='analysis_service_id'
        ),

    # Calculate the precision from Uncertainty value
    # Behavior controlled by javascript
    # - If checked, Precision and ExponentialFormatPrecision are not displayed.
    #   The precision will be calculated according to the uncertainty.
    # - If checked, Precision and ExponentialFormatPrecision will be displayed.
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('PrecisionFromUncertainty',
                 schemata="Uncertainties",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Calculate Precision from Uncertainties"),
                     description=_("Precision as the number of significant " + \
                                   "digits according to the uncertainty. " + \
                                   "The decimal position will be given by " + \
                                   "the first number different from zero in " + \
                                   "the uncertainty, at that position the " + \
                                   "system will round up the uncertainty " + \
                                   "and results. " + \
                                   "For example, with a result of 5.243 and " + \
                                   "an uncertainty of 0.22, the system " + \
                                   "will display correctly as 5.2+-0.2. " + \
                                   "If no uncertainty range is set for the " + \
                                   "result, the system will use the " + \
                                   "fixed precision set."),
                 ),
    ),

    # If checked, an additional input with the default uncertainty will
    # be displayed in the manage results view. The value set by the user
    # in this field will override the default uncertainty for the analysis
    # result
    BooleanField('AllowManualUncertainty',
                 schemata="Uncertainties",
                 default=False,
                 widget=BooleanWidget(
                    label = _("Allow manual uncertainty value input"),
                    description = _("Allow the analyst to manually " + \
                                    "replace the default uncertainty " + \
                                    "value."),
                ),
    ),
          
          
    fields.One2many(string='ResultOptions',
                       comodel_name='olims.result_option',
                       inverse_name='service_resultoption_id'

        ),

    BooleanField('Separate',
                 schemata='Container and Preservation',
                 default=False,
                 required=0,
                 widget=BooleanWidget(
                     label = _("Separate Container"),
                     description=_("Check this box to ensure a separate sample " + \
                                   "container is used for this analysis service"),
                 ),
    ),

    fields.Many2one(string='Preservation',
                    comodel_name='olims.preservation',
                    help="Select a default preservation for this " + \
                                    "analysis service. If the preservation depends on " + \
                                    "the sample type combination, specify a preservation " + \
                                    "per sample type in the table below",
                    required=False,
    ),
    fields.Many2one(string='Container',
                   comodel_name='olims.container',
                   required=False,
                   help="Select the default container to be used for this " + \
                            "analysis service. If the container to be used " + \
                            "depends on the sample type and preservation " + \
                            "combination, specify the container in the sample " + \
                            "type table below",
    ),
    fields.Many2many(string='PartitionSetup',
                     comodel_name='olims.partition_setup'
    ),

    BooleanField('Hidden',
                 schemata="Analysis",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Hidden"),
                     description = _(
                        "If enabled, this analysis and its results " + \
                        "will not be displayed by default in reports. " + \
                        "This setting can be overrided in Analysis " + \
                        "Profile and/or Analysis Request"),
                 ),
    ),
    StringField('CommercialID',
        searchable=1,
        schemata='Description',
        required=0,
        widget=StringWidget(
            label=_("Commercial ID"),
            description=_("The service's commercial ID for accounting purposes")
        ),
    ),
    StringField('ProtocolID',
        searchable=1,
        schemata = 'Description',
        required=0,
        widget=StringWidget(
            label=_("Protocol ID"),
            description=_("The service's analytical protocol ID")
        ),
    ),
    StringField('ChangeNote',
        schemata = 'Description',
        widget=StringWidget(
            label=_("Change Note"),
            description=_("Enter a comment that describes the changes you made")
        ),
    ),
)


class AnalysisService(models.Model, BaseOLiMSModel):
    _name = 'olims.analysis_service'
    _rec_name = 'Service'

    def computeTotalPrice(self):
        """ compute total price """
        for record in self:
            price = record.getPrice()
            vat = record.getVAT()
            price = price and price or 0
            vat = vat and vat or 0
            record.TotalPrice = float(price) + (float(price) * float(vat)) / 100


    def getTotalBulkPrice(self):
        """ compute total price """
        price = self.getBulkPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100


    def getTotalDiscountedPrice(self):
        """ compute total discounted price """
        price = self.getDiscountedPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100


    def getTotalDiscountedBulkPrice(self):
        """ compute total discounted corporate price """
        price = self.getDiscountedCorporatePrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    def getDefaultVAT(self):
        """ return default VAT from bika_setup """
        try:
            vat = self.bika_setup.getVAT()
            return vat
        except ValueError:
            return "0.00"

    
    def computeVATAmount(self):
        for record in self:
            price, vat = record.getPrice(), record.getVAT()
            record.VATAmount = (float(price) * (float(vat) / 100))
        

    def getPrecision(self, result=None):
        """
        Returns the precision for the Analysis Service. If the
        option Calculate Precision according to Uncertainty is not
        set, the method will return the precision value set in the
        Schema. Otherwise, will calculate the precision value
        according to the Uncertainty and the result.
        If Calculate Precision to Uncertainty is set but no result
        provided neither uncertainty values are set, returns the
        fixed precision.

        Examples:
        Uncertainty     Returns
        0               1
        0.22            1
        1.34            0
        0.0021          3
        0.013           2

        For further details, visit
        https://jira.bikalabs.com/browse/LIMS-1334

        :param result: if provided and "Calculate Precision according
                       to the Uncertainty" is set, the result will be
                       used to retrieve the uncertainty from which the
                       precision must be calculated. Otherwise, the
                       fixed-precision will be used.
        :return: the precision
        """
        pass


    def getExponentialFormatPrecision(self, result=None):
        """
        Returns the precision for the Analysis Service and result
        provided. Results with a precision value above this exponential
        format precision should be formatted as scientific notation.

        If the Calculate Precision according to Uncertainty is not set,
        the method will return the exponential precision value set in
        the Schema. Otherwise, will calculate the precision value
        according to the Uncertainty and the result.

        If Calculate Precision from the Uncertainty is set but no
        result provided neither uncertainty values are set, returns the
        fixed exponential precision.

        Will return positive values if the result is below 0 and will
        return 0 or positive values if the result is above 0.

        Given an analysis service with fixed exponential format
        precision of 4:
        Result      Uncertainty     Returns
        5.234           0.22           0
        13.5            1.34           1
        0.0077          0.008         -3
        32092           0.81           4
        456021          423            5

        For further details, visit
        https://jira.bikalabs.com/browse/LIMS-1334

        :param result: if provided and "Calculate Precision according
                       to the Uncertainty" is set, the result will be
                       used to retrieve the uncertainty from which the
                       precision must be calculated. Otherwise, the
                       fixed-precision will be used.
        :return: the precision
        """
        pass

    @api.one
    @api.constrains("Keyword")
    def check_unique_keyword(self):
        if self.Keyword :
            filters = [("Keyword", '=', self.Keyword),
                       ]
            analysis_service_ids = self.search(filters)
            if len(analysis_service_ids) > 1:
                raise Warning(
                    _('There can not be two services with the same keyword.'))

    @api.onchange('Methods')
    def onchanage_methods_set_default_method(self):
        for item in self:
            if item.Methods:
                item._Method = item.Methods[0]



AnalysisService.initialze(schema)
