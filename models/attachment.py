from openerp import fields, models
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.file_field import FileField
from fields.widget.widget import  DateTimeWidget, FileWidget, StringWidget
from base_olims_model import BaseOLiMSModel
from lims import bikaMessageFactory as _

schema = (
    # ~~~~~~~ To be implemented ~~~~~~~
    #          ComputedField('RequestID',
    #     expression = 'here.getRequestID()',
    #     widget = ComputedWidget(
    #         visible = True,
    #     ),
    # ),
    FileField('AttachmentFile',
        widget = FileWidget(
            label=_("Attachment"),
        ),
    ),


    fields.Many2one(string='AttachmentType',
                    comodel_name='olims.attachment_type',
                    required=False,
                    help='Attachment Type'
        ),

     StringField('AttachmentKeys',
        searchable = True,
        widget = StringWidget(
            label=_("Attachment Keys"),
        ),
    ),
    DateTimeField('DateLoaded',
        required = 1,
        default_method = 'current_date',
        widget = DateTimeWidget(
            label=_("Date Loaded"),
        ),
    ),
    # ~~~~~~~ To be implemented ~~~~~~~
    # ComputedField('ClientUID',
    #     expression = 'here.aq_parent.UID()',
    #     widget = ComputedWidget(
    #         visible = False,
    #     ),
    # ),
)

class Attachment(models.Model, BaseOLiMSModel):
    _name='olims.attachment'

class res_company(models.Model):
    _inherit = "res.company"
    report_logo = fields.Binary("Report Logo", attachment=True,
            help="This field holds the image used as avatar for reports logo, limited to 1024x1024px",
            )
Attachment.initialze(schema)