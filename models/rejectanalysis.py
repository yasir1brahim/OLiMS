""" RejectAnalysis """

from openerp import fields, models
from lims import bikaMessageFactory as _
from fields.string_field import StringField
from fields.boolean_field import BooleanField
from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.date_time_field import DateTimeField
from fields.integer_field import IntegerField
from fields.widget.widget import ComputedWidget, DateTimeWidget, \
                                IntegerWidget, DecimalWidget
from base_olims_model import BaseOLiMSModel

schema = (fields.Many2one(string='Calculation',
                   comodel_name='olims.calculation',
                   required=False,

            ),
    fields.Many2many(string='InterimFields',
                     comodel_name='olims.interimfield',
    ),

    StringField('Result',
    ),
    DateTimeField('ResultCaptureDate',
        widget = ComputedWidget(
            visible=False,
        ),
    ),
    StringField('ResultDM',
    ),
    BooleanField('Retested',
        default = False,
    ),
          
          
    fields.Char(string='Days'),
    fields.Char(string='Hours'),
    fields.Char(string='Minutes'),

    DateTimeField('DateAnalysisPublished',
        widget = DateTimeWidget(
            label = _("Date Published"),
        ),
    ),
    DateTimeField('DueDate',
        widget = DateTimeWidget(
            label = _("Due Date"),
        ),
    ),
    IntegerField('Duration',
        widget = IntegerWidget(
            label = _("Duration"),
        )
    ),
    IntegerField('Earliness',
        widget = IntegerWidget(
            label = _("Earliness"),
        )
    ),
    BooleanField('ReportDryMatter',
        default = False,
    ),
    StringField('Analyst',
    ),
    TextField('Remarks',
    ),
    FixedPointField('Uncertainty',
        widget=DecimalWidget(
            label = _("Uncertainty"),
        ),
    ),
    StringField('DetectionLimitOperand',
    ),

    # The analysis that was originally rejected
    fields.Many2one(string='Analysis',
                        comodel_name='olims.analysis',
        # allowed_types=('Analysis',),
        # relationship = 'RejectAnalysisAnalysis',
        ),

)

class RejectAnalysis(models.Model, BaseOLiMSModel): #Analysis
    _name ='olims.reject_analysis'


RejectAnalysis.initialze(schema)