""" Reference Definitions represent standard specifications for
    reference samples used in quality control
"""
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from dependencies.dependency import DateTime
# from dependencies.dependency import *
# from lims.content.bikaschema import BikaSchema
# from lims.browser.fields import ReferenceResultsField
# from lims.browser.widgets import ReferenceResultsWidget
# from lims.config import PROJECTNAME
# import sys
# import time
# from lims import PMF, bikaMessageFactory as _
# from dependencies.dependency import implements

from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from lims import bikaMessageFactory as _
from fields.boolean_field import BooleanField
from fields.widget.widget import BooleanWidget, TextAreaWidget
from fields.string_field import StringField
from fields.text_field import TextField




#schema = BikaSchema.copy() + Schema((
schema = (fields.Many2many(string='Reference Results',
        comodel_name = 'olims.reference_values',
        required = True,
    ),
    StringField('Title',
              required=1,        
    ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = _('Used in item listings and search results.'),
                            )
    ),
    BooleanField('Blank',
        schemata = 'Description',
        default = False,
        widget = BooleanWidget(
            label=_("Blank"),
            description=_("Reference sample values are zero or 'blank'"),
        ),
    ),
    BooleanField('Hazardous',
        schemata = 'Description',
        default = False,
        widget = BooleanWidget(
            label=_("Hazardous"),
            description=_("Samples of this type should be treated as hazardous"),
        ),
    ),
)

# schema['title'].schemata = 'Description'
# schema['title'].widget.visible = True
# schema['description'].schemata = 'Description'
# schema['description'].widget.visible = True

class ReferenceDefinition(models.Model, BaseOLiMSModel): #BaseContent
    _name ='olims.reference_definition'
    _rec_name = "Title"
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

#registerType(ReferenceDefinition, PROJECTNAME)
ReferenceDefinition.initialze(schema)