"""AttachmentType - the type of attachment
"""
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget


schema = (StringField('attachment type',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = ('Used in item listings and search results.'),
                            )
    ),
)

class AttachmentType(models.Model, BaseOLiMSModel):
    _name = 'olims.attachment_type'
    _rec_name = 'attachment type'


AttachmentType.initialze(schema)