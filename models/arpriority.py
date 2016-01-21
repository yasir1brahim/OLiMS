# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from lims.utils import t
# from lims.content.bikaschema import BikaSchema
# from lims.config import PROJECTNAME
# from lims.interfaces import IARPriority
# from dependencies import atapi
# from dependencies.dependency import *
# from dependencies.dependency import implements

import logging
from openerp import models

_logger = logging.getLogger(__name__)

from lims.idserver import renameAfterCreation
from lims import bikaMessageFactory as _
from base_olims_model import BaseOLiMSModel
from fields.integer_field import IntegerField
from fields.file_field import FileField
from fields.boolean_field import BooleanField
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import IntegerWidget, BooleanWidget, FileWidget, \
                                TextAreaWidget, StringWidget
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# schema = BikaSchema.copy() + Schema((
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
)#)
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# schema['description'].widget.visible = True


class ARPriority(models.Model, BaseOLiMSModel):#(BaseContent):
    _name = 'olims.ar_priority'
    _rec_name = 'Priority'
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
#     security = ClassSecurityInfo()
#     schema = schema
#     displayContentsTab = False
#     implements(IARPriority)
#     _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        renameAfterCreation(self)

ARPriority.initialze(schema)
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# atapi.registerType(ARPriority, PROJECTNAME)
