from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.date_time_field import DateTimeField
from fields.widget.widget import StringWidget, TextAreaWidget, DateTimeWidget
from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from messagealert import write_message

schema = (StringField('AssetNumber',
                      required=1,
                      widget = StringWidget(
                            label=_("Asset Number"),
        )
    ),
    DateTimeField('DateIssued',
        with_time = 1,
        with_date = 1,
        widget = DateTimeWidget(
            label=_("Report Date"),
            description=_("Validation report date"),
        ),
    ),
    fields.Many2one(string='Instrument',
                   comodel_name='olims.instrument',
                   required=False,

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

    fields.Many2one(string='Worker',
                   comodel_name='olims.lab_contact',
                   help='The person at the supplier who performed the task',
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

)

sourcemodel = "InstrumentValidation"

class InstrumentValidation(models.Model, BaseOLiMSModel):
    _name='olims.instrument_validation'

    @api.model
    def create(self, values):
        write_message(self, values, sourcemodel)
        new_record = super(InstrumentValidation, self).create(values)
        return new_record

    @api.multi
    def write(self, data):
        write_message(self, data, sourcemodel)
        res = super(InstrumentValidation, self).write(data)
        return res


InstrumentValidation.initialze(schema)