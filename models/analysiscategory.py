"""Analysis Category - the category of the analysis service
"""
from openerp import fields, models
from openerp.tools.translate import _
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget
from base_olims_model import BaseOLiMSModel
schema =  (StringField('Category',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = _('Used in item listings and search results.'),
                            )
    ),
    TextField('Comments',
        default_output_type = 'text/plain',
        allowable_content_types = ('text/plain',),
        widget=TextAreaWidget (
            description = _("To be displayed below each Analysis "
                            "Category section on results reports."),
            label = _("Comments")),
    ),
    fields.Many2one(string='Department',
        comodel_name='olims.department',
        required=False,
        help='The laboratory department'
    ),
)

class AnalysisCategory(models.Model, BaseOLiMSModel):
    _name = "olims.analysis_category"
    _rec_name = 'Category'

AnalysisCategory.initialze(schema)
