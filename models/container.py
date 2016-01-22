from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.widget.widget import StringWidget, TextAreaWidget, \
                                BooleanWidget
from openerp.tools.translate import _
schema = (StringField('Container',
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
    fields.Many2one(string='Container Type',
        required = False,
        comodel_name='olims.container_type',
    ),
    StringField('Capacity',
        required = 1,
        default = "0 ml",
        widget = StringWidget(
            label=_("Capacity"),
            description=_("Maximum possible size or volume of samples."),
        ),
    ),
    BooleanField('PrePreserved',
        validators = ('container_prepreservation_validator'),
        default = False,
        widget = BooleanWidget(
            label=_("Pre-preserved"),
            description = _(
                "Check this box if this container is already preserved." + \
                "Setting this will short-circuit the preservation workflow " + \
                "for sample partitions stored in this container."),
        ),
    ),
    fields.Many2one(string='Pre-preserved',
        required = False,
        comodel_name='olims.preservation',
        help="If this container is pre-preserved, then the preservation " +\
                "method could be selected here."
    ),
)

class Container(models.Model, BaseOLiMSModel):#(BaseContent):
    _name = 'olims.container'
    _rec_name = 'Container'

Container.initialze(schema)
