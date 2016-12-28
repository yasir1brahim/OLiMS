from openerp import fields, models, api
from openerp.tools.translate import _
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.integer_field import IntegerField
from fields.widget.widget import TextAreaWidget,StringWidget
from openerp.tools.translate import _
schema = (StringField('Title',
              required=1,        
    ),
    TextField('Description',
        widget = TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    fields.One2many(string='Analysis_Service',
                    comodel_name='olims.worksheet_analysis_service',
                    inverse_name='worksheet_analysis_id',
                    required=True,
                    help='Select which Analyses should be included on the Worksheet',
                    compute="_get_control_analysis"
    ),
    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
        required = False,
        help='Select the preferred instrument'
    ),
    fields.One2many(string='Layout',
                    comodel_name='olims.ws_template_layout',
                    inverse_name='worksheet_layout_id',
    ),
    StringField(string="name"),
    IntegerField('number_of_pos'),
    fields.Many2many(comodel_name="olims.reference_definition", string="ControlAnalysis"),
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
        StringField(string="name"),
        FixedPointField(string="Target"),
        FixedPointField(string="Lower_Value"),
        FixedPointField(string="Upper_Value"),
        StringField(string="Calculation",
            compute="_ComputeAnalysisServiceFields"
        ),
        fields.Many2one(string='Category',
                    comodel_name='olims.analysis_category'),
        fields.Many2one('olims.worksheet',ondelete='set null', string="ws_temp_service_reference_id"),
        FixedPointField(string="Result"),
)

class WorksheetTemplate(models.Model, BaseOLiMSModel): #BaseContent
    _name = 'olims.worksheet_template'
    _rec_name = 'Title'

    @api.multi
    def add_layout_data(self):
        if self.number_of_pos > 0:
            ws_template_obj = self.search([('id','=', self.id)])
            self.write({"Layout":[(2, layout.id) for layout in ws_template_obj.Layout]})
            pos = 0
            for index in range(0, self.number_of_pos):
                pos += 1
                self.write({"Layout":[[0,0, {"analysis_type":'analysis','position': pos}]]})
    
        #Get the view ref. by paasing module & name of the required form
        view_ref = self.env['ir.model.data'].get_object_reference('olims', 'olims_worksheet_template_form_view')
        view_id = view_ref[1] if view_ref else False

        #Let's prepare a dictionary with all necessary info to open current form in edit mode
        res = {
           'type': 'ir.actions.act_window',
           'name': _('worksheet_template.form'),
           'res_model': 'olims.worksheet_template',
           'view_type': 'form',
           'view_mode': 'form',
           'view_id': view_id,
           'target': 'current',
           'res_id': self.id,
           'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
        }

        return res

    @api.depends("ControlAnalysis")
    def _get_control_analysis(self):
        for rec in  self.ControlAnalysis:
            for item in rec.Reference_Results:
                values = {
                    "worksheet_analysis_id": self.id,
                    "name": rec.name,
                    "Category": item.Category.id,
                    "Service": item.Service.id,
                    "Lower_Value": item.Min,
                    "Upper_Value": item.Max,
                    "Target": item.Permitted_Error,
                    "Result": item.Expected_Result
                    }
                self.Analysis_Service |= self.env['olims.worksheet_analysis_service'].create(values)

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

class WorkSheetTemplateLayout(models.Model):
    _name = "olims.ws_template_layout"

    analysis_type = fields.Selection(string="Analysis Type",
        selection=[
            ('analysis', 'Analysis'),('blank', 'Blank'),
            ('control', 'Control'), ('duplicate', 'Duplicate')],
        default='analysis', select=True,
        copy=False, track_visibility='always'
        )
    position = fields.Integer('pos')
    ref_definition = fields.Many2one(string='Reference Definition',
        comodel_name="olims.reference_definition")
    dup_of = fields.Selection(string='Dup of',
        selection=[('0','0'), ('1','1'),
        ('2','2')],
        default='0', select=True,
        copy=False, track_visibility='always')
    worksheet_layout_id = fields.Many2one(string="WS Layout",
        comodel_name="olims.worksheet_template")

    @api.onchange('analysis_type')
    def get_refrence_definition(self):
        selection = []
        if self.analysis_type == "blank":
            return {'domain':{'ref_definition':[('Blank', '=', True)]}}
        elif self.analysis_type == "control":
            return {'domain':{'ref_definition':[('Blank', '=', False)]}}

WorksheetTemplate.initialze(schema)
WorksheetAnalysisService.initialze(schema_worksheet_analysis_servive)
