"""Analysis result range specifications for a client
"""
from openerp.tools.translate import _
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget

schema = (fields.Many2one(string='Sample Type',
                   comodel_name='olims.sample_type',
                   required=False,
                   help="Sample Type",
            ),
    StringField('Title',
              required=1,        
    ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = _('Used in item listings and search results.'),
                            )
    ),
    fields.Many2many(string='Specifications',
                comodel_name='olims.specification',
                relation='analysis_service_specification',
                help="Click on Analysis Categories (against shaded background" \
                    "to see Analysis Services in each category. Enter minimum " \
                    "and maximum values to indicate a valid results range. " \
                    "Any result outside this range will raise an alert. " \
                    "The % Error field allows for an % uncertainty to be " \
                    "considered when evaluating results against minimum and " \
                    "maximum values. A result out of range but still in range " \
                    "if the % error is taken into consideration, will raise a " \
                    "less severe alert. If the result is below '< Min' " \
                    "the result will be shown as '< [min]'. The same " \
                    "applies for results above '> Max'"
    ),
    
    fields.Many2one(string='ClientUID',
        comodel_name = "olims.client",
    ),
)

class AnalysisSpec(models.Model, BaseOLiMSModel):
    _name = "olims.analysis_spec"
    _rec_name = "Title"

AnalysisSpec.initialze(schema)

