"""AttachmentType - the type of attachment
"""
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from dependencies.dependency import *
# from lims.content.bikaschema import BikaSchema
# from lims.config import PROJECTNAME
# import sys
# from lims import bikaMessageFactory as _
# from lims.utils import t
# from dependencies.dependency import implements
#
# schema = BikaSchema.copy()

from openerp import fields, models
from models.base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget


schema = (StringField('name',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = ('Used in item listings and search results.'),
                            )
    ),
)

# schema['description'].widget.visible = True
# schema['description'].schemata = 'default'

class AttachmentType(models.Model, BaseOLiMSModel): #BaseContent
    _name = 'olims.attachment_type'
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

#registerType(AttachmentType, PROJECTNAME)

AttachmentType.initialze(schema)