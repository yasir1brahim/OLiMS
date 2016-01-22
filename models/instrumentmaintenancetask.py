from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.date_time_field import DateTimeField
from fields.fixed_point_field import FixedPointField
from fields.boolean_field import BooleanField
from fields.widget.widget import StringWidget, TextAreaWidget, DateTimeWidget, BooleanWidget, ReferenceWidget, DecimalWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (


        fields.Many2one(string='Instrument',
                   comodel_name='olims.instrument',

    ),

    StringField('Type',
        vocabulary = "getMaintenanceTypes",
        widget = ReferenceWidget(
            checkbox_bound = 0,
            label = ("Maintenance type",
                      "Type"),
        ),
    ),

    DateTimeField('DownFrom',
        with_time = 1,
        with_date = 1,
        required = 1,
        widget = DateTimeWidget(
            label=_("From"),
            description=_("Date from which the instrument is under maintenance"),
            show_hm = True,
        ),
    ),

    DateTimeField('DownTo',
        with_time = 1,
        with_date = 1,
        widget = DateTimeWidget(
            label=_("To"),
            description=_("Date until the instrument will not be available"),
            show_hm = True,
        ),
    ),

    StringField('Maintainer',
        widget = StringWidget(
            label=_("Maintainer"),
            description=_("The analyst or agent responsible of the maintenance"),
        )
    ),

    TextField('Considerations',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Considerations"),
            description=_("Remarks to take into account for maintenance process"),
        ),
    ),

    TextField('WorkPerformed',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Work Performed"),
            description=_("Description of the actions made during the maintenance process"),
        ),
    ),

    TextField('Remarks',
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            label=_("Remarks"),
        ),
    ),

    FixedPointField('Cost',
        default = '0.00',
        widget = DecimalWidget(
            label=_("Price"),
        ),
    ),

    BooleanField('Closed',
        default = '0',
        widget = BooleanWidget(
            label=_("Closed"),
            description=_("Set the maintenance task as closed.")
        ),
    ),
)


class InstrumentMaintenanceTaskStatuses:
    CLOSED = 'Closed'
    CANCELLED = 'Cancelled'
    OVERDUE = "Overdue"
    PENDING = "Pending"
    INQUEUE = "In queue"

class InstrumentMaintenanceTask(models.Model, BaseOLiMSModel): #BaseFolder
    _name = 'olims.instrument_maintenance_task'

InstrumentMaintenanceTask.initialze(schema)