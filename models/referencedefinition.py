""" Reference Definitions represent standard specifications for
    reference samples used in quality control
"""
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from openerp.tools.translate import _
from fields.boolean_field import BooleanField
from fields.widget.widget import BooleanWidget, TextAreaWidget
from fields.string_field import StringField
from fields.text_field import TextField

schema = (
    fields.Many2many(string='Reference_Results',
        comodel_name = 'olims.reference_values',
        required = True,
    ),
    StringField('name',
              required=1,        
    ),
    # StringField('Title',
    #           required=1,        
    # ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = _('Used in item listings and search results.'),
                            )
    ),
    BooleanField('Blank',
        schemata = 'Description',
        default = False,
        widget = BooleanWidget(
            label=_("Blank"),
            description=_("Reference sample values are zero or 'blank'"),
        ),
    ),
    BooleanField('Hazardous',
        schemata = 'Description',
        default = False,
        widget = BooleanWidget(
            label=_("Hazardous"),
            description=_("Samples of this type should be treated as hazardous"),
        ),
    ),
)


class ReferenceDefinition(models.Model, BaseOLiMSModel):
    _name ='olims.reference_definition'
    _rec_name = "name"


    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

ReferenceDefinition.initialze(schema)