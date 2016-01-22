"""DuplicateAnalysis uses Analysis as it's base.  Until that's fixed there
is some confusion.
"""
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.widget.widget import StringWidget
from fields.boolean_field import BooleanField
from openerp.tools.translate import _
DUPLICATE_ANALYSIS_STAES = (
                            ('unassigned','Unassigned'),
                            ('assigned','Assigned'),
                            ('attachment_due','Attachment Outstanding'),
                            ('to_be_verified','To be verified'),
                            ('verified','Verified'),
                            ('rejected','Rejected'),
                            )

schema = (

    fields.Many2one(string='Analysis',
                    comodel_name='olims.analysis',
                    required=True,
    ),
          
    fields.Many2many(string='InterimFields', comodel_name='olims.interimfield'),


    StringField(
        'Result',
    ),
    StringField(
        'ResultDM',
    ),
    BooleanField(
        'Retested',
    ),
# ~~~~~~~ To be implemented ~~~~~~~
# fields.One2many(string='Attachment',
#                     comodel_name='olims.analysis',
#          #     multiValued=1,
#     #     allowed_types=('Attachment',),
#     #     referenceClass=HoldingReference,
#     #     relationship='DuplicateAnalysisAttachment',
#     ),


    StringField(
        'Analyst',
    ),

    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
                    requied=False,
    ),

# ~~~~~~~ To be implemented ~~~~~~~
    # ComputedField(
    #     'SamplePartition',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getSamplePartition()',
    # ),
    # ComputedField(
    #     'ClientOrderNumber',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getClientOrderNumber()',
    # ),
    # ComputedField(
    #     'Service',
    #     expression='context.getAnalysis() and context.getAnalysis().getService() or ""',
    # ),
    # ComputedField(
    #     'ServiceUID',
    #     expression='context.getAnalysis() and context.getAnalysis().getServiceUID()',
    # ),
    # ComputedField(
    #     'CategoryUID',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getCategoryUID()',
    # ),
    # ComputedField(
    #     'Calculation',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getCalculation()',
    # ),
    # ComputedField(
    #     'ReportDryMatter',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getReportDryMatter()',
    # ),
    # ComputedField(
    #     'DateReceived',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getDateReceived()',
    # ),
    # ComputedField(
    #     'MaxTimeAllowed',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getMaxTimeAllowed()',
    # ),
    # ComputedField(
    #     'DueDate',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getDueDate()',
    # ),
    # ComputedField(
    #     'Duration',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getDuration()',
    # ),
    # ComputedField(
    #     'Earliness',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getEarliness()',
    # ),
    # ComputedField(
    #     'ClientUID',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getClientUID()',
    # ),
    # ComputedField(
    #     'RequestID',
    #     expression='context.getAnalysis() and context.getAnalysis().aq_parent.portal_type=="AnalysisRequest" and context.getAnalysis().getRequestID() or ""',
    # ),
    # ComputedField(
    #     'PointOfCapture',
    #     expression='context.getAnalysis() and context.getAnalysis().getPointOfCapture()',
    # ),

    StringField(
        'ReferenceAnalysesGroupID',
        widget=StringWidget(
            label=_("ReferenceAnalysesGroupID"),
            visible=False,
        ),
    ),
    fields.Selection(string='state',
                     selection=DUPLICATE_ANALYSIS_STAES,
                     default='unassigned',
                     select=True,
                     required=True, readonly=True,
                     copy=False, track_visibility='always'
    ),
    # ~~~~~~~ To be implemented ~~~~~~~
    # ComputedField(
    #     'Keyword',
    #     expression="context.getAnalysis().getKeyword()",
#    ),

)



class DuplicateAnalysis(models.Model, BaseOLiMSModel): #Analysis
    _name='olims.duplicate_analysis'

    def workflow_script_submit(self):
        return ""

    def workflow_script_attach(self):
        return ""

    def workflow_script_retract(self):
        return ""

    def workflow_script_verify(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'verified'}, 
                   context=context)
        return True

    def workflow_script_assign(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'assigned'}, 
                   context=context)
        return True

    def workflow_script_unassign(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'assigned'}, 
                   context=context)
        return True

    def workflow_script_attachment_due(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'attachment_due'}, 
                   context=context)
        return True
    def workflow_script_to_be_verified(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'to_be_verified'}, 
                   context=context)
        return True
    def workflow_script_rejected(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'rejected'}, 
                   context=context)
        return True

DuplicateAnalysis.initialze(schema)