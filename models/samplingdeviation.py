from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget
import logging
_logger = logging.getLogger(__name__)

schema = (StringField('Sampling Deviation',
              required=1,
    ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = ('Used in item listings and search results.'),
                            )
    ),
)

class SamplingDeviation(models.Model, BaseOLiMSModel):
    _name = 'olims.sampling_deviation'
    _rec_name = 'Sampling Deviation'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

SamplingDeviation.initialze(schema)