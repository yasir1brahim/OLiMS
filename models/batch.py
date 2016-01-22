from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, DateTimeWidget,TextAreaWidget
from openerp.tools.translate import _

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

    def workflow_guard_open(self, cr, uid, ids, context=None):
        """ Permitted if current review_state is 'closed' or 'cancelled'
            The open transition is already controlled by 'Bika: Reopen Batch'
            permission, but left here for security reasons and also for the
            capability of being expanded/overrided by child products or
            instance-specific-needs.
        """
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def workflow_guard_close(self, cr, uid, ids, context=None):
        """ Permitted if current review_state is 'open'.
            The close transition is already controlled by 'Bika: Close Batch'
            permission, but left here for security reasons and also for the
            capability of being expanded/overrided by child products or
            instance-specific needs.
        """
        return self.write(cr, uid, ids, {'state': 'closed'}, context=context)


Batch.initialze(schema)
