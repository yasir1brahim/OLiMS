""" An AnalysisRequest report, containing the report itself in pdf and html
    format. Also, includes information about the date when was published, from
    who, the report recipients (and their emails) and the publication mode
# """
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from openerp.tools.translate import _


schema = (
        fields.Many2one(string='AnalysisRequest',
                    comodel_name='olims.analysis_request',
                    required=True

    ),
    fields.Binary(string='Pdf'),
    StringField('Html',
    ),
    StringField('SMS',
    ),
)



class ARReport(models.Model, BaseOLiMSModel):
    _name='olims.ar_report'

ARReport.initialze(schema)