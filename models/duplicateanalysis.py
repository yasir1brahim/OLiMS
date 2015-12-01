"""DuplicateAnalysis uses Analysis as it's base.  Until that's fixed there
is some confusion.
"""
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from lims import bikaMessageFactory as _
# from lims.utils import t
# from lims.browser.fields import InterimFieldsField
# from lims.config import PROJECTNAME
# from lims.content.analysis import schema, Analysis
# from lims.interfaces import IDuplicateAnalysis
# from lims.subscribers import skip
# from dependencies.dependency import REFERENCE_CATALOG
# from dependencies.dependency import *
# from dependencies.dependency import HoldingReference
# from dependencies.dependency import getToolByName
# from dependencies.dependency import implements


from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.widget.widget import StringWidget
from fields.boolean_field import BooleanField
from lims import bikaMessageFactory as _
DUPLICATE_ANALYSIS_STAES = (
                            ('unassigned','Unassigned'),
                            ('assigned','Assigned'),
                            ('attachment_due','Attachment Outstanding'),
                            ('to_be_verified','To be verified'),
                            ('verified','Verified'),
                            ('rejected','Rejected'),
                            )

#schema = schema.copy() + Schema((
schema = (

    fields.Many2one(string='Analysis',
                    comodel_name='olims.analysis',
                    required=True,
        #             'Analysis',
        # required=1,
        # allowed_types=('Analysis',),
        # referenceClass=HoldingReference,
        # relationship='DuplicateAnalysisAnalysis',

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


    # ReferenceField(
    #     'Attachment',
    #     multiValued=1,
    #     allowed_types=('Attachment',),
    #     referenceClass=HoldingReference,
    #     relationship='DuplicateAnalysisAttachment',
    # ),

    StringField(
        'Analyst',
    ),

    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
                    requied=False,
        # required=0,
        # allowed_types=('Instrument',),
        # relationship='AnalysisInstrument',
        # referenceClass=HoldingReference,
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
    # implements(IDuplicateAnalysis)
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def getSample(self):
        analysis = self.getAnalysis()
        # check for getSample access, eg. ReferenceAnalysis
        if hasattr(analysis, 'getSample'):
            return analysis.getSample()
        # traverse to parent for getSample access
        analysis_parent = analysis.aq_parent
        if hasattr(analysis_parent, 'getSample'):
            return analysis_parent.getSample()

    def workflow_script_submit(self):
        workflow = getToolByName(self, 'portal_workflow')
        self.reindexObject(idxs=["review_state", ])
        # If all analyses on the worksheet have been submitted,
        # then submit the worksheet.
        ws = self.getBackReferences('WorksheetAnalysis')
        ws = ws[0]
        # if the worksheet analyst is not assigned, the worksheet can't  be transitioned.
        if ws.getAnalyst() and not skip(ws, "submit", peek=True):
            all_submitted = True
            for a in ws.getAnalyses():
                if workflow.getInfoFor(a, 'review_state') in \
                   ('to_be_sampled', 'to_be_preserved', 'sample_due',
                    'sample_received', 'assigned',):
                    all_submitted = False
                    break
            if all_submitted:
                workflow.doActionFor(ws, 'submit')
        # If no problem with attachments, do 'attach' action.
        can_attach = True
        if not self.getAttachment():
            service = self.getService()
            if service.getAttachmentOption() == 'r':
                can_attach = False
        if can_attach:
            workflow.doActionFor(self, 'attach')

    def workflow_script_attach(self):
        if skip(self, "attach"):
            return
        workflow = getToolByName(self, 'portal_workflow')
        self.reindexObject(idxs=["review_state", ])
        # If all analyses on the worksheet have been attached,
        # then attach the worksheet.
        ws = self.getBackReferences('WorksheetAnalysis')
        ws = ws[0]
        ws_state = workflow.getInfoFor(ws, 'review_state')
        if ws_state == 'attachment_due' and not skip(ws, "attach", peek=True):
            can_attach = True
            for a in ws.getAnalyses():
                if workflow.getInfoFor(a, 'review_state') in \
                   ('to_be_sampled', 'to_be_preserved', 'sample_due',
                    'sample_received', 'attachment_due', 'assigned',):
                    can_attach = False
                    break
            if can_attach:
                workflow.doActionFor(ws, 'attach')

        return

    def workflow_script_retract(self):
        if skip(self, "retract"):
            return
        workflow = getToolByName(self, 'portal_workflow')
        self.reindexObject(idxs=["review_state", ])
        # Escalate action to the Worksheet.
        ws = self.getBackReferences('WorksheetAnalysis')
        ws = ws[0]
        if skip(ws, "retract", peek=True):
            if workflow.getInfoFor(ws, 'review_state') == 'open':
                skip(ws, "retract")
            else:
                if not "retract all analyses" in self.REQUEST['workflow_skiplist']:
                    self.REQUEST["workflow_skiplist"].append("retract all analyses")
                workflow.doActionFor(ws, 'retract')

    def workflow_script_verify(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'verified'}, 
                   context=context)
        return True
        
#         if skip(self, "verify"):
#             return
#         workflow = getToolByName(self, 'portal_workflow')
#         self.reindexObject(idxs=["review_state", ])
#         # If all other analyses on the worksheet are verified,
#         # then verify the worksheet.
#         ws = self.getBackReferences('WorksheetAnalysis')
#         ws = ws[0]
#         ws_state = workflow.getInfoFor(ws, 'review_state')
#         if ws_state == 'to_be_verified' and not skip(ws, "verify", peek=True):
#             all_verified = True
#             for a in ws.getAnalyses():
#                 if workflow.getInfoFor(a, 'review_state') in \
#                    ('to_be_sampled', 'to_be_preserved', 'sample_due',
#                     'sample_received', 'attachment_due', 'to_be_verified', 'assigned'):
#                     all_verified = False
#                     break
#             if all_verified:
#                 if not "verify all analyses" in self.REQUEST['workflow_skiplist']:
#                     self.REQUEST["workflow_skiplist"].append("verify all analyses")
#                 workflow.doActionFor(ws, "verify")

    def workflow_script_assign(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'assigned'}, 
                   context=context)
        return True
#         if skip(self, "assign"):
#             return
#         workflow = getToolByName(self, 'portal_workflow')
#         self.reindexObject(idxs=["review_state", ])
#         rc = getToolByName(self, REFERENCE_CATALOG)
#         wsUID = self.REQUEST['context_uid']
#         ws = rc.lookupObject(wsUID)
# 
#         # retract the worksheet to 'open'
#         ws_state = workflow.getInfoFor(ws, 'review_state')
#         if ws_state != 'open':
#             if 'workflow_skiplist' not in self.REQUEST:
#                 self.REQUEST['workflow_skiplist'] = ['retract all analyses', ]
#             else:
#                 self.REQUEST["workflow_skiplist"].append('retract all analyses')
#             workflow.doActionFor(ws, 'retract')

    def workflow_script_unassign(self,cr,uid,ids,context=None):
        self.write(cr, uid, 
                   ids, {'state': 'assigned'}, 
                   context=context)
        return True
#         if skip(self, "unassign"):
#             return
#         workflow = getToolByName(self, 'portal_workflow')
#         self.reindexObject(idxs=["review_state", ])
#         rc = getToolByName(self, REFERENCE_CATALOG)
#         wsUID = self.REQUEST['context_uid']
#         ws = rc.lookupObject(wsUID)
# 
#         # May need to promote the Worksheet's review_state
#         #  if all other analyses are at a higher state than this one was.
#         # (or maybe retract it if there are no analyses left)
#         # Note: duplicates, controls and blanks have 'assigned' as a review_state.
#         can_submit = True
#         can_attach = True
#         can_verify = True
#         ws_empty = False
#         analyses = ws.getAnalyses()
#         # We flag this worksheet as empty if there is ONE UNASSIGNED
#         # analysis left: worksheet.removeAnalysis() hasn't removed it from
#         # the layout yet at this stage.
#         if len(analyses) == 1 \
#            and workflow.getInfoFor(analyses[0], 'review_state') == 'unassigned':
#             ws_empty = True
#         for a in analyses:
#             ws_empty = False
#             a_state = workflow.getInfoFor(a, 'review_state')
#             if a_state in \
#                ('assigned', 'sample_due', 'sample_received',):
#                 can_submit = False
#             else:
#                 if not ws.getAnalyst():
#                     can_submit = False
#             if a_state in \
#                ('assigned', 'sample_due', 'sample_received', 'attachment_due',):
#                 can_attach = False
#             if a_state in \
#                ('assigned', 'sample_due', 'sample_received', 'attachment_due', 'to_be_verified',):
#                 can_verify = False
#         if not ws_empty:
#         # Note: WS adds itself to the skiplist so we have to take it off again
#         #       to allow multiple promotions (maybe by more than one self).
#             if can_submit and workflow.getInfoFor(ws, 'review_state') == 'open':
#                 workflow.doActionFor(ws, 'submit')
#                 skip(ws, 'submit', unskip=True)
#             if can_attach and workflow.getInfoFor(ws, 'review_state') == 'attachment_due':
#                 workflow.doActionFor(ws, 'attach')
#                 skip(ws, 'attach', unskip=True)
#             if can_verify and workflow.getInfoFor(ws, 'review_state') == 'to_be_verified':
#                 self.REQUEST["workflow_skiplist"].append('verify all analyses')
#                 workflow.doActionFor(ws, 'verify')
#                 skip(ws, 'verify', unskip=True)
#         else:
#             if workflow.getInfoFor(ws, 'review_state') != 'open':
#                 workflow.doActionFor(ws, 'retract')
#                 skip(ws, 'retract', unskip=True)
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

#registerType(DuplicateAnalysis, PROJECTNAME)
DuplicateAnalysis.initialze(schema)