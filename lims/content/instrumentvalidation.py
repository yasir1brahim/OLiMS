from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import schemata
from dependencies.dependency import HoldingReference
from dependencies import atapi
from dependencies.dependency import *
from dependencies.dependency import getToolByName
from lims import bikaMessageFactory as _
from lims.browser.widgets import DateTimeWidget, ReferenceWidget
from lims.config import PROJECTNAME
from lims.content.bikaschema import BikaSchema

schema = BikaSchema.copy() + Schema((

    DateTimeField('DateIssued',
        with_time = 1,
        with_date = 1,
        widget = DateTimeWidget(
            label=_("Report Date"),
            description=_("Validation report date"),
        ),
    ),

    DateTimeField('DownFrom',
        with_time = 1,
        with_date = 1,
        widget = DateTimeWidget(
            label=_("From"),
            description=_("Date from which the instrument is under validation"),
        ),
    ),

    DateTimeField('DownTo',
        with_time = 1,
        with_date = 1,
        widget = DateTimeWidget(
            label=_("To"),
            description=_("Date until the instrument will not be available"),
        ),
    ),

    StringField('Validator',
        widget = StringWidget(
            label=_("Validator"),
            description=_("The analyst responsible of the validation"),
        )
    ),

    TextField('Considerations',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Considerations"),
            description=_("Remarks to take into account before validation"),
        ),
    ),

    TextField('WorkPerformed',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Work Performed"),
            description=_("Description of the actions made during the validation"),
        ),
    ),

    ReferenceField('Worker',
        vocabulary='getLabContacts',
        allowed_types=('LabContact',),
        relationship='LabContactInstrumentValidation',
        widget=ReferenceWidget(
            checkbox_bound=0,
            label=_("Performed by"),
            description=_("The person at the supplier who performed the task"),
            size=30,
            base_query={'inactive_state': 'active'},
            showOn=True,
            colModel=[{'columnName': 'UID', 'hidden': True},
                      {'columnName': 'JobTitle', 'width': '20', 'label': _('Job Title')},
                      {'columnName': 'Title', 'width': '80', 'label': _('Name')}
                     ],
        ),
    ),

    StringField('ReportID',
        widget = StringWidget(
            label=_("Report ID"),
            description=_("Report identification number"),
        )
    ),

    TextField('Remarks',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Remarks"),
        ),
    ),

))

schema['title'].widget.label = 'Asset Number'

class InstrumentValidation(BaseFolder):
    security = ClassSecurityInfo()
    schema = schema
    displayContentsTab = False

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def getLabContacts(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        # fallback - all Lab Contacts
        pairs = []
        for contact in bsc(portal_type='LabContact',
                           inactive_state='active',
                           sort_on='sortable_title'):
            pairs.append((contact.UID, contact.Title))
        return DisplayList(pairs)

atapi.registerType(InstrumentValidation, PROJECTNAME)
