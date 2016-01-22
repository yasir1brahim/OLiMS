
from openerp import models
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, TextAreaWidget
from base_olims_model import BaseOLiMSModel
from openerp.tools.translate import _

schema = (StringField('Container Type',
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
    )

class ContainerType(models.Model, BaseOLiMSModel):
    _name = 'olims.container_type'
    _rec_name = 'Container Type'

ContainerType.initialze(schema)
