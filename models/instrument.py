from datetime import date
from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.date_time_field import DateTimeField
from fields.file_field import FileField
from fields.reference_field import ReferenceField
from fields.widget.widget import StringWidget, TextAreaWidget, BooleanWidget, FileWidget, DateTimeWidget
from openerp.tools.translate import _
from openerp.exceptions import Warning
schema = (

    StringField('Instrument',
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

    fields.Many2one(string='Type',
           comodel_name='olims.instrument_type',
           required=True,
    ),


    fields.Many2one(string='Brand',
           comodel_name='olims.manufacturer',
           required=True,
    ),
    
    fields.Many2one(string='Supplier',
                    comodel_name='olims.supplier',
                    required=True,
    ),

    StringField('Model',
        widget = StringWidget(
            label=_("Model"),
            description=_("The instrument's model number"),
        )
    ),

    StringField('SerialNo',
        widget = StringWidget(
            label=_("Serial No"),
            description=_("The serial number that uniquely identifies the instrument"),
        )
    ),


        fields.Many2one(string='Method',
                   comodel_name='olims.method',
                   required=False,
                   help="Method",
    ),


    BooleanField('DisposeUntilNextCalibrationTest',
        default = False,
        widget = BooleanWidget(
            label=_("De-activate until next calibration test"),
            description=_("If checked, the instrument will be unavailable until the next valid "+
                          "calibration was performed. This checkbox will automatically be unchecked."),
        ),
    ),

    # Procedures
    TextField('InlabCalibrationProcedure',
        schemata = 'Procedures',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("In-lab calibration procedure"),
            description=_("Instructions for in-lab regular calibration routines intended for analysts"),
        ),
    ),
    TextField('PreventiveMaintenanceProcedure',
        schemata = 'Procedures',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Preventive maintenance procedure"),
            description=_("Instructions for regular preventive and maintenance routines intended for analysts"),
        ),
    ),
    StringField('AssetNumber',
        widget = StringWidget(
            label=_("Asset Number"),
            description=_("The instrument's ID in the lab's asset register"),
        )
    ),

    StringField('Location',
        schemata = 'Additional info.',
        widget = StringWidget(
            label=_("Location"),
            description=_("The room and location where the instrument is installed"),
        )
    ),

    FileField('Photo',
              help='Photo of the instrument',
        widget = FileWidget(
            label = _("Photo image file"),
        ),
    ),
          
    DateTimeField('InstallationDate',
    schemata = 'Additional info.',
    widget = DateTimeWidget(
        label=_("InstallationDate"),
        description=_("The date the instrument was installed"),
        )
    ),

    FileField('InstallationCertificate',
    schemata = 'Additional info.',
    widget = FileWidget(
        label=_("Installation Certificate"),
        description=_("Installation certificate upload"),
        ),
    ),
    DateTimeField('Expiry Date',
                  widget = DateTimeWidget(
                            label=_("Expiry Date"),
                            description=_("Date until the certificate is valid"),
        ),
    ),
    fields.One2many('olims.instrument_calibration',
                                 'Instrument',
                                 string='Instrument Calibration'\
    ),
    fields.One2many('olims.instrument_certification',
                                 'Instrument',
                                 string='Instrument Certification'\
    ),
    fields.One2many('olims.instrument_validation',
                                 'Instrument',
                                 string='Instrument Validation'\
    ),
    fields.One2many('olims.multifile',
                                 'Instrument',
                                 string='Document'\
    ),

)

class Instrument(models.Model, BaseOLiMSModel):
    _name = 'olims.instrument'
    _rec_name = 'Instrument'

    @api.model
    def create(self, values):
        new_record = super(Instrument,self).create(values)
        MessageAlertsObjects = self.env['olims.message_alert']
        alert_message_vals = { 'message' : "Instrument's calibration certificate expired",
                'severity' :"high",
                'Instrument' : new_record.id,
        }
        MessageAlertsObjects.create(alert_message_vals)
        return new_record

    @api.one
    @api.constrains("SerialNo")
    def check_unique_serial_number(self):
        if self.SerialNo :
            filters = [("SerialNo", '=', self.SerialNo),
                       ]
            instrument_ids = self.search(filters)
            if len(instrument_ids) > 1:
                raise Warning(
                    _('There can not be two instruments with the same serial number.'))

Instrument.initialze(schema)