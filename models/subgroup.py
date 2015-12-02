# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from lims.utils import t
# from lims.config import PROJECTNAME
# from lims.interfaces import ISubGroup
# from lims.content.bikaschema import BikaSchema
# from lims.fields import *
# from dependencies.dependency import *
# from dependencies.dependency import implements

from lims import bikaMessageFactory as _
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget, StringWidget
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# schema = BikaSchema.copy() + Schema((
schema = (StringField('name',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = ('Used in item listings and search results.'),
                            )
    ),
    StringField(
        'SortKey',
        widget=StringWidget(
            label=_("Sort Key"),
            description=_("Subgroups are sorted with this key in group views")
        )
    ),
)
# schema['description'].widget.visible = True
# schema['description'].schemata = 'default'


class SubGroup(models.Model, BaseOLiMSModel): #(BaseContent):
    _name = 'olims.subgroup'
SubGroup.initialze(schema)
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
#     implements(ISubGroup)
#     security = ClassSecurityInfo()
#     displayContentsTab = False
#     schema = schema
# 
#     _at_rename_after_creation = True
# 
#     def _renameAfterCreation(self, check_auto_id=False):
#         from lims.idserver import renameAfterCreation
#         renameAfterCreation(self)
# 
# registerType(SubGroup, PROJECTNAME)