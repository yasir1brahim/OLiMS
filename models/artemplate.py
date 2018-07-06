"""
    AnalysisRequests often use the same configurations.
    ARTemplate includes all AR fields, including preset AnalysisProfile
"""
from openerp.tools.translate import _
from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from fields.widget.widget import BooleanWidget, TextAreaWidget
from fields.boolean_field import BooleanField
from fields.string_field import StringField
from fields.text_field import TextField

schema = (StringField('Template',
              required=1,        
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = _('Used in item listings and search results.'),
                            )
    ),
    ## SamplePoint and SampleType references are managed with
    ## accessors and mutators below to get/set a string value
    ## (the Title of the object), but still store a normal Reference.
    ## Form autocomplete widgets can then work with the Titles.

    fields.Many2one(string='Sample Point',
                    comodel_name='olims.sample_point',
                    help="Location where sample was taken",
                    required=False,
                    ),

    fields.Many2one(string='SampleType',
                    comodel_name='olims.sample_type',
                    help="Create a new sample of this type",
                    required=False,
    ),


    TextField('Remarks',
        searchable = True,
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            macro = "bika_widgets/remarks",
            label = _("Remarks"),
            append_only = True,
        ),
    ),
          
        fields.Many2many(string='Partitions',
                       comodel_name='olims.partition_ar_template',
        ),

    fields.Many2many(string='AnalysisProfile',
                    comodel_name='olims.analysis_profile',
                    help="The Analysis Profile selection for this template",
                    required=False,
    ),
    fields.Many2many(string='Analyses',
                       comodel_name='olims.records_field_artemplates',
    ),
    fields.Many2one(string='ClientARTemplate',
                    comodel_name='olims.client',
                    ),
    fields.Many2many('olims.contact',string="contact_id"),
    fields.Many2many('olims.email', string="email_id"),
    fields.Many2one(string='priority',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
)

class ARTemplate(models.Model, BaseOLiMSModel):
    _name = 'olims.ar_template'
    _rec_name = 'Template'

    @api.model
    def create(self, values):
        client = values.get('ClientARTemplate', None)
        if not client:
            client = self._context.get('client_context', None)
        values.update({'ClientARTemplate':client})
        res = super(ARTemplate, self).create(values)
        return res


ARTemplate.initialze(schema)
