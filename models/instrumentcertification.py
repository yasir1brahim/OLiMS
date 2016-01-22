from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.file_field import FileField
from fields.date_time_field import DateTimeField
from fields.reference_field import ReferenceField
from fields.boolean_field import BooleanField
from fields.widget.widget import StringWidget, TextAreaWidget, DateTimeWidget, BooleanWidget, FileWidget
from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from messagealert import write_message

schema = (StringField('Certificate Code',
                      required=1,
                      widget = StringWidget(
                            label=_("Certificate Code"),
        ),
    ),

    fields.Many2one(string='Instrument',
                   comodel_name='olims.instrument',
                   required = False,
    ),

    # Set the Certificate as Internal
    # When selected, the 'Agency' field is hidden
    BooleanField('Internal',
        default=False,
        widget=BooleanWidget(
            label=_("Internal Certificate"),
            description=_("Select if is an in-house calibration certificate")
        )
    ),

    StringField('Agency',
        widget = StringWidget(
            label=_("Agency"),
            description=_("Organization responsible of granting the calibration certificate")
        ),
    ),

    DateTimeField('Date',
        widget = DateTimeWidget(
            label=_("Date"),
            description=_("Date when the calibration certificate was granted"),
        ),
    ),

    DateTimeField('ValidFrom',
        with_time = 1,
        with_date = 1,
        required = 1,
        widget = DateTimeWidget(
            label=_("From"),
            description=_("Date from which the calibration certificate is valid"),
        ),
    ),

    DateTimeField('DownTo',
        with_time = 1,
        with_date = 1,
        required = 1,
        widget = DateTimeWidget(
            label=_("To"),
            description=_("Date until the certificate is valid"),
        ),
    ),

    fields.Many2one(string='Preparator',
                   comodel_name='olims.lab_contact',
                   help="The person at the supplier who prepared the certificate",
    ),

    fields.Many2one(string='Validator',
                   comodel_name='olims.lab_contact',
                   help="The person at the supplier who approved the certificate"
    ),



    FileField('Document',
        widget = FileWidget(
            label=_("Report upload"),
            description=_("Load the certificate document here"),
        )
    ),

    TextField('Remarks',
        searchable=True,
        default_content_type='text/x-web-intelligent',
        allowable_content_types = ('text/plain', ),
        default_output_type="text/plain",
        mode="rw",
        widget=TextAreaWidget(
            macro="bika_widgets/remarks",
            label=_("Remarks"),
            append_only=True,
        ),
    ),

)

sourcemodel = "InstrumentCertification"

class InstrumentCertification(models.Model, BaseOLiMSModel):
    _name = 'olims.instrument_certification'

    @api.model
    def create(self, values):
        write_message(self, values, sourcemodel)
        res = super(InstrumentCertification, self).create(values)
        return res

    @api.multi
    def write(self, data):
        write_message(self, data, sourcemodel)
        res = super(InstrumentCertification, self).write(data)
        return res

InstrumentCertification.initialze(schema)