from lims import bikaMessageFactory as _
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget, StringWidget
schema = (StringField('Sub Group',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = ('Used in item listings and search results.'),
                            )
    ),
    StringField(
        'Sort Key',
        widget=StringWidget(
            label=_("Sort Key"),
            description=_("Subgroups are sorted with this key in group views")
        )
    ),
)
class SubGroup(models.Model, BaseOLiMSModel):
    _name = 'olims.subgroup'
    _rec_name = 'Sub Group'

SubGroup.initialze(schema)