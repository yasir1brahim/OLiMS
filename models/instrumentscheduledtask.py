from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, TextAreaWidget, ReferenceWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (

    fields.Many2one(string='Instrument',
                   comodel_name='olims.instrument',

    ),

    StringField('Type',
        vocabulary = "getTaskTypes",
        widget = ReferenceWidget(
            checkbox_bound = 0,
            label = ("Task type",
                      "Type"),
        ),
    ),

    TextField('Considerations',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Considerations"),
            description=_("Remarks to take into account before performing the task"),
        ),
    ),
)

class InstrumentScheduledTask(models.Model, BaseOLiMSModel): #BaseFolder
    _name = 'olims.instrument_scheduled_task'

InstrumentScheduledTask.initialze(schema)