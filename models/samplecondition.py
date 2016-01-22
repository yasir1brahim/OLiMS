from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget

schema = (StringField('Sample Condition',
              required=1,
    ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = ('Used in item listings and search results.'),
                            )
    ),
)

class SampleCondition(models.Model, BaseOLiMSModel): #BaseFolder
    _name='olims.sample_condition'
    _rec_name = 'Sample Condition'


    _at_rename_after_creation = True

SampleCondition.initialze(schema)
