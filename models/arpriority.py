
from openerp import models
from openerp.tools.translate import _
from base_olims_model import BaseOLiMSModel
from fields.integer_field import IntegerField
from fields.file_field import FileField
from fields.boolean_field import BooleanField
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import IntegerWidget, BooleanWidget, FileWidget, \
                                TextAreaWidget, StringWidget
schema = (StringField('Priority',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = _('Used in item listings and search results.'),
                            )
    ),
          IntegerField('Sort Key',
        widget=IntegerWidget(
            label = _("Sort Key"),
            description = _("Numeric value indicating the sort order of objects that are prioritised"),
        ),
    ),
    IntegerField('Premium',
        widget=IntegerWidget(
            label = _("Price Premium Percentage"),
            description = _("The percentage used to calculate the price for analyses done at this priority"),
        ),
    ),
          
    FileField('smallIcon',
              help='6x16 pixel icon used for the this priority in listings.',
              widget = FileWidget(
              label = _("Small Icon"),
              ),
    ),
          
    FileField('bigIcon',
              help='32x32 pixel icon used for the this priority in object views.',
              widget = FileWidget(
              label = _("Big Icon"),
              ),
    ),
         
    BooleanField('Default',
        widget=BooleanWidget(
            label = _("Default Priority?"),
            description = _("Check this box if this is the default priority"),
        ),
    ),
    StringField('ChangeNote',
        widget=StringWidget(
            label=_("Change Note"),
            description=_("Enter a comment that describes the changes you made")
        ),
    ),
)

class ARPriority(models.Model, BaseOLiMSModel):
    _name = 'olims.ar_priority'
    _rec_name = 'Priority'


ARPriority.initialze(schema)
