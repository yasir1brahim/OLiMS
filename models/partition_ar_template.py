
from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel

schema = (
          fields.Many2one(string='Container', comodel_name ='olims.container'),
          fields.Many2one(string='Preservation', comodel_name ='olims.preservation'),
          fields.Char('Partition'),
          )
ar_partition_schema = (fields.Char('State'),
                       fields.Many2one(string='analysis_request_id', comodel_name ='olims.analysis_request'),
#                        fields.Char('partition_id')
                       )
ar_sample_partition_schema = (fields.Char('State'),
                       fields.Many2one(string='analysis_request_id', comodel_name ='olims.analysis_request'),
                       fields.Char('Preserver',
                                   readonly=True),
                       fields.Datetime('Date Preserved',
                                       readonly=True),
                       )
class PartitionARTemplate(models.Model, BaseOLiMSModel): 
    _name='olims.partition_ar_template'
    _rec_name = 'Partition'

class ARPartition(models.Model, BaseOLiMSModel):
    _inherit = 'olims.partition_ar_template'
    _name='olims.ar_partition'

#     ToDO
#     @api.one
#     def write(self,data):
#         print "test"
#         ar_partition = self.env['olims.ar_sample_partition'].search([('analysis_request_id','=', self.analysis_request_id.id)])
#         ar_partition.write(data)
#         res = super(ARPartition, self).write(data)
#         return res
    
class ARSamplePartition(models.Model, BaseOLiMSModel):
    _inherit = 'olims.partition_ar_template'
    _name='olims.ar_sample_partition'

    @api.multi
    def write(self,data):
        ar_partition_object = self.env['olims.ar_partition'].search([('analysis_request_id','=', self.analysis_request_id.id)])
        ar_partition_object.write(data)
        res = super(ARSamplePartition, self).write(data)
        return res
        
        

PartitionARTemplate.initialze(schema)
ARPartition.initialze(ar_partition_schema)
ARSamplePartition.initialze(ar_sample_partition_schema)