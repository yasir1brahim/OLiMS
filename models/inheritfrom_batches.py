from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField

schema = (
    fields.Selection(string='Title',selection='RetrieveBatchesAndAnalysisRequests'),
    fields.Selection(string='ObjectId',selection='RetrieveBatchesAndAnalysisRequestsTitles'
    ),
    StringField('Description',
    ),
)
title_dict = {}
id_dict = {}
description_dict = {}
class InheritFromBatch(models.Model, BaseOLiMSModel):
    _name = 'olims.inherit_from_batch'
    @api.multi
    def RetrieveBatchesAndAnalysisRequests(self):
        batch_object = self.env['olims.batch']
        analysis_request_object = self.env['olims.analysis_request']

        batch_object_ids = batch_object.search([('id', '>', 0)])
        analysis_request_object_ids = analysis_request_object.search([('id', '>', 0)])
        if batch_object_ids:
            for obj in batch_object_ids:
                batch = batch_object.browse(obj.id)
                batch_name = unicode(batch.Title).encode('utf-8')
                batchid = unicode(batch.BatchId).encode('utf-8')
                batchdesc = batch.Description
                id_dict.update({batchid : batchid})
                title_dict.update({ batchid: batch_name})
                description_dict.update({ batchdesc: batchid})

        if analysis_request_object_ids:
            for request_id in analysis_request_object_ids:
                analysis_request = analysis_request_object.browse(request_id.id)
                requestid = unicode(analysis_request.RequestID).encode('utf-8')
                id_dict.update({requestid : requestid})
                title_dict.update({requestid : requestid})
                clientname = unicode(analysis_request.Client.Name).encode('utf-8')
                requestdesc = requestid + ' ' + clientname
                description_dict.update({ requestdesc: requestid})
        selection = id_dict.items()
        return selection
    @api.multi
    def RetrieveBatchesAndAnalysisRequestsTitles(self):
        selection = title_dict.items()
        return selection

    @api.onchange('Title')
    def ChangeObjectId(self):
        self.ObjectId = self.Title
        if self.Title is not False:
            self.Description = description_dict.keys()[description_dict.values().index(self.Title)]

    @api.onchange('ObjectId')
    def ChangeTitle(self):
        self.Title = self.ObjectId
        if self.Title is not False:
            self.Description = description_dict.keys()[description_dict.values().index(self.Title)]

InheritFromBatch.initialze(schema)