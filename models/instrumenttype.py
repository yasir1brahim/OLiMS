from openerp import fields, models,osv

from base_olims_model import BaseOLiMSModel
from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget

schema = (StringField('Title',
              required=1,        
    ),
    TextField('Description',
              widget=TextAreaWidget(
                label=_('Description'),
                description=_('Used in item listings and search results.')),    
    ),
    fields.One2many('olims.instrument',
                    'Type',
                    string='Type')
    )


class InstrumentType(models.Model, BaseOLiMSModel):#(BaseContent):
    _name = 'olims.instrument_type'
    _rec_name = 'Title'


InstrumentType.initialze(schema)
