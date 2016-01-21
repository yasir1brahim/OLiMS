from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, DateTimeWidget,TextAreaWidget
from lims import bikaMessageFactory as _

BATCHE_STATES = (
    ('open','Open'), ('closed','Closed'),
    )
schema = (StringField(
        'Title',
        searchable=True,
        required=True,
        validators=('uniquefieldvalidator',),
        widget=StringWidget(
            visible=False,
            label=_("Batch ID"),
        )
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = ('Used in item listings and search results.'),
                            )
    ),

    fields.Many2one(string='Client',
                    comodel_name='olims.client',
                    required=False,
    ),

    StringField(
        'ClientBatchID',
        searchable=True,
        required=0,
        widget=StringWidget(
            label=_("Client Batch ID")
        )
    ),
    DateTimeField(
        'BatchDate',
        required=False,
        widget=DateTimeWidget(
            label=_('Date'),
        ),
    ),
          
    fields.Many2many(string='BatchLabels',
                   comodel_name='olims.batch_label',
    ),

    fields.Many2many(string='InheritedObjects',
    comodel_name='olims.inherit_from_batch',
    relation='inheritform_batch',
    required=False,
    ondelete='cascade'
    ),
    StringField(string='BatchId',compute='_ComputeBatchId'),
    fields.Selection(string='state',selection=BATCHE_STATES,
        default='open', select=True,
        required=True, readonly=True,
        copy=False, track_visibility='always'
        ),

)


class Batch(models.Model, BaseOLiMSModel): #ATFolder
    _name='olims.batch'
    _rec_name = 'Title'

    def _ComputeBatchId(self):
        for record in self:
            batchidstring = 'B-0' + str(record.id)
            record.BatchId = batchidstring

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        """ Return the Batch ID if title is not defined """
        titlefield = self.Schema().getField('title')
        if titlefield.widget.visible:
            return safe_unicode(self.title).encode('utf-8')
        else:
            return safe_unicode(self.id).encode('utf-8')

    def _getCatalogTool(self):
        from lims.catalog import getCatalog
        return getCatalog(self)

    def getClient(self):
        """ Retrieves the Client for which the current Batch is attached to
            Tries to retrieve the Client from the Schema property, but if not
            found, searches for linked ARs and retrieve the Client from the
            first one. If the Batch has no client, returns None.
        """
        client = self.Schema().getField('Client').get(self)
        if client:
            return client
        return client

    def getClientTitle(self):
        client = self.getClient()
        if client:
            return client.Title()
        return ""

    def getContactTitle(self):
        return ""

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

    #security.declarePublic('getBatchID')

    def getBatchID(self):
        return self.getId()

    def BatchLabelVocabulary(self):
        """ return all batch labels """
        bsc = getToolByName(self, 'bika_setup_catalog')
        ret = []
        for p in bsc(portal_type='BatchLabel',
                     inactive_state='active',
                     sort_on='sortable_title'):
            ret.append((p.UID, p.Title))
        return DisplayList(ret)

    def getAnalysisRequests(self):
        """ Return all the Analysis Requests linked to the Batch
        """
        return self.getBackReferences("AnalysisRequestBatch")

    def isOpen(self):
        """ Returns true if the Batch is in 'open' state
        """
        revstatus = getCurrentState(self, StateFlow.review)
        canstatus = getCurrentState(self, StateFlow.cancellation)
        return revstatus == BatchState.open \
            and canstatus == CancellationState.active

    def getLabelNames(self):
        uc = getToolByName(self, 'uid_catalog')
        uids = [uid for uid in self.Schema().getField('BatchLabels').get(self)]
        labels = [label.getObject().title for label in uc(UID=uids)]
        return labels

    def workflow_guard_open(self, cr, uid, ids, context=None):
        """ Permitted if current review_state is 'closed' or 'cancelled'
            The open transition is already controlled by 'Bika: Reopen Batch'
            permission, but left here for security reasons and also for the
            capability of being expanded/overrided by child products or
            instance-specific-needs.
        """
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)
        # revstatus = getCurrentState(self, StateFlow.review)
        # canstatus = getCurrentState(self, StateFlow.cancellation)
        # return revstatus == BatchState.closed \
        #     and canstatus == CancellationState.active

    def workflow_guard_close(self, cr, uid, ids, context=None):
        """ Permitted if current review_state is 'open'.
            The close transition is already controlled by 'Bika: Close Batch'
            permission, but left here for security reasons and also for the
            capability of being expanded/overrided by child products or
            instance-specific needs.
        """
        return self.write(cr, uid, ids, {'state': 'closed'}, context=context)
        # revstatus = getCurrentState(self, StateFlow.review)
        # canstatus = getCurrentState(self, StateFlow.cancellation)
        # return revstatus == BatchState.open \
        #     and canstatus == CancellationState.active


#registerType(Batch, PROJECTNAME)
Batch.initialze(schema)

# @indexer(IBatch)
# def BatchDate(instance):
#     return instance.Schema().getField('BatchDate').get(instance)
