from openerp import fields, models,osv
from dependencies.dependency import getToolByName
from openerp.tools.translate import _
from lims.utils import t
from dependencies.dependency import DisplayList
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.file_field import FileField
from fields.widget.widget import StringWidget, TextAreaWidget, \
                                FileWidget, BooleanWidget, \
                                ReferenceWidget, MultiSelectionWidget

schema = (
    StringField('Method',
        required=True,
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
    # Method ID should be unique, specified on MethodSchemaModifier
    StringField('MethodID',
        searchable=1,
        required=0,
        help='Define an identifier code for the method. It must be unique.',
        validators=('uniquefieldvalidator',),
        widget=StringWidget(
            visible={'view': 'visible', 'edit': 'visible'},
            label=_('Method ID'),
            description=_('Define an identifier code for the method. It must be unique.'),
        ),
    ),
    TextField('Instructions',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label = ("Method Instructions",
                      "Instructions"),
            description=_("Technical description and instructions intended for analysts"),
        ),
    ),
    FileField('MethodDocument',  # XXX Multiple Method documents please
        widget = FileWidget(
            label=_("Method Document"),
            description=_("Load documents describing the method here"),
        )
    ),
    fields.Many2one(string='Instruments',
        comodel_name='olims.instrument_type',
        vocabulary='getInstrumentsDisplayList',
        widget=MultiSelectionWidget(
            modes = ('edit'),
            label=_("Instruments"),
            description =_(
                "The selected instruments have support for this method. "
                "Use the Instrument edit view to assign "
                "the method to a specific instrument"),
        ),
    ),

    # If no instrument selected, always True. Otherwise, the user will
    # be able to set or unset the value. The behavior for this field
    # is controlled with javascript.
    BooleanField('ManualEntryOfResults',
        default=True,
        readonly=True,
        widget=BooleanWidget(
            label=_("Manual entry of results"),
            description=_("The results for the Analysis Services that use this method can be set manually"),
            modes = ('edit'),
        )
    ),

    # Calculations associated to this method. The analyses services
    # with this method assigned will use the calculation selected here.

    fields.Many2one(string='Calculation',
                   comodel_name='olims.calculation',
                   required=False,
                   help="If required, select a calculation for the "+
                           "The analysis services linked to this "+
                           "method. Calculations can be configured "+
                           "under the calculations item in the LIMS "+
                            "set-up",
    ),

    BooleanField('Accredited',
        schemata="default",
        default=True,
        widget=BooleanWidget(
            label=_("Accredited"),
            description=_("Check if the method has been accredited"))
    ),
    StringField('ChangeNote',
        schemata = 'Description',
        widget=StringWidget(
            label=_("Change Note"),
            description=_("Enter a comment that describes the changes you made")
        ),
    ),
)

class Method(models.Model, BaseOLiMSModel):#(BaseFolder):
    _name = 'olims.method'
    _rec_name = 'Method'
    
    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def isManualEntryOfResults(self):
        """ Indicates if manual entry of results is allowed.
            If no instrument is selected for this method, returns True.
            Otherwise, returns False by default, but its value can be
            modified using the ManualEntryOfResults Boolean Field
        """
        return len(self.getInstruments()) == 0 or self.getManualEntryOfResults()

    def _getCalculations(self):
        """ Returns a DisplayList with the available Calculations
            registered in Bika-Setup. Used to fill the Calculation
            ReferenceWidget.
        """
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(c.UID, c.Title) \
                for c in bsc(portal_type='Calculation',
                             inactive_state = 'active')]
        items.sort(lambda x,y: cmp(x[1], y[1]))
        items.insert(0, ('', t(_('None'))))
        return DisplayList(list(items))

    def getInstruments(self):
        """ Instruments capable to perform this method
        """
        return self.getBackReferences('InstrumentMethod')

    def getInstrumentUIDs(self):
        """ UIDs of the instruments capable to perform this method
        """
        return [i.UID() for i in self.getInstruments()]

    def getInstrumentsDisplayList(self):
        """ DisplayList containing the Instruments capable to perform
            this method.
        """
        items = [(i.UID(), i.Title()) for i in self.getInstruments()]
        return DisplayList(list(items))

    def _getAvailableInstrumentsDisplayList(self):
        """ Available instruments registered in the system
            Only instruments with state=active will be fetched
        """
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(i.UID, i.Title) \
                for i in bsc(portal_type='Instrument',
                             inactive_state = 'active')]
        items.sort(lambda x,y: cmp(x[1], y[1]))
        return DisplayList(list(items))
    
Method.initialze(schema)
