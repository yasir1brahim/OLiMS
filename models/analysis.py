# -*- coding: utf-8 -*-

"DuplicateAnalysis uses this as it's base.  This accounts for much confusion."
import datetime
import math
from openerp import fields, models
from fields.string_field import StringField
from fields.boolean_field import BooleanField
from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.date_time_field import DateTimeField
from fields.integer_field import IntegerField
from fields.widget.widget import ComputedWidget, DateTimeWidget, \
                                IntegerWidget, DecimalWidget
from base_olims_model import BaseOLiMSModel
from openerp.tools.translate import _
schema = (
            fields.Many2one(string='Service',
                   comodel_name='olims.analysis_service',
                   required=True,
                   help="Analysis Service",
            ),


        fields.Many2one(string='Calculation',
                   comodel_name='olims.calculation',
                   required=False
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

    StringField('Analyst',
    ),
    TextField('Remarks',
    ),

    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
                    required=False

    ),

     fields.Many2one(string='Method',
                    comodel_name='olims.method',
                    required=False

    ),
    fields.Many2one(string='SamplePartition',
                    comodel_name='olims.sample_partition',
                    required=False
    ),

# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('ClientUID',
#         expression = 'context.aq_parent.aq_parent.UID()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('ClientTitle',
#         expression = 'context.aq_parent.aq_parent.Title()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('RequestID',
#         expression = 'context.aq_parent.getRequestID()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('ClientOrderNumber',
#         expression = 'context.aq_parent.getClientOrderNumber()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('Keyword',
#         expression = 'context.getService().getKeyword()',
#     ),
#     ComputedField('ServiceTitle',
#         expression = 'context.getService().Title()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('ServiceUID',
#         expression = 'context.getService().UID()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('SampleTypeUID',
#         expression = 'context.aq_parent.getSample().getSampleType().UID()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('SamplePointUID',
#         expression = 'context.aq_parent.getSample().getSamplePoint().UID() if context.aq_parent.getSample().getSamplePoint() else None',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('CategoryUID',
#         expression = 'context.getService().getCategoryUID()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('CategoryTitle',
#         expression = 'context.getService().getCategoryTitle()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('PointOfCapture',
#         expression = 'context.getService().getPointOfCapture()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('DateReceived',
#         expression = 'context.aq_parent.getDateReceived()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('DateSampled',
#         expression = 'context.aq_parent.getSample().getDateSampled()',
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('InstrumentValid',
#         expression = 'context.isInstrumentValid()'
#     ),
    FixedPointField('Uncertainty',
        widget=DecimalWidget(
            label = _("Uncertainty"),
        ),
    ),
    StringField('DetectionLimitOperand',
    ),

)


class Analysis(models.Model, BaseOLiMSModel): #(BaseContent):
    _name = 'olims.analysis'
                
Analysis.initialze(schema)


