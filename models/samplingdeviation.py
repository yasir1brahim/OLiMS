# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from dependencies.dependency import *
# from dependencies.dependency import HoldingReference
# from dependencies.dependency import RecordsField as RecordsField
# from lims.browser.widgets import RecordsWidget
# from lims.content.bikaschema import BikaSchema
# from lims.config import PROJECTNAME
# import sys
# from lims import bikaMessageFactory as _
# from lims.utils import t
# from dependencies.dependency import implements
#

from openerp import fields, models, api, _
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget
import logging
_logger = logging.getLogger(__name__)
#
# schema = BikaSchema.copy() + Schema((
#
# ))

schema = (StringField('name',
              required=1,
    ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = ('Used in item listings and search results.'),
                            )
    ),
)

# schema['description'].schemata = 'default'
# schema['description'].widget.visible = True

class SamplingDeviation(models.Model, BaseOLiMSModel): #BaseFolder
    _name = 'olims.sampling_deviation'
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

#registerType(SamplingDeviation, PROJECTNAME)
SamplingDeviation.initialze(schema)