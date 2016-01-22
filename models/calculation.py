from openerp import fields, models,osv
from openerp.tools.translate import _
from fields.widget.widget import TextAreaWidget, StringWidget
from fields.string_field import StringField
from fields.text_field import TextField
from base_olims_model import BaseOLiMSModel

schema = (
          
          fields.Many2many(string='InterimFields',
                           comodel_name='olims.interimfield'
            ),
          
    StringField('Calculation',
        required=1,
        schemata='Description',
    ),
    StringField('Description',
        schemata='Description',
        widget=StringWidget(
            label=_('Description'),
            description=_("Used in item listings and search results."),
        ),
    ),
    StringField('Changenote',
        schemata='Description',
        widget=StringWidget(
            label=_('Change note'),
            description=_("Enter a comment that describes the changes you made."),
        ),
    ),
    TextField('Formula',
        schemata='Calculation',
        validators=('formulavalidator',),
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        widget = TextAreaWidget(
            label=_("Calculation Formula"),
            description=(
                "calculation_formula_description"
                "<p>The formula you type here will be dynamically calculated "
                "when an analysis using this calculation is displayed.</p>"
                "<p>To enter a Calculation, use standard maths operators,  "
                "+ - * / ( ), and all keywords available, both from other "
                "Analysis Services and the Interim Fields specified here, "
                "as variables. Enclose them in square brackets [ ].</p>"
                "<p>E.g, the calculation for Total Hardness, the total of "
                "Calcium (ppm) and Magnesium (ppm) ions in water, is entered "
                "as [Ca] + [Mg], where Ca and MG are the keywords for those "
                "two Analysis Services.</p>"),
            )
    ),
)


class Calculation(models.Model, BaseOLiMSModel): #:(BaseFolder, HistoryAwareMixin):
    _name = 'olims.calculation'
    _rec_name = 'Calculation'
        
Calculation.initialze(schema)
