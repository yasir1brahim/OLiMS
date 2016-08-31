"""Sample represents a physical sample submitted for testing
"""
from dependencies.dependency import DT2dt, dt2DT
import sys
from dependencies.dependency import getToolByName
from dependencies.dependency import safe_unicode
from openerp.tools.translate import _
from openerp import fields, models
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.date_time_field import DateTimeField
from base_olims_model import BaseOLiMSModel
import datetime
SAMPLE_STATES = (
                ('sample_registered', 'Registered'),
                ('to_be_sampled', 'To Be Sampled'),
                ('sampled', 'Sampled'),
                ('to_be_preserved', 'To Be Preserved'),
                ('sample_received', 'Sample Received'),
                ('sample_due', 'Sample Due'),
                ('expired', 'Expired'),
                ('disposed', 'Disposed'),
                )
schema = (StringField('name',
              compute='compute_smapleName',        
    ),
    fields.Char('SampleID',
        required=0,
        compute='compute_smapleId',
        help=_("The ID assigned to the client's sample by the lab"),
    ),
    StringField('ClientReference',
        searchable=True,
    ),
    StringField('ClientSampleID',
        searchable=True,
    ),

    fields.Many2one(string='LinkedSample',
                   comodel_name='olims.sample',
    ),

    fields.Many2one(string='SampleType',
                   comodel_name='olims.sample_type',
                   readonly=True,
    ),

    fields.Many2one(string='SamplePoint',
                   comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='StorageLocation',
                   comodel_name='olims.storage_location',
    ),

    BooleanField('SamplingWorkflowEnabled',
                 default_method='getSamplingWorkflowEnabledDefault'
    ),

    DateTimeField('DateSampled',
    ),

    StringField('Sampler',
    ),
    DateTimeField('SamplingDate',
                  readonly=True,
    ),

    fields.Many2one(string='SamplingDeviation',
                   comodel_name='olims.sampling_deviation',
    ),


    fields.Many2one(string='SampleCondition',
                   comodel_name='olims.sample_condition',
    ),

    DateTimeField('DateReceived',
        readonly=True,
    ),

    fields.Many2one(string='Client',
           comodel_name = 'olims.client',
       ),
    BooleanField('Composite',
    ),
    DateTimeField('DateExpired',
        readonly=True,
    ),
    DateTimeField('DateDisposed',
        readonly=True,
    ),
    BooleanField('AdHoc',
        default=False,
    ),
    TextField('Remarks',
        searchable=True,
        default_content_type='text/x-web-intelligent',
    ),
    fields.Selection(string='state',
                     selection=SAMPLE_STATES,
                     default='sample_registered',
                     select=True,
                     required=True, readonly=True,
                     copy=False, track_visibility='always'
    ),
    fields.Many2one(string='Analysis_Request',
           comodel_name = 'olims.analysis_request',
    ),
)


class Sample(models.Model, BaseOLiMSModel): #BaseFolder, HistoryAwareMixin
    _name = 'olims.sample'
    _rec_name = "name"

    def compute_smapleId(self):
        for record in self:
            record.SampleID = 'S-0' + str(record.id)

    def compute_smapleName(self):
        for record in self:
            record.name = record.SampleID
    # implements(ISample)
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    def actionToBeSampled(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_sampled',
        })
        return True

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def _getCatalogTool(self):
        from lims.catalog import getCatalog
        return getCatalog(self)

    def Title(self):
        """ Return the Sample ID as title """
        return safe_unicode(self.getId()).encode('utf-8')

    def getSamplingWorkflowEnabledDefault(self):
        return self.bika_setup.getSamplingWorkflowEnabled()

    def getContactTitle(self):
        return ""

    def getClientTitle(self):
        proxies = self.getAnalysisRequests()
        if not proxies:
            return ""
        value = proxies[0].aq_parent.Title()
        return value

    def getProfilesTitle(self):
        return ""

    def getAnalysisCategory(self):
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += list(ar.getAnalyses(full_objects=True))
        value = []
        for analysis in analyses:
            val = analysis.getCategoryTitle()
            if val not in value:
                value.append(val)
        return value

    def getAnalysisService(self):
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += list(ar.getAnalyses(full_objects=True))
        value = []
        for analysis in analyses:
            val = analysis.getServiceTitle()
            if val not in value:
                value.append(val)
        return value

    def getAnalysts(self):
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += list(ar.getAnalyses(full_objects=True))
        value = []
        for analysis in analyses:
            val = analysis.getAnalyst()
            if val not in value:
                value.append(val)
        return value


    def setClientReference(self, value, **kw):
        """ Set the field on Analysis Requests.
        """
        for ar in self.getAnalysisRequests():
            ar.Schema()['ClientReference'].set(ar, value)
        self.Schema()['ClientReference'].set(self, value)

    def setClientSampleID(self, value, **kw):
        """ Set the field on Analysis Requests.
        """
        for ar in self.getAnalysisRequests():
            ar.Schema()['ClientSampleID'].set(ar, value)
        self.Schema()['ClientSampleID'].set(self, value)

    def setAdHoc(self, value, **kw):
        """ Set the field on Analysis Requests.
        """
        for ar in self.getAnalysisRequests():
            ar.Schema()['AdHoc'].set(ar, value)
        self.Schema()['AdHoc'].set(self, value)

    def setComposite(self, value, **kw):
        """ Set the field on Analysis Requests.
        """
        for ar in self.getAnalysisRequests():
            ar.Schema()['Composite'].set(ar, value)
        self.Schema()['Composite'].set(self, value)

    #security.declarePublic('getAnalysisRequests')

    def getAnalysisRequests(self):
        tool = getToolByName(self, REFERENCE_CATALOG)
        ar = ''
        ars = []
        uids = [uid for uid in
                tool.getBackReferences(self, 'AnalysisRequestSample')]
        for uid in uids:
            reference = uid
            ar = tool.lookupObject(reference.sourceUID)
            ars.append(ar)
        return ars

    #security.declarePublic('getAnalyses')

    def getAnalyses(self, contentFilter):
        """ return list of all analyses against this sample
        """
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += ar.getAnalyses(**contentFilter)
        return analyses

    def getSamplers(self):
        return getUsers(self, ['LabManager', 'Sampler'])

    def disposal_date(self):
        """ Calculate the disposal date by returning the latest
            disposal date in this sample's partitions """

        parts = self.objectValues("SamplePartition")
        dates = []
        for part in parts:
            date = part.getDisposalDate()
            if date:
                dates.append(date)
        if dates:
            dis_date = dt2DT(max([DT2dt(date) for date in dates]))
        else:
            dis_date = None
        return dis_date

    def getLastARNumber(self):
        ARs = self.getBackReferences("AnalysisRequestSample")
        prefix = self.getSampleType().getPrefix()
        ar_ids = sorted([AR.id for AR in ARs if AR.id.startswith(prefix)])
        try:
            last_ar_number = int(ar_ids[-1].split("-R")[-1])
        except:
            return 0
        return last_ar_number

    def workflow_script_sample_receive(self,cr,uid,ids,context=None):
        samples = self.pool.get('olims.sample').browse(cr,uid,ids,context)
        ar_ids = []
        for sample in samples:
            if sample.state != "sample_due":
                ids.remove(sample.id)
            else:
                ar_ids.append(sample.Analysis_Request.id)
        datereceive = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'sample_received','DateReceived': datereceive,
        })
        self.pool.get('olims.analysis_request').workflow_script_receive(cr,uid,ar_ids,context)
        return True
    # def workflow_script_receive(self):
        # workflow = getToolByName(self, 'portal_workflow')
        # self.setDateReceived(DateTime())
        # self.reindexObject(idxs=["review_state", "getDateReceived"])
        # # Receive all self partitions that are still 'sample_due'
        # parts = self.objectValues('SamplePartition')
        # sample_due = [sp for sp in parts
        #               if workflow.getInfoFor(sp, 'review_state') == 'sample_due']
        # for sp in sample_due:
        #     workflow.doActionFor(sp, 'receive')
        # # when a self is received, all associated
        # # AnalysisRequests are also transitioned
        # for ar in self.getAnalysisRequests():
        #     doActionFor(ar, "receive")

    def workflow_script_preserve(self):
        """This action can happen in the Sample UI, so we transition all
        self partitions that are still 'to_be_preserved'
        """
        workflow = getToolByName(self, 'portal_workflow')
        parts = self.objectValues("SamplePartition")
        tbs = [sp for sp in parts
               if workflow.getInfoFor(sp, 'review_state') == 'to_be_preserved']
        for sp in tbs:
            doActionFor(sp, "preserve")
        # All associated AnalysisRequests are also transitioned
        for ar in self.getAnalysisRequests():
            doActionFor(ar, "preserve")
            ar.reindexObject()

    def workflow_script_expire(self,cr,uid,ids,context=None):
        samples = self.pool.get('olims.sample').browse(cr,uid,ids,context)
        for sample in samples:
            if sample.state != "sample_received":
                ids.remove(sample.id)
        expired_date = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'expired', 'DateExpired': expired_date,
        })
        return True
        # self.setDateExpired(DateTime())
        # self.reindexObject(idxs=["review_state", "getDateExpired", ])

    def workflow_script_dispose(self,cr,uid,ids,context=None):
        samples = self.pool.get('olims.sample').browse(cr,uid,ids,context)
        for sample in samples:
            if sample.state != "expired":
                ids.remove(sample.id)
        date_disposed = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'disposed', 'DateDisposed': date_disposed
        })
        return True
        # self.setDateDisposed(DateTime())
        # self.reindexObject(idxs=["review_state", "getDateDisposed", ])

    def workflow_script_sample(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'sampled',
        })
        return True

        # if skip(self, "sample"):
        #     return
        # workflow = getToolByName(self, 'portal_workflow')
        # parts = self.objectValues('SamplePartition')
        # # This action can happen in the Sample UI.  So we transition all
        # # partitions that are still 'to_be_sampled'
        # tbs = [sp for sp in parts
        #        if workflow.getInfoFor(sp, 'review_state') == 'to_be_sampled']
        # for sp in tbs:
        #     doActionFor(sp, "sample")
        # # All associated AnalysisRequests are also transitioned
        # for ar in self.getAnalysisRequests():
        #     doActionFor(ar, "sample")
        #     ar.reindexObject()

    def workflow_script_to_be_preserved(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_preserved',
        })
        return True
        # if skip(self, "to_be_preserved"):
        #     return
        # workflow = getToolByName(self, 'portal_workflow')
        # parts = self.objectValues('SamplePartition')
        # # Transition our children
        # tbs = [sp for sp in parts
        #        if workflow.getInfoFor(sp, 'review_state') == 'to_be_preserved']
        # for sp in tbs:
        #     doActionFor(sp, "to_be_preserved")
        # # All associated AnalysisRequests are also transitioned
        # for ar in self.getAnalysisRequests():
        #     doActionFor(ar, "to_be_preserved")
        #     ar.reindexObject()

    def workflow_script_sample_due(self,cr,uid,ids,context=None):
        samples = self.pool.get('olims.sample').browse(cr,uid,ids,context)
        ar_ids = []
        for sample in samples:
            if sample.state != "to_be_sampled":
                ids.remove(sample.id)
            else:
                ar_ids.append(sample.Analysis_Request.id)
        self.write(cr, uid, ids, {
            'state': 'sample_due',
        })
        self.pool.get('olims.analysis_request').workflow_script_sample_due(cr,uid,ar_ids,context)
        return True
        # if skip(self, "sample_due"):
        #     return
        # # All associated AnalysisRequests are also transitioned
        # for ar in self.getAnalysisRequests():
        #     doActionFor(ar, "sample_due")
        #     ar.reindexObject()

    def workflow_script_reinstate(self):
        if skip(self, "reinstate"):
            return
        workflow = getToolByName(self, 'portal_workflow')
        parts = self.objectValues('SamplePartition')
        self.reindexObject(idxs=["cancellation_state", ])
        # Re-instate all self partitions
        for sp in [sp for sp in parts
                   if workflow.getInfoFor(sp, 'cancellation_state') == 'cancelled']:
            workflow.doActionFor(sp, 'reinstate')
        # reinstate all ARs for this self.
        ars = self.getAnalysisRequests()
        for ar in ars:
            if not skip(ar, "reinstate", peek=True):
                ar_state = workflow.getInfoFor(ar, 'cancellation_state')
                if ar_state == 'cancelled':
                    workflow.doActionFor(ar, 'reinstate')

    def workflow_script_cancel(self):
        if skip(self, "cancel"):
            return
        workflow = getToolByName(self, 'portal_workflow')
        parts = self.objectValues('SamplePartition')
        self.reindexObject(idxs=["cancellation_state", ])
        # Cancel all partitions
        for sp in [sp for sp in parts
                   if workflow.getInfoFor(sp, 'cancellation_state') == 'active']:
            workflow.doActionFor(sp, 'cancel')
        # cancel all ARs for this self.
        ars = self.getAnalysisRequests()
        for ar in ars:
            if not skip(ar, "cancel", peek=True):
                ar_state = workflow.getInfoFor(ar, 'cancellation_state')
                if ar_state == 'active':
                    workflow.doActionFor(ar, 'cancel')

    def guard_receive_transition(self):
        """Prevent the receive transition from being available:
        - if object is cancelled
        - if any related ARs have field analyses with no result.
        """
        # Can't do anything to the object if it's cancelled
        if not isBasicTransitionAllowed(self):
            return False
        # check if any related ARs have field analyses with no result.
        for ar in self.getAnalysisRequests():
            field_analyses = ar.getAnalyses(getPointOfCapture='field',
                                            full_objects=True)
            no_results = [a for a in field_analyses if a.getResult() == '']
            if no_results:
                return False
        return True


Sample.initialze(schema)