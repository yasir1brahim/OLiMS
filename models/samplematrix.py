from openerp import fields, models
from lims import bikaMessageFactory as _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget
from base_olims_model import BaseOLiMSModel

schema = (StringField('Sample Matrix',
              required=1,        
    ),
    TextField('Description',
              widget=TextAreaWidget(
                label=_('Description'),
                description=_('Used in item listings and search results.')),    
    ),
    )

class SampleMatrix(models.Model, BaseOLiMSModel):#(BaseFolder):
    _name = 'olims.sample_matrix'
    _rec_name = 'Sample Matrix'


    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)
SampleMatrix.initialze(schema)
