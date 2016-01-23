from openerp import fields, models, api
from openerp.tools.translate import _
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget,StringWidget
schema = (StringField('Title',
              required=1,        
    ),
    TextField('Description',
        widget = TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    fields.One2many(string='Analysis Service',
                    comodel_name='olims.worksheet_analysis_service',
                    inverse_name='worksheet_analysis_id',
                    required=True,
                    help='Select which Analyses should be included on the Worksheet',
    ),
    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
        required = False,
        help='Select the preferred instrument'
    ),
)
schema_worksheet_analysis_servive = (fields.Many2one(string="worksheet_analysis_id",
        comodel_name="olims.worksheet_template"
        ),
        fields.Many2one(string="Service",
            comodel_name="olims.analysis_service",
            domain="[('category', '=', Category)]",
        ),
        StringField(string="Keyword",
            compute="_ComputeAnalysisServiceFields"
        ),
        StringField(string="Method",
            compute="_ComputeAnalysisServiceFields"
        ),
        StringField(string="Calculation",
            compute="_ComputeAnalysisServiceFields"
        ),
        fields.Many2one(string='Category',
                    comodel_name='olims.analysis_category'),
)

class WorksheetTemplate(models.Model, BaseOLiMSModel): #BaseContent
    _name = 'olims.worksheet_template'
    _rec_name = 'Title'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def getAnalysisTypes(self):
        """ return Analysis type displaylist """
        return ANALYSIS_TYPES

    def getInstruments(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [('', '')] + [(o.UID, o.Title) for o in
                               bsc(portal_type = 'Instrument',
                                   inactive_state = 'active')]
        o = self.getInstrument()
        if o and o.UID() not in [i[0] for i in items]:
            items.append((o.UID(), o.Title()))
        items.sort(lambda x, y: cmp(x[1], y[1]))
        return DisplayList(list(items))

class WorksheetAnalysisService(models.Model, BaseOLiMSModel):
    _name = 'olims.worksheet_analysis_service'

    @api.onchange('Service')
    def _ComputeAnalysisServiceFields(self):
        for items in self:
            items.Keyword = items.Service.Keyword
            items.Method = items.Service._Method.getMethod()
            items.Calculation = items.Service._Calculation.getCalculation()

WorksheetTemplate.initialze(schema)
WorksheetAnalysisService.initialze(schema_worksheet_analysis_servive)
