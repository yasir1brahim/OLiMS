import logging

from openerp import fields, models,osv

_logger = logging.getLogger(__name__)

from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import  TextAreaWidget
from lims import bikaMessageFactory as _

schema = (fields.Char(string='name',
                      compute='getNameFromTitle'),
    StringField(string='Title',
              required=1,        
    ),
    TextField(string='Description',
              widget=TextAreaWidget(
                label=_('Description'),
                description=_('Used in item listings and search results.')),    
    ),
    )


class Manufacturer(models.Model, BaseOLiMSModel):#(BaseContent):
    _name = 'olims.manufacturer'

    def getNameFromTitle(self):
        for record in self:
            record.name = record.Title

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

Manufacturer.initialze(schema)
