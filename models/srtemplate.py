"""
    Sample Round Template
"""



from lims import bikaMessageFactory as _
from fields.text_field import TextField
from fields.string_field import StringField
from fields.integer_field import IntegerField
from fields.widget.widget import TextAreaWidget, StringWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (StringField('Template',
        required=1,
        widget=StringWidget(
            label=_('Title'),
            description=_('Title is required.'),
        ),
    ),
    TextField('Description',
        widget=TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    fields.Many2one(string='Department',
                    comodel_name='olims.department',
                    help='The laboratory department',
                    required=True,
                    relation='srtemplate_department'
    ),
    TextField('Instructions',
            searchable = True,
            default_content_type = 'text/plain',
            allowed_content_types= ('text/plain'),
            default_output_type="text/plain",
            widget = TextAreaWidget(
            label=_("Instructions"),
            append_only = True,
        ),
    ),

    fields.Many2many(string='ARTemplates',
                   comodel_name='olims.ar_template',
                   required=True,

    ),
    IntegerField(string='Sampling Frequency',
                 required=True,
                 default=7
    ),
    fields.Many2one(string='ClientSRTemplate',
                    comodl_name='olims.client'
    ),
    fields.Many2one(string='Sampler',
        comodel_name="res.users",
        domain="[('groups_id', 'in', (14,18))]",
        required = True
    ),

)


class SRTemplate(models.Model, BaseOLiMSModel):
    _name = 'olims.sr_template'
    _rec_name = 'Template'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        renameAfterCreation(self)


SRTemplate.initialze(schema)
