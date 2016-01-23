from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, TextAreaWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
PRESERVATION_CATEGORIES = (
    ('field', _('Field Preservation')),
    ('lab', _('Lab Preservation')),
    )
schema = (StringField('Preservation',
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
    fields.Selection(string='Category',
        selection=PRESERVATION_CATEGORIES,
        default='lab',
    ),
    
    fields.Char(string='Days'),
    fields.Char(string='Hours'),
    fields.Char(string='Minutes'),

)


class Preservation(models.Model, BaseOLiMSModel):
    _name = 'olims.preservation'
    _rec_name = 'Preservation'


    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

Preservation.initialze(schema)