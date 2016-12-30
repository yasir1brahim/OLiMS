"""The request for analysis by a client. It contains analysis instances.
"""
import datetime
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.date_time_field import DateTimeField
from fields.fixed_point_field import FixedPointField
from fields.integer_field import IntegerField
from fields.widget.widget import StringWidget, TextAreaWidget, \
                                BooleanWidget, DateTimeWidget, \
                                DecimalWidget, RichWidget
from openerp import fields, models, api
from openerp.tools.translate import _
from openerp.exceptions import Warning
AR_STATES = (
    ('sample_registered','Sample Registered'),
    ('not_requested','Not Requested'),
    ('to_be_sampled','To Be Labeled'),
    ('sampled','Sampled'),
    ('to_be_preserved','To Be Preserved'),
    ('sample_due','Sample Due'),
    ('sample_received','Received'),
    ('attachment_due','Attachment Outstanding'),
    ('to_be_verified','To be verified'),
    ('verified','Verified'),
    ('published','Published'),
    ('invalid','Invalid'),
    ('cancelled', 'Canceled')
    )
SELECT_OPTIONS=(
    ('0','Select-to-copy'),
    ('1', '2'),
    ('2', '3'),
    ('3', '4')
    )

schema = (fields.Char(string='RequestID',
                      compute='compute_analysisRequestId',
                      store=True
        ),
    fields.Many2one(string='Client',
                    comodel_name='olims.client',
                    required=False,

    ),
    fields.Many2many(string='Contact',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=True
    ),
    fields.Many2many(string='Contact1',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact2',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact3',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact1',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact2',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact3',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(
        string='CCEmails',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails1',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails2',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails3',
        comodel_name="olims.email"
    ),
    fields.Char(string='Sample',
                        compute='Compute_AnalysisSample',

    ),
    fields.Many2one(string='Sample_id',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id1',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id2',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id3',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Batch',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch1',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch2',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch3',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='SubGroup',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup1',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup2',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup3',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='Template',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template1',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template2',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template3',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='AnalysisProfile',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2one(string='AnalysisProfile1',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2one(string='AnalysisProfile2',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2one(string='AnalysisProfile3',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.One2many(string='Partition',
                     comodel_name='olims.ar_partition',
                    inverse_name='analysis_request_id',
    ),
    fields.One2many(string='Sample Partition',
                     comodel_name='olims.ar_sample_partition',
                    inverse_name='analysis_request_id',
    ),
    fields.One2many(string='Analyses',
                     comodel_name='olims.ar_analysis',
                    inverse_name='analysis_request_id',
    ),
    # Sample field
    DateTimeField('DateSampled',
    ),
    # Sample field
    fields.Many2one(string='Sampler',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler1',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler2',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler3',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    DateTimeField(
        'SamplingDate',
        required=1,
    ),
    DateTimeField(
        'SamplingDate1',
        required=0,
    ),
    DateTimeField(
        'SamplingDate2',
        required=0,
    ),
    DateTimeField(
        'SamplingDate3',
        required=0,
    ),
    fields.Many2one(string='SampleType',
                        comodel_name='olims.sample_type',
                        required=True

    ),
    fields.Many2one(string='SampleType1',
                        comodel_name='olims.sample_type',
                        required=False

    ),
    fields.Many2one(string='SampleType2',
                        comodel_name='olims.sample_type',
                        required=False

    ),
    fields.Many2one(string='SampleType3',
                        comodel_name='olims.sample_type',
                        required=False

    ),
    fields.Many2one(string='Specification',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification1',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification2',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification3',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='SamplePoint',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint1',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint2',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint3',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='StorageLocation',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation1',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation2',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation3',
                        comodel_name='olims.storage_location',

    ),
    StringField(
        'LotID',
    ),
    StringField(
        'LotID1',
    ),
    StringField(
        'LotID2',
    ),
    StringField(
        'LotID3',
    ),
    # Sample field
    StringField(
        'ClientReference',
        searchable=True,
    ),
    StringField(
        'ClientReference1',
        searchable=True,
    ),
    StringField(
        'ClientReference2',
        searchable=True,
    ),
    StringField(
        'ClientReference3',
        searchable=True,
    ),
    # Sample field
    StringField(
        'ClientSampleID',
        searchable=True,
    ),
    StringField(
        'ClientSampleID1',
        searchable=True,
    ),
    StringField(
        'ClientSampleID2',
        searchable=True,
    ),
    StringField(
        'ClientSampleID3',
        searchable=True,
    ),
    fields.Many2one(string='SamplingDeviation',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation1',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation2',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation3',
                        comodel_name='olims.sampling_deviation',

    ),
#     # Sample field
    fields.Many2one(string='SampleCondition',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition1',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition2',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition3',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='DefaultContainerType',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType1',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType2',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType3',
                        comodel_name='olims.container_type',

    ),
    # Sample field
    BooleanField(
        'AdHoc',
        default=False,
    ),
    BooleanField(
        'AdHoc1',
        default=False,
    ),
    BooleanField(
        'AdHoc2',
        default=False,
    ),
    BooleanField(
        'AdHoc3',
        default=False,
    ),
    # Sample field
    BooleanField(
        'Composite',
        default=False,
    ),
    BooleanField(
        'Composite1',
        default=False,
    ),
    BooleanField(
        'Composite2',
        default=False,
    ),
    BooleanField(
        'Composite3',
        default=False,
    ),
    BooleanField(
        'ReportDryMatter',
        default=False,
    ),
    BooleanField(
        'ReportDryMatter1',
        default=False,
    ),
    BooleanField(
        'ReportDryMatter2',
        default=False,
    ),
    BooleanField(
        'ReportDryMatter3',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude1',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude2',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude3',
        default=False,
    ),
    DateTimeField(
        'DateReceived',
    ),
    DateTimeField(
        'DatePublished',
    ),
    DateTimeField(
        'DateDue',
    ),
    TextField(
        string='Remarks',
        searchable=True,
    ),
    FixedPointField(
        'MemberDiscount',
    ),
    fields.Many2one(string='ChildAnalysisRequest',
                        comodel_name='olims.analysis_request',

    ),
    fields.Many2one(string='ParentAnalysisRequest',
                        comodel_name='olims.analysis_request',

    ),
    fields.Many2one(string='Priority',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority1',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority2',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority3',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    TextField(
        string='ResultsInterpretation',
    ),
    fields.One2many(string='LabService',
                     comodel_name='olims.field_analysis_service',
                    inverse_name='ar_service_lab_id',
    ),
    fields.One2many(string='FieldService',
                     comodel_name='olims.field_analysis_service',
                    inverse_name='analysis_request_id',
    ),
    fields.Selection(string='adjustment_option',
                     selection=(('percentage','Percentage'),
                                ('amount','Amount')
                                ),
                     default='percentage',
    ),
    fields.Char(string="Adjustment_Remarks"),
    fields.Float(string='Adjustment',
                 default=0.00,
    ),
    fields.Float(string='Discount',
                 default=0.00,
    ),
    fields.Float(string='Discount1',
                 default=0.00,
    ),
    fields.Float(string='Discount2',
                 default=0.00,
    ),
    fields.Float(string='Discount3',
                 default=0.00,
    ),
    fields.Float(string='Subtotal',
                 default=0.00,
    ),
    fields.Float(string='Subtotal1',
                 default=0.00,
    ),
    fields.Float(string='Subtotal2',
                 default=0.00,
    ),
    fields.Float(string='Subtotal3',
                 default=0.00,
    ),
    fields.Float(string='VAT',
                 default=0.00,
    ),
    fields.Float(string='VAT1',
                 default=0.00,
    ),
    fields.Float(string='VAT2',
                 default=0.00,
    ),
    fields.Float(string='VAT3',
                 default=0.00,
    ),
    fields.Float(string='Total',
                 default=0.00,
    ),
    fields.Float(string='Total1',
                 default=0.00,
    ),
    fields.Float(string='Total2',
                 default=0.00,
    ),
    fields.Float(string='Total3',
                 default=0.00,
    ),
    fields.Selection(string='state',
                     selection=AR_STATES,
                     default='sample_registered',
                     select=True,
                     required=True, readonly=True,
                     copy=False, track_visibility='always'
    ),
    fields.Selection(string='result_option',
                     selection=(('general','General'),
                                ('sampling','Sampling')
                                ),
                     default='general',
    ),
    fields.One2many(string="Field_Manage_Result",
        comodel_name="olims.manage_analyses",
        inverse_name="manage_analysis_id"),
    fields.One2many(string="Lab_Manage_Result",
        comodel_name="olims.manage_analyses",
        inverse_name="lab_manage_analysis_id"),
    fields.One2many(string="AddAnalysis",
        comodel_name="olims.add_analysis",
        inverse_name="add_analysis_id"),
    fields.Boolean(
        string='CopyContact',
        default=False,
    ),
    fields.Boolean(
        string='CopyCCContact',
        default=False,
    ),
    fields.Boolean(
        string='CopyEmail',
        default=False,
    ),
    fields.Boolean(
        string='Copysample',
        default=False,
    ),
    fields.Boolean(
        string='Copybatch',
        default=False,
    ),
    fields.Boolean(
        string='Copysubgroup',
        default=False,
    ),
    fields.Boolean(
        string='Copytemplate',
        default=False,
    ),
    fields.Boolean(
        string='Copyprofile',
        default=False,
    ),
    fields.Boolean(
        string='Copysmaplingdate',
        default=False,
    ),
    fields.Boolean(
        string='Copysampler',
        default=False,
    ),
    fields.Boolean(
        string='Copysampletype',
        default=False,
    ),
    fields.Boolean(
        string='Copyspecification',
        default=False,
    ),
    fields.Boolean(
        string='Copysamplepoint',
        default=False,
    ),
    fields.Boolean(
        string='Copystorage',
        default=False,
    ),
    fields.Boolean(
        string='CopyClientReference',
        default=False,
    ),
    fields.Boolean(
        string='CopySamplingDeviation',
        default=False,
    ),
    fields.Boolean(
        string='CopySampleCondition',
        default=False,
    ),
    fields.Boolean(
        string='CopyDefaultContainerType',
        default=False,
    ),
    fields.Boolean(
        string='CopyAdHoc',
        default=False,
    ),
    fields.Boolean(
        string='CopyComposite',
        default=False,
    ),
    fields.Boolean(
        string='CopyReportDryMatter',
        default=False,
    ),
    fields.Boolean(
        string='CopyInvoiceExclude',
        default=False,
    ),
    fields.Boolean(
        string='CopyPriority',
        default=False,
    ),
    fields.Boolean(
        string='CopyDiscount',
        default=False,
    ),
    fields.Boolean(
        string='CopySubtotal',
        default=False,
    ),
    fields.Boolean(
        string='CopyVAT',
        default=False,
    ),
    fields.Boolean(
        string='CopyTotal',
        default=False,
    ),
    fields.Selection(
        string='Copy',
        selection=SELECT_OPTIONS,
        default='0',
        select=True,
    ),
    fields.Many2one(string="ar_invoice_id",
        comodel_name="olims.ar_invoice", ondelete='set null'),
    fields.Boolean(string='is_billed',
        default=False),
    fields.Char(string="billing_status",compute='set_billing_status', store=True),
)
schema_analysis = (fields.Many2one(string='Service',
                    comodel_name='olims.analysis_service',
                    relation='analysisservice_analysisrequest',
                    domain="[('PointOfCapture', '=', 'field'),('category', '=', Category)]"
    ),
    fields.Many2one(string='LabService',
                     comodel_name='olims.analysis_service',
                    relation='analysisservice_analysisrequest',
                    domain="[('PointOfCapture', '=', 'lab'),('category', '=', Category)]"
    ),
    StringField('CommercialID',
        compute='_ComputeFieldResults',
        widget=StringWidget(
            label=_("Commercial ID"),
            description=_("The service's commercial ID for accounting purposes")
        ),
    ),
    StringField('ProtocolID',
        compute='_ComputeFieldResults',
        widget=StringWidget(
            label=_("Protocol ID"),
            description=_("The service's analytical protocol ID")
        ),
    ),
    fields.Many2one(string='analysis_request_id',
        comodel_name='olims.analysis_request',
        ondelete='cascade'
    ),
    fields.Many2one(string='ar_service_lab_id',
        comodel_name='olims.analysis_request',
        ondelete='cascade'
    ),
    FixedPointField(string="Error"),
    FixedPointField(string="Min"),
    FixedPointField(string="Max"),
    fields.Many2one(string='Category',
        comodel_name='olims.analysis_category'),
)

manage_result_schema = (
    StringField(string="Partition"),
    FixedPointField(string="Result"),
    BooleanField('+-', default=False),
    DateTimeField('Capture'),
    DateTimeField('Due Date'),
    fields.Char(string="Result_string"),
    # fields.Many2one(string="Result",
    #     comodel_name="olims.result_option"),
    fields.Many2one(string="Instrument",
        comodel_name="olims.instrument"),
    fields.Many2one(string="Analyst",
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,22])]"),
    StringField('Specifications'),
    IntegerField('Position'),
    fields.Many2one(string='manage_analysis_id',
        comodel_name='olims.analysis_request',
        # domain="[('state', '=', 'sample_received')]",
        ondelete='cascade'
    ),
    fields.Many2one(string='lab_manage_analysis_id',
        comodel_name='olims.analysis_request',
        # domain="[('state', '=', 'sample_received')]",
        ondelete='cascade'
    ),
    fields.Many2one(string='Method',
        comodel_name='olims.method',
        ),
    fields.Many2one(string='Category',
        comodel_name='olims.analysis_category'),
    fields.Selection(string='state',
                     selection=AR_STATES,
                     default='sample_received',
                     select=True,
                     readonly=True,
                     copy=False, track_visibility='always'
    ),
    fields.Char(string="flag", compute="insert_flag")
    )

class AnalysisRequest(models.Model, BaseOLiMSModel): #(BaseFolder):
    _name = 'olims.analysis_request'
    _rec_name = "RequestID"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.depends("Contact")
    def compute_analysisRequestId(self):
        for record in self:
            record.RequestID = 'R-0' + str(record.id)
    @api.multi
    def Compute_AnalysisSample(self):
        for record in self:
            if not record.Sample_id:
                sample = self.env["olims.sample"].search([('Analysis_Request', '=', record.id)])
                record.Sample = sample.SampleID
                record.Sample_id = sample.id
            else:
                record.Sample = record.Sample_id.SampleID

    @api.model
    def create(self, values):
        """Overwrite the create method of Odoo and create other models data
           with their fields
        """
        list_of_dicts = []
        count = 0
        analysis_request_0_dict, analysis_request_1_dict, analysis_request_2_dict, analysis_request_3_dict = self.get_fields_value_dicts(
            values)
        data, data1, data2, data3,\
        field_result_list, lab_result_list,\
        field_result_list_profile1, lab_result_list_profile1,\
        field_result_list_profile2, lab_result_list_profile2,\
        field_result_list_profile3, lab_result_list_profile3 = self.create_field_and_lab_analyses(values)

        if not analysis_request_0_dict.get("Field_Manage_Result",None) and not analysis_request_0_dict.get("Lab_Manage_Result",None):
            analysis_request_0_dict.update({"Field_Manage_Result": field_result_list,
                "Lab_Manage_Result": lab_result_list})
        if not analysis_request_1_dict.get("Field_Manage_Result",None) and not analysis_request_1_dict.get("Lab_Manage_Result",None):
            analysis_request_1_dict.update({"Field_Manage_Result": field_result_list_profile1,
                "Lab_Manage_Result": lab_result_list_profile1})
        if not analysis_request_2_dict.get("Field_Manage_Result",None) and not analysis_request_2_dict.get("Lab_Manage_Result",None):
            analysis_request_2_dict.update({"Field_Manage_Result": field_result_list_profile2,
                "Lab_Manage_Result": lab_result_list_profile2})
        if not analysis_request_3_dict.get("Field_Manage_Result",None) and not analysis_request_3_dict.get("Lab_Manage_Result",None):
            analysis_request_3_dict.update({"Field_Manage_Result": field_result_list_profile3,
                                        "Lab_Manage_Result": lab_result_list_profile3})

        list_of_dicts.append(analysis_request_0_dict)
        list_of_dicts.append(analysis_request_1_dict)
        list_of_dicts.append(analysis_request_2_dict)
        list_of_dicts.append(analysis_request_3_dict)

        for ar_values in list_of_dicts:
            if ar_values.get("Contact") and ar_values.get('SamplingDate') and ar_values.get('SampleType'):
                res = super(AnalysisRequest, self).create(ar_values)
                if not ar_values.get("Sample_id",None):
                    new_sample = self.create_sample(ar_values, res)
                    analysis_object = super(AnalysisRequest, self).search([('id', '=',res.id)])
                    analysis_object.write({"Sample_id":new_sample.id})

                ar_p = self.create_ar_partitions(res)
                if not ar_values.get("Analyses", None):
                    ar_analysis_object = self.env['olims.ar_analysis']
                    if count == 0:
                        for rec in data:
                            self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                    elif count == 1:
                        for rec in data1:
                            self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                    elif count == 2:
                        for rec in data2:
                            self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                    elif count == 3:
                        for rec in data3:
                            self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                    count += 1
        return res

    def create_analyses(self, ar_analysis_object, ar_p, ar_values, rec, res):
        if "LabService" in rec[2]:
            serv_temp = rec[2]['LabService']
        elif "Service" in rec[2]:
            serv_temp = rec[2]['Service']
        analyses_values = {
            'Priority': ar_values.get('Priority'),
            'Partition': ar_p.id,
            'analysis_request_id': res.id,
            'Category': rec[2]['Category'],
            'Services': serv_temp,
            'Min': rec[2]['Min'],
            'Max': rec[2]['Max'],
            'Error': rec[2]['Error']
        }
        manage_ar_obj = self.env["olims.manage_analyses"].search(["|",("manage_analysis_id","=",res.id),
                    ("lab_manage_analysis_id","=",res.id),"|",("Service","=",serv_temp)
                    ,("LabService","=",serv_temp)])
        manage_ar_obj.write({"Partition":ar_p.Partition})
        ar_analysis_object.create(analyses_values)

    def create_ar_partitions(self, res):
        partition_values = {'State': res.state,
                            'analysis_request_id': res.id,
                            'Partition': 'P-0' + str(res.id) + '-R-0' + str(res.id)
                            }
        ar_partition_object = self.env["olims.ar_partition"]
        ar_sample_partition_object = self.env["olims.ar_sample_partition"]
        ar_sample_partition_object.create(partition_values)
        ar_p = ar_partition_object.create(partition_values)
        return ar_p

    def create_sample(self, ar_values, res):
        smaple_vals_dict = {
            'SamplingDate': ar_values.get('SamplingDate'),
            'SampleType': ar_values.get('SampleType'),
            'Client': ar_values.get('Client'),
            'Analysis_Request': res.id,
            'ClientReference': ar_values.get('ClientReference'),
            'ClientSampleID': ar_values.get('ClientSampleID'),
            'SamplePoint': ar_values.get('SamplePoint'),
            'StorageLocation': ar_values.get('StorageLocation'),
            'SamplingDeviation': ar_values.get('SamplingDeviation'),
            'SampleCondition': ar_values.get('SampleCondition'),
            "LotID": ar_values.get('LotID'),
        }
        sample_object = self.env["olims.sample"]
        new_sample = sample_object.create(smaple_vals_dict)
        return new_sample

    def create_field_and_lab_analyses(self, values):
        data = []
        data1 = []
        data2 = []
        data3 = []
        lab_result_list = []
        field_result_list = []
        lab_result_list_p1 = []
        field_result_list_p1 = []
        lab_result_list_p2 = []
        field_result_list_p2 = []
        lab_result_list_p3 = []
        field_result_list_p3 = []
        profile_analysis_id_list = []
        profile1_analysis_id_list = []
        profile2_analysis_id_list = []
        profile3_analysis_id_list = []
        if values.get('AnalysisProfile', None):
            analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', values.get('AnalysisProfile'))])
            for analysis in analysis_profile_obj.Service:
                profile_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile1', None):
            analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', values.get('AnalysisProfile1'))])
            for analysis in analysis_profile_obj.Service:
                profile1_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile2', None):
            analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', values.get('AnalysisProfile2'))])
            for analysis in analysis_profile_obj.Service:
                profile2_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile3', None):
            analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', values.get('AnalysisProfile3'))])
            for analysis in analysis_profile_obj.Service:
                profile3_analysis_id_list.append(analysis.Services.id)
        Position = 0
        if values.get('LabService',None):
            for LabService in values.get('LabService'):
                Position = Position+1
                if LabService[2]['LabService'] in profile_analysis_id_list:
                    self.update_lab_service_obj(LabService, data, lab_result_list)
                if LabService[2]['LabService'] in profile1_analysis_id_list:
                    self.update_lab_service_obj(LabService, data1, lab_result_list_p1)
                if LabService[2]['LabService'] in profile2_analysis_id_list:
                    self.update_lab_service_obj(LabService, data2, lab_result_list_p2)
                if LabService[2]['LabService'] in profile3_analysis_id_list:
                    self.update_lab_service_obj(LabService, data3, lab_result_list_p3)
                if LabService[2]['LabService'] not in profile_analysis_id_list and \
                                LabService[2]['LabService'] not in profile1_analysis_id_list and \
                                LabService[2]['LabService'] not in profile2_analysis_id_list and \
                                LabService[2]['LabService'] not in profile3_analysis_id_list:
                    Specification = ">" + str(LabService[2]['Min']) + ", <" + str(LabService[2]['Max'])
                    service_instance = self.env['olims.analysis_service'].search([('id', '=', LabService[2]['LabService'])])
                    if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
                        LabService[2].update({'Method': service_instance._Method.id})
                    elif service_instance.InstrumentEntryOfResults:
                        LabService[2].update({'Method': None, 'Instrument': service_instance.Instrument})
                    LabService[2].update({'Specifications': Specification,
                                  "Due Date": datetime.datetime.now(),'Position':Position})
                    lab_result_list.append([0, 0, LabService[2]])
                    lab_result_list_p1.append([0, 0, LabService[2]])
                    lab_result_list_p2.append([0, 0, LabService[2]])
                    lab_result_list_p3.append([0, 0, LabService[2]])
                    data.append(LabService)
                    data1.append(LabService)
                    data2.append(LabService)
                    data3.append(LabService)
        Position = 0
        if values.get('FieldService',None):
            for FieldService in values.get('FieldService'):
                Position = Position+1
                if FieldService[2]['Service'] in profile_analysis_id_list:
                    self.update_field_service_obj(FieldService, data, field_result_list)
                if FieldService[2]['Service'] in profile1_analysis_id_list:
                    self.update_field_service_obj(FieldService, data1, field_result_list_p1)
                if FieldService[2]['Service'] in profile2_analysis_id_list:
                    self.update_field_service_obj(FieldService, data2, field_result_list_p2)
                if FieldService[2]['Service'] in profile3_analysis_id_list:
                    self.update_field_service_obj(FieldService, data3, field_result_list_p3)
                if FieldService[2]['Service'] not in profile_analysis_id_list and \
                                FieldService[2]['Service'] not in profile1_analysis_id_list and \
                                FieldService[2]['Service'] not in profile2_analysis_id_list and \
                                FieldService[2]['Service'] not in profile3_analysis_id_list:
                    Specification = ">" + str(FieldService[2]['Min']) + ", <" + str(FieldService[2]['Max'])
                    service_instance = self.env['olims.analysis_service'].search([('id', '=', FieldService[2]['Service'])])
                    if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
                        FieldService[2].update({'Method': service_instance._Method.id})
                    elif service_instance.InstrumentEntryOfResults:
                        FieldService[2].update({'Method': None, 'Instrument': service_instance.Instrument})
                    FieldService[2].update({'Specifications': Specification,
                                    "Due Date": datetime.datetime.now(),'Position':Position})
                    field_result_list.append([0, 0, FieldService[2]])
                    data.append(FieldService)
                    field_result_list_p1.append([0, 0, FieldService[2]])
                    data1.append(FieldService)
                    field_result_list_p2.append([0, 0, FieldService[2]])
                    data2.append(FieldService)
                    field_result_list_p3.append([0, 0, FieldService[2]])
                    data3.append(FieldService)

        return data, data1, data2, data3,\
               field_result_list, lab_result_list,\
               field_result_list_p1, lab_result_list_p1,\
               field_result_list_p2, lab_result_list_p2,\
               field_result_list_p3, lab_result_list_p3

    def update_field_service_obj(self, FieldService, data1, field_result_list_p1):
        Specification = ">" + str(FieldService[2]['Min']) + ", <" + str(FieldService[2]['Max'])
        service_instance = self.env['olims.analysis_service'].search([('id', '=', FieldService[2]['Service'])])
        if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
            FieldService[2].update({'Method': service_instance._Method.id})
        elif service_instance.InstrumentEntryOfResults:
            FieldService[2].update({'Method': None, 'Instrument': service_instance.Instrument})
        FieldService[2].update({'Specifications': Specification,
                                "Due Date": datetime.datetime.now()})
        field_result_list_p1.append([0, 0, FieldService[2]])
        data1.append(FieldService)

    def update_lab_service_obj(self, LabService, data, lab_result_list):
        Specification = ">" + str(LabService[2]['Min']) + ", <" + str(LabService[2]['Max'])
        service_instance = self.env['olims.analysis_service'].search([('id', '=', LabService[2]['LabService'])])
        if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
            LabService[2].update({'Method': service_instance._Method.id})
        elif service_instance.InstrumentEntryOfResults:
            LabService[2].update({'Method': None, 'Instrument': service_instance.Instrument})
        LabService[2].update({'Specifications': Specification,
                              "Due Date": datetime.datetime.now()})
        lab_result_list.append([0, 0, LabService[2]])
        data.append(LabService)

    def get_fields_value_dicts(self, values):
        client = values.get('Client', None)
        if not client:
            client = self._context.get('client_context', None)
        analysis_request_0_dict = {
            'StorageLocation': values.get('StorageLocation', None),
            'AdHoc': values.get('AdHoc', None),
            'Template': values.get('Template', None),
            'AnalysisProfile': values.get('AnalysisProfile', None),
            'ClientSampleID': values.get('ClientSampleID', None),
            'LotID': values.get('LotID', None),
            'SubGroup': values.get('SubGroup', None),
            'SampleType': values.get('SampleType', None),
            'Batch': values.get('Batch', None),
            'SamplingDeviation': values.get('SamplingDeviation', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint', None),
            'Specification': values.get('Specification', None),
            'Priority': values.get('Priority', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate', None),
            'ReportDryMatter': values.get('ReportDryMatter', None),
            'Contact': values.get('Contact', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails', None),
            'CCContact': values.get('CCContact', None),
            'Sampler': values.get('Sampler', None),
            'Composite': values.get('Composite', None),
            'Sample_id': values.get('Sample_id', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType', None),
            'ClientReference': values.get('ClientReference',None),
            'Subtotal': values.get('Subtotal',None),
            'Discount': values.get('Discount',None),
            'VAT': values.get('VAT',None),
            'Total': values.get('Total',None),
        }
        analysis_request_1_dict = {
            'StorageLocation': values.get('StorageLocation1', None),
            'AdHoc': values.get('AdHoc1', None),
            'Template': values.get('Template1', None),
            'AnalysisProfile': values.get('AnalysisProfile1', None),
            'ClientSampleID': values.get('ClientSampleID1', None),
            'LotID': values.get('LotID1', None),
            'SubGroup': values.get('SubGroup1', None),
            'SampleType': values.get('SampleType1', None),
            'Batch': values.get('Batch1', None),
            'SamplingDeviation': values.get('SamplingDeviation1', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint1', None),
            'Specification': values.get('Specification1', None),
            'Priority': values.get('Priority1', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate1', None),
            'ReportDryMatter': values.get('ReportDryMatter1', None),
            'Contact': values.get('Contact1', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails1', None),
            'CCContact': values.get('CCContact1', None),
            'Sampler': values.get('Sampler1', None),
            'Composite': values.get('Composite1', None),
            'Sample_id': values.get('Sample_id1', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude1', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition1', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType1', None),
            'ClientReference': values.get('ClientReference1',None),
            'Subtotal': values.get('Subtotal1',None),
            'Discount': values.get('Discount1',None),
            'VAT': values.get('VAT1',None),
            'Total': values.get('Total1',None),
        }
        analysis_request_2_dict = {
            'StorageLocation': values.get('StorageLocation2', None),
            'AdHoc': values.get('AdHoc2', None),
            'Template': values.get('Template2', None),
            'AnalysisProfile': values.get('AnalysisProfile2', None),
            'ClientSampleID': values.get('ClientSampleID2', None),
            'LotID': values.get('LotID2', None),
            'SubGroup': values.get('SubGroup2', None),
            'SampleType': values.get('SampleType2', None),
            'Batch': values.get('Batch2', None),
            'SamplingDeviation': values.get('SamplingDeviation2', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint2', None),
            'Specification': values.get('Specification2', None),
            'Priority': values.get('Priority2', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate2', None),
            'ReportDryMatter': values.get('ReportDryMatter2', None),
            'Contact': values.get('Contact2', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails2', None),
            'CCContact': values.get('CCContact2', None),
            'Sampler': values.get('Sampler2', None),
            'Composite': values.get('Composite2', None),
            'Sample_id': values.get('Sample_id2', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude2', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition2', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType2', None),
            'ClientReference': values.get('ClientReference2',None),
            'Subtotal': values.get('Subtotal2',None),
            'Discount': values.get('Discount2',None),
            'VAT': values.get('VAT2',None),
            'Total': values.get('Total2',None),
        }
        analysis_request_3_dict = {
            'StorageLocation': values.get('StorageLocation3', None),
            'AdHoc': values.get('AdHoc3', None),
            'Template': values.get('Template3', None),
            'AnalysisProfile': values.get('AnalysisProfile3', None),
            'ClientSampleID': values.get('ClientSampleID3', None),
            'LotID': values.get('LotID3', None),
            'SubGroup': values.get('SubGroup3', None),
            'SampleType': values.get('SampleType3', None),
            'Batch': values.get('Batch3', None),
            'SamplingDeviation': values.get('SamplingDeviation3', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint3', None),
            'Specification': values.get('Specification3', None),
            'Priority': values.get('Priority3', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate3', None),
            'ReportDryMatter': values.get('ReportDryMatter3', None),
            'Contact': values.get('Contact3', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails3', None),
            'CCContact': values.get('CCContact3', None),
            'Sampler': values.get('Sampler3', None),
            'Composite': values.get('Composite3', None),
            'Sample_id': values.get('Sample_id3', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude3', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition3', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType3', None),
            'ClientReference': values.get('ClientReference3',None),
            'Subtotal': values.get('Subtotal3',None),
            'Discount': values.get('Discount3',None),
            'VAT': values.get('VAT3',None),
            'Total': values.get('Total3',None),
        }
        return analysis_request_0_dict, analysis_request_1_dict, analysis_request_2_dict, analysis_request_3_dict

    @api.multi
    def write(self, values):
        for record in self:
            if values.get("Analyses", None):
                for items in values.get("Analyses"):
                    if items[0] == 0:
                        result_val_dict = {}
                        result_val_dict.update({
                                "Specifications":">"+str(items[2].get("Min", None))+", <"+str(items[2].get("Max", None)),
                                "Category": items[2].get("Category"),
                                'Due Date':datetime.datetime.now(),
                                'Min': items[2].get("Min", None),
                                'Max': items[2].get("Max", None),
                                'Error': items[2].get("Error", None)
                                })
                        if items[2].get("Partition", None):
                            partition = self.env["olims.ar_partition"].search([("id", '=', items[2].get("Partition"))])
                            result_val_dict.update({"Partition": partition.Partition})
                        else:
                            result_val_dict.update({"Partition": 'P-0'+ str(record.id)+'-R-0'+str(record.id)})
                        if items[2].get("Services", None):
                            service = self.env["olims.analysis_service"].search([('id', '=', items[2].get("Services"))])
                            if service._Method and service.InstrumentEntryOfResults == False:
                                result_val_dict.update({'Method':service._Method.id})
                            elif service.InstrumentEntryOfResults:
                                result_val_dict.update({'Method':None, 'Instrument': service.Instrument})
                            if service.PointOfCapture == 'field':
                                result_val_dict.update({
                                    'Service': items[2].get("Services"),
                                    })
                                record.write({"Field_Manage_Result": [[0, 0, result_val_dict]]})
                            else:
                                result_val_dict.update({
                                    'LabService': items[2].get("Services"),
                                    })
                                record.write({"Lab_Manage_Result": [[0, 0, result_val_dict]]})
                    if items[0] == 2:
                        pass
                    if items[0] == 1:
                        manage_res_val_dict = {}
                        ar_obj = self.env["olims.ar_analysis"].search([('id', '=', items[1])])
                        ar_manage_res_obj = self.env["olims.manage_analyses"].search(["|",("manage_analysis_id","=",record.id),
                        ("lab_manage_analysis_id","=",record.id),"|",("Service","=",ar_obj.Services.id)
                        ,("LabService","=",ar_obj.Services.id)])
                        Min = items[2].get("Min") if items[2].get("Min", None) else ar_obj.Min
                        Max = items[2].get("Max") if items[2].get("Max", None) else ar_obj.Max
                        error = items[2].get("Error") if items[2].get("Error", None) else ar_obj.Error
                        manage_res_val_dict.update({"Min": Min,
                                               "Max": Max,
                                               "Error": error,
                                                "Specifications": ">" + str(Min) + ", <" + str(Max)})
                        if ar_obj.Services.PointOfCapture == "field":
                            for ar_man_res_obj in ar_manage_res_obj:
                                record.write({"Field_Manage_Result":[[1,ar_man_res_obj.id,manage_res_val_dict]]})
                        else:
                            for ar_man_res_obj in ar_manage_res_obj:
                                record.write({"Lab_Manage_Result":[[1,ar_man_res_obj.id,manage_res_val_dict]]})

        res = super(AnalysisRequest, self).write(values)
        return res  

    @api.multi
    def publish_analysis_request(self):
        # self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'olims.report_certificate_of_analysis')

    def actionToBeSampled(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_sampled',
        }, context=context)
        return True

    def getSubtotalTotalPrice(self):
        """ Compute the price with VAT but no member discount"""
        return self.getSubtotal() + self.getSubtotalVATAmount()

    @api.onchange('adjustment_option','Adjustment')
    def Computetotalamount(self):
        for record in self:
            if record.adjustment_option =='amount':
                total = self._origin.Total - record.Adjustment
            else:
                total = self._origin.Total - (self._origin.Total*record.Adjustment/100)
            record.Total = total

    @api.onchange('LabService','FieldService')
    def ComputeServiceCalculation(self):
        """
        It computes and returns the analysis service's discount amount without VAT, SubToatl and Total
        """
        client_obj = self.env["olims.client"].search([('id', '=',self._context.get('client_context', None))])
        for record in self:
            service_discount = 0.0
            service_subtotal = 0.0
            service_vat = 0.0
            service_total = 0.0

            service_discount1 = 0.0
            service_subtotal1 = 0.0
            service_vat1 = 0.0
            service_total1 = 0.0

            service_discount2 = 0.0
            service_subtotal2 = 0.0
            service_vat2 = 0.0
            service_total2 = 0.0

            service_discount3 = 0.0
            service_subtotal3 = 0.0
            service_vat3 = 0.0
            service_total3 = 0.0

            f_service_ids_list_p1 = []
            f_service_ids_list_p2 = []
            f_service_ids_list_p3 = []
            f_service_ids_list_p4 = []

            service_ids_list_p1 = []
            service_ids_list_p2 = []
            service_ids_list_p3 = []
            service_ids_list_p4 = []
            for service_p1 in record.AnalysisProfile.Service:
                if service_p1.Services.PointOfCapture == "lab":
                    service_ids_list_p1.append(service_p1.Services.id)
                else:
                    f_service_ids_list_p1.append(service_p1.Services.id)
            for service_p2 in record.AnalysisProfile1.Service:
                if service_p2.Services.PointOfCapture == "lab":
                    service_ids_list_p2.append(service_p2.Services.id)
                else:
                    f_service_ids_list_p2.append(service_p2.Services.id)
            for service_p3 in record.AnalysisProfile2.Service:
                if service_p3.Services.PointOfCapture == "lab":
                    service_ids_list_p3.append(service_p3.Services.id)
                else:
                    f_service_ids_list_p3.append(service_p3.Services.id)
            for service_p4 in record.AnalysisProfile3.Service:
                if service_p4.Services.PointOfCapture == "lab":
                    service_ids_list_p4.append(service_p4.Services.id)
                else:
                    f_service_ids_list_p4.append(service_p4.Services.id)

            for service in record.LabService:
                if service.LabService.id in service_ids_list_p1:
                    if record.AnalysisProfile.UseAnalysisProfilePrice:
                        service_price = float(record.AnalysisProfile.AnalysisProfilePrice)
                        service_discount = service_price * client_obj.M_Discount / 100
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal = float(service_price) - float(discount)
                        # compute VAT
                        service_vat = (float(service_price) - float(discount)) * record.AnalysisProfile.AnalysisProfileVAT / 100
                        service_total = service_subtotal + service_vat
                    else:
                        service_price = service.LabService.Price
                        service_discount += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal += float(service_price) - float(discount)
                        # compute VAT
                        service_vat += (float(service_price) - float(discount)) * service.LabService.VAT / 100
                        service_total = service_subtotal + service_vat
                if service.LabService.id in service_ids_list_p2:
                    if record.AnalysisProfile1.UseAnalysisProfilePrice:
                        service_price = record.AnalysisProfile1.AnalysisProfilePrice
                        service_discount1 = service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal1 = float(service_price) - float(discount)
                        # compute VAT
                        service_vat1 = service_subtotal1 * record.AnalysisProfile1.AnalysisProfileVAT / 100
                        service_total1 = service_subtotal1 + service_vat1
                    else:
                        service_price = service.LabService.Price
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat1 += (service_price - discount) * service.LabService.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1
                if service.LabService.id in service_ids_list_p3:
                    if record.AnalysisProfile2.UseAnalysisProfilePrice:
                        service_price = record.AnalysisProfile2.AnalysisProfilePrice
                        service_discount2 = service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal2 = float(service_price) - float(discount)
                        # compute VAT
                        service_vat2 = service_subtotal2 * record.AnalysisProfile2.AnalysisProfileVAT / 100
                        service_total2 = service_subtotal2 + service_vat2
                    else:
                        service_price = service.LabService.Price
                        service_discount2 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal2 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat2 += (service_price - discount) * service.LabService.VAT / 100
                        service_total2 = service_subtotal2 + service_vat2
                if service.LabService.id in service_ids_list_p4:
                    if record.AnalysisProfile3.UseAnalysisProfilePrice:
                        service_price = record.AnalysisProfile3.AnalysisProfilePrice
                        service_discount3 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal3 = float(service_price) - float(discount)
                        # compute VAT
                        service_vat3 = service_subtotal3 * record.AnalysisProfile3.AnalysisProfileVAT / 100
                        service_total3 = service_subtotal3 + service_vat3
                    else:
                        service_price = service.LabService.Price
                        service_discount3 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal3 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat3 += (service_price - (service_price * client_obj.M_Discount / 100)) * service.LabService.VAT / 100
                        service_total3 = service_subtotal3 + service_vat3
                if service.LabService.id not in service_ids_list_p1 and \
                                service.LabService.id not in service_ids_list_p2 and \
                                service.LabService.id not in service_ids_list_p3 and \
                                service.LabService.id not in service_ids_list_p4:
                    service_price = float(service.LabService.Price)
                    discount = service_price * client_obj.M_Discount / 100
                    service_discount, service_subtotal, service_total, service_vat = self.calculate_lab_service_amount_for_ar(
                        discount, service, service_discount, service_price, service_subtotal, service_total,
                        service_vat,client_obj)
                    if record.Copy == '1' or record.AnalysisProfile1 and not record.AnalysisProfile2 and not record.AnalysisProfile3:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)
                    elif record.Copy == '2' or record.AnalysisProfile1 and record.AnalysisProfile2 and not record.AnalysisProfile3:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)
                    elif record.Copy == '3' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)
            for FService in record.FieldService:
                if FService.Service.id in f_service_ids_list_p1:
                    if record.AnalysisProfile.UseAnalysisProfilePrice:
                        service_price = float(record.AnalysisProfile.AnalysisProfilePrice)
                        service_discount = service_price * client_obj.M_Discount / 100
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal = float(service_price) - float(discount)
                        # compute VAT
                        service_vat = (float(service_price) - float(discount)) * record.AnalysisProfile.AnalysisProfileVAT / 100
                        service_total = service_subtotal + service_vat
                    else:
                        service_price = FService.Service.Price
                        service_discount += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal += float(service_price) - float(discount)
                        # compute VAT
                        service_vat += (float(service_price) - float(discount)) * FService.Service.VAT / 100
                        service_total = service_subtotal + service_vat
                if FService.Service.id in f_service_ids_list_p2:
                    if record.AnalysisProfile1.UseAnalysisProfilePrice:
                        service_price = record.AnalysisProfile1.AnalysisProfilePrice
                        service_discount1 = service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal1 = float(service_price) - float(discount)
                        # compute VAT
                        service_vat1 = (float(service_price) - float(discount)) * record.AnalysisProfile1.AnalysisProfileVAT / 100
                        service_total1 = service_subtotal1 + service_vat1
                    else:
                        service_price = FService.Service.Price
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat1 += (float(service_price) - float(discount)) * FService.Service.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1
                if FService.Service.id in f_service_ids_list_p3:
                    if record.AnalysisProfile2.UseAnalysisProfilePrice:
                        service_price = record.AnalysisProfile2.AnalysisProfilePrice
                        service_discount2 = service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal2 = float(service_price) - float(discount)
                        # compute VAT
                        service_vat2 = (float(service_price) - float(discount)) * record.AnalysisProfile2.AnalysisProfileVAT / 100
                        service_total2 = service_subtotal2 + service_vat2
                    else:
                        service_price = FService.Service.Price
                        service_discount2 += service_price * client_obj.M_Discount / 100
                        # compute sf_ubtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal2 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat2 += (float(service_price) - float(discount)) * FService.Service.VAT / 100
                        service_total2 = service_subtotal2 + service_vat2
                if FService.Service.id in f_service_ids_list_p4:
                    if record.AnalysisProfile3.UseAnalysisProfilePrice:
                        service_price = record.AnalysisProfile3.AnalysisProfilePrice
                        service_discount3 = service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal3 = float(service_price) - float(discount)
                        # compute VAT
                        service_vat3 = (float(service_price) - float(discount)) * record.AnalysisProfile3.AnalysisProfileVAT /100
                        service_total3 = service_subtotal3 + service_vat3
                    else:
                        service_price = FService.Service.Price
                        service_discount3 = service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        discount = service_price * client_obj.M_Discount / 100
                        service_subtotal3 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat3 += service_subtotal3 * FService.Service.VAT / 100
                        service_total3 = service_subtotal3 + service_vat3
                if FService.Service.id not in f_service_ids_list_p1 and \
                                FService.Service.id not in f_service_ids_list_p2 and \
                                FService.Service.id not in f_service_ids_list_p3 and \
                                FService.Service.id not in f_service_ids_list_p4:
                    
                    service_price = float(FService.Service.Price)
                    service_discount += service_price * client_obj.M_Discount / 100
                    # compute subtotal
                    discount = service_price * client_obj.M_Discount / 100
                    service_subtotal += float(service_price) - float(discount)
                    # compute VAT
                    service_vat += service_subtotal * FService.Service.VAT / 100
                    service_total = service_subtotal + service_vat

                    if record.Copy == '1' or record.AnalysisProfile1 and not record.AnalysisProfile2 and not record.AnalysisProfile3:
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        # discount = service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat1 += service_subtotal1 * FService.Service.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1
                    elif record.Copy == '2' or record.AnalysisProfile1 and record.AnalysisProfile2 and not record.AnalysisProfile3:
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        service_vat1 += service_subtotal1 * FService.Service.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1

                        service_discount2 += service_price * client_obj.M_Discount / 100
                        service_subtotal2 += float(service_price) - float(discount)
                        service_vat2 += service_subtotal2 * FService.Service.VAT / 100
                        service_total2 = service_subtotal2 + service_vat2
                    elif record.Copy == '3' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3:
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        service_vat1 += service_subtotal1 * FService.Service.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1

                        service_discount2 += service_price * client_obj.M_Discount / 100
                        service_subtotal2 += float(service_price) - float(discount)
                        service_vat2 += service_subtotal2 * FService.Service.VAT / 100
                        service_total2 = service_subtotal2 + service_vat2

                        service_discount3 += service_price * client_obj.M_Discount / 100
                        service_subtotal3 += float(service_price) - float(discount)
                        service_vat3 += service_subtotal3 * FService.Service.VAT / 100
                        service_total3 = service_subtotal3 + service_vat3    

            record.Discount = service_discount
            record.Subtotal = service_subtotal
            record.VAT = service_vat
            record.Total = service_total

            record.Discount1 = service_discount1
            record.Subtotal1 = service_subtotal1
            record.VAT1 = service_vat1
            record.Total1 = service_total1

            record.Discount2 = service_discount2
            record.Subtotal2 = service_subtotal2
            record.VAT2 = service_vat2
            record.Total2 = service_total2

            record.Discount3 = service_discount3
            record.Subtotal3 = service_subtotal3
            record.VAT3 = service_vat3
            record.Total3 = service_total3

    def calculate_lab_service_amount_for_ar(self, discount, service, service_discount, service_price, service_subtotal,
                                            service_total, service_vat, client_obj):
        service_discount += service_price * client_obj.M_Discount / 100
        service_subtotal += float(service_price) - float(discount)
        service_vat += (float(service_price) - float(discount)) * service.LabService.VAT / 100
        service_total = service_subtotal + service_vat
        return service_discount, service_subtotal, service_total, service_vat

    def getTotalPrice(self):
        """
        It gets the discounted price from analyses and profiles to obtain the total value with the VAT
        and the discount applied
        :return: the analysis request's total price including the VATs and discounts
        """
        for record in self:
            record.Total = record.Subtotal + record.VAT

    def isInvalid(self,cr,uid,ids,context=None):
        """ return if the Analysis Request has been invalidated
        """
        return self.write(cr, uid, ids, {
            'state': 'invalid',
        }, context=context)
        return True

    def workflow_script_receive(self,cr,uid,ids,context=None):
        analysis_request_obj = self.pool.get('olims.analysis_request').browse(cr,uid,ids,context)
        for ar_object in analysis_request_obj:
            data_list = []
            ar_cate_ids_list = []
            for items in ar_object.Analyses:
                analysis_dict = {}
                analysis_dict.update({
                    'category':items.Category.id,
                    'client': ar_object.Client.id,
                    'order':ar_object.LotID,
                    'priority':ar_object.Priority.id,
                    'due_date':ar_object.DateDue,
                    'received_date':datetime.datetime.now(),
                    'analysis':items.Services.id,
                    'sample_type': ar_object.SampleType.id,
                    'add_analysis_id':ar_object.id
                    })
                data_list.append([0, 0, analysis_dict])
            ar_object.write({'AddAnalysis': data_list})

        datereceived = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'sample_received', 'DateReceived' : datereceived,
        }, context=context)
        return True

    def workflow_script_preserve(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'preserved',
        }, context=context)
        return True

    def workflow_script_sample(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'sampled',
        }, context=context)

        return True

    def workflow_script_to_be_preserved(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_preserved',
        }, context=context)
        return True

    def workflow_script_sample_due(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'sample_due', 'DateDue':datetime.datetime.now()
        }, context=context)
        return True

    def workflow_script_to_be_verified(self,cr,uid,ids,context=None):
        data_list = []
        for items in self.browse(cr,uid,ids,context):
            for objects in items.AddAnalysis:
                data_list.append([2, objects.id])

        self.write(cr, uid, ids, {
            'state': 'to_be_verified', 'AddAnalysis': data_list
        }, context=context)
        return True

    def workflow_script_verify(self):
        self.write({
            'state': 'verified',
        })
        return True

    def workflow_script_publish(self):
        datepublished = datetime.datetime.now()
        self.write({
            'state': 'published', 'DatePublished' : datepublished
        })
        return True

    def workflow_script_cancel(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids,{
            'state': 'cancelled'
        },context)
        return True

    @api.multi
    @api.onchange("AnalysisProfile","AnalysisProfile1","AnalysisProfile2","AnalysisProfile3")
    def _add_values_in_analyses(self):
        service_ids_list = []
        for record in self:
            if record.state != "sample_registered":
                record.Field_Manage_Result = None
                record.Lab_Manage_Result = None
                record.Analyses = None
                for services in record.AnalysisProfile.Service:
                    record.Analyses += record.Analyses.new({'Category':services.Services.category.id,
                                'Services':services.Services.id,
                                'Min':services.Services.Min,
                                'Max':services.Services.Max,
                                'Partition': record.Partition.id})
                return {
                        'warning': {'title': 'Warning!', 'message': "All Analysis will be changed." +
                        "To proceed click on Save button or Discard the changes."},
                        }
            self.LabService = None
            self.FieldService = None
            for service in record.AnalysisProfile.Service:
                if service.Services.PointOfCapture == 'lab':
                    l_service = {'LabService':service.Services.id,
                        'Category':service.Services.category.id}
                    record.LabService += record.LabService.new(l_service)
                if service.Services.PointOfCapture == 'field':
                    f_service = {'Service':service.Services.id,
                        'Category':service.Services.category.id}
                    record.FieldService += record.FieldService.new(f_service)
                service_ids_list.append(service.Services.id)
            for service in record.AnalysisProfile1.Service:
                if service.Services.PointOfCapture == 'lab':
                    if service.Services.id in service_ids_list:
                        continue
                    else:
                        l_service = {'LabService':service.Services.id,
                            'Category':service.Services.category.id}
                        record.LabService += record.LabService.new(l_service)
                        service_ids_list.append(service.Services.id)
                elif service.Services.PointOfCapture == 'field':
                    if service.Services.id in service_ids_list:
                        continue
                    else:
                        f_service = {'Service':service.Services.id,
                        'Category':service.Services.category.id}
                        record.FieldService += record.FieldService.new(f_service)
                        service_ids_list.append(service.Services.id)

            for service in record.AnalysisProfile2.Service:
                if service.Services.PointOfCapture == 'lab':
                    if service.Services.id in service_ids_list:
                        continue
                    else:
                        l_service = {'LabService':service.Services.id,
                            'Category':service.Services.category.id}
                        record.LabService += record.LabService.new(l_service)
                        service_ids_list.append(service.Services.id)
                elif service.Services.PointOfCapture == 'field':
                    if service.Services.id in service_ids_list:
                        continue
                    else:
                        f_service = {'Service':service.Services.id,
                        'Category':service.Services.category.id}
                        record.FieldService += record.FieldService.new(f_service)
                        service_ids_list.append(service.Services.id)

            for service in record.AnalysisProfile3.Service:
                if service.Services.PointOfCapture == 'lab':
                    if service.Services.id in service_ids_list:
                        continue
                    else:
                        l_service = {'LabService':service.Services.id,
                            'Category':service.Services.category.id}
                        record.LabService += record.LabService.new(l_service)
                        service_ids_list.append(service.Services.id)
                elif service.Services.PointOfCapture == 'field':
                    if service.Services.id in service_ids_list:
                        continue
                    else:
                        f_service = {'Service':service.Services.id,
                        'Category':service.Services.category.id}
                        record.FieldService += record.FieldService.new(f_service)
                        service_ids_list.append(service.Services.id)

                        

    def bulk_change_states(self,state,cr,uid,ids,context=None):
        previous_state = ""
        if state == "sample_due":
            previous_state = "to_be_sampled"
        elif state == "sample_received":
            previous_state = "sample_due"
        requests = self.browse(cr,uid,ids)
        sample_ids = []
        for request in requests:
            if request.state != previous_state:
                ids.remove(request.id)
            else:
                sample_ids.append(request.Sample_id.id)
        self.browse(cr,uid,ids).signal_workflow(state)
        self.pool.get("olims.sample").browse(cr,uid,sample_ids).write({"state":state})
        return True

    def bulk_verify_request(self,cr,uid,ids,context=None):
        requests = self.pool.get('olims.analysis_request').browse(cr,uid,ids,context)
        res_user = self.pool.get("res.users").browse(cr, uid, [uid], context)
        for request in requests:
            if request.state == "to_be_verified" and request.write_uid.id == uid and res_user.two_step_verification:
                message = _("You are not allowed to verify")
                raise Warning(message)
            ar_manage_results = self.pool.get("olims.manage_analyses")
            analyses = ar_manage_results.search_read(cr, uid, [
                "|",("manage_analysis_id","=",request.id),
                    ("lab_manage_analysis_id","=",request.id)
                ])
            all_verified = True
            for analysis in analyses:
                if analysis['state'] == 'to_be_verified':
                    ar_manage_results.write(cr, uid, analysis['id'], {"state": "verified"})
                elif analysis['state'] != 'verified':
                    all_verified = False
            if all_verified:
                request.signal_workflow('verify')
            worksheet_manage_results = self.pool.get('olims.ws_manage_results')
            ws_man_results = worksheet_manage_results.search_read(cr, uid, [
                ('request_analysis_id', '=', request.id)])
            
            ws_manage_res_ids_list = []
            worksheets_boject = self.pool.get('olims.worksheet')
            for ws_manage_res in ws_man_results:
                if ws_manage_res['state'] == 'to_be_verified':
                    worksheet_manage_results.write(
                        cr, uid, ws_manage_res['id'],{'state':'verified'})
                worksheets = worksheets_boject.search_read(cr, uid, [
                    ('ManageResult', '=', ws_manage_res['id'])])
                for worksheet in worksheets:
                    if worksheet['id'] not in ws_manage_res_ids_list:
                        ws_manage_res_ids_list.append(worksheet['id'])
            ws_manage_results_all_verified = True
            if ws_manage_res_ids_list:
                worksheet_objs = worksheets_boject.browse(cr, uid, ws_manage_res_ids_list, context)
                for worksheet_obj in worksheet_objs:
                    for ws_manage_result_boj in worksheet_obj.ManageResult:
                        if ws_manage_result_boj.state != 'verified':
                            ws_manage_results_all_verified = False
                            continue
                        if ws_manage_results_all_verified:
                            worksheet_obj.signal_workflow('verify')

    @api.onchange('CopyContact')
    def copy_contact(self):
        if self.Copy == '1':
            self.Contact1 = self.Contact
            self.Contact2 = self.Contact3 = None
        elif self.Copy == '2':
            self.Contact1 = self.Contact2 = self.Contact
            self.Contact3 = None
        elif self.Copy == '3':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact
        else:
            pass

    @api.onchange('CopyCCContact')
    def copy_cccontact(self):
        if self.Copy == '1':
            self.CCContact1 = self.CCContact
            self.CCContact2 = self.CCContact3 = None
        elif self.Copy == '2':
            self.CCContact1 = self.CCContact2 = self.CCContact
            self.CCContact3 = None
        elif self.Copy == '3':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact
        else:
            pass

    @api.onchange('CopyEmail')
    def copy_email(self):
        if self.Copy == '1':
            self.CCEmails1 = self.CCEmails
            self.CCEmails2 = self.CCEmails3 = None
        elif self.Copy == '2':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails
            self.CCEmails3 = None
        elif self.Copy == '3':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails
        else:
            pass

    @api.onchange('Copysample')
    def copy_sample(self):
        if self.Copy == '1':
            self.Sample_id1 = self.Sample_id
            self.Sample_id2 = self.Sample_id3 = None
        elif self.Copy == '2':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id
            self.Sample_id3 = None
        elif self.Copy == '3':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id
        else:
            pass


    @api.onchange('Copysubgroup')
    def copy_subgroup(self):
        if self.Copy == '1':
            self.SubGroup1 = self.SubGroup
            self.SubGroup2 = self.SubGroup3 = None
        elif self.Copy == '2':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup
            self.SubGroup3 = None
        elif self.Copy == '3':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup
        else:
            pass

    @api.onchange('Copytemplate')
    def copy_template(self):
        if self.Copy == '1':
            self.Template1 = self.Template
            self.Template2 = self.Template3 = None
        elif self.Copy == '2':
            self.Template1 = self.Template2 = self.Template
            self.Template3 = None
        elif self.Copy == '3':
            self.Template1 = self.Template2 = self.Template3 = self.Template
        else:
            pass

    @api.onchange('Copyprofile')
    def copy_profile(self):
        if self.Copy == '1':
            self.AnalysisProfile1 = self.AnalysisProfile
            self.AnalysisProfile2 = self.AnalysisProfile3 = None
        elif self.Copy == '2':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile
            self.AnalysisProfile3 = None
        elif self.Copy == '3':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile
        else:
            pass

    @api.onchange('Copysmaplingdate')
    def copy_sampledate(self):
        if self.Copy == '1':
            self.SamplingDate1 = self.SamplingDate
            self.SamplingDate2 = self.SamplingDate3 = None
        elif self.Copy == '2':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate
            self.SamplingDate3 = None
        elif self.Copy == '3':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate
        else:
            pass

    @api.onchange('Copysampler')
    def copy_sampler(self):
        if self.Copy == '1':
            self.Sampler1 = self.Sampler
            self.Sampler2 = self.Sampler3 = None
        elif self.Copy == '2':
            self.Sampler1 = self.Sampler2 = self.Sampler
            self.Sampler3 = None
        elif self.Copy == '3':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler
        else:
            pass

    @api.onchange('Copysampletype')
    def copy_sample_type(self):
        if self.Copy == '1':
            self.SampleType1 = self.SampleType
            self.SampleType2 = self.SampleType3 = None
        elif self.Copy == '2':
            self.SampleType1 = self.SampleType2 = self.SampleType
            self.SampleType3 = None
        elif self.Copy == '3':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType
        else:
            pass

    @api.onchange('Copyspecification')
    def copy_specification(self):
        if self.Copy == '1':
            self.Specification1 = self.Specification
            self.Specification2 = self.Specification3 = None
        elif self.Copy == '2':
            self.Specification1 = self.Specification2 = self.Specification
            self.Specification3 = None
        elif self.Copy == '3':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification
        else:
            pass


    @api.onchange('CopyClientReference')
    def copy_client_reference(self):
        if self.Copy == '1':
            self.ClientReference1 = self.ClientReference
            self.ClientReference2 = self.ClientReference3 = None
        elif self.Copy == '2':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference
            self.ClientReference3 = None
        elif self.Copy == '3':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference
        else:
            pass

    @api.onchange('CopySampleCondition')
    def copy_sample_condition(self):
        if self.Copy == '1':
            self.SampleCondition1 = self.SampleCondition
            self.SampleCondition2 = self.SampleCondition3 = None
        elif self.Copy == '2':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition
            self.SampleCondition3 = None
        elif self.Copy == '3':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition
        else:
            pass

    @api.onchange('CopyAdHoc')
    def copy_adhoc(self):
        if self.Copy == '1':
            self.AdHoc1 = self.AdHoc
            self.AdHoc2 = self.AdHoc3 = False
        elif self.Copy == '2':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc
            self.AdHoc3 = False
        elif self.Copy == '3':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc
        else:
            pass

    @api.onchange('CopyComposite')
    def copy_composite(self):
        if self.Copy == '1':
            self.Composite1 = self.Composite
            self.Composite2 = self.Composite3 = False
        elif self.Copy == '2':
            self.Composite1 = self.Composite2 = self.Composite
            self.Composite3 = False
        elif self.Copy == '3':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite
        else:
            pass

    @api.onchange('CopyReportDryMatter')
    def copy_report_dry_matter(self):
        if self.Copy == '1':
            self.ReportDryMatter1 = self.ReportDryMatter
            self.ReportDryMatter2 = self.ReportDryMatter3 = False
        elif self.Copy == '2':
            self.ReportDryMatter1 = self.ReportDryMatter2 = self.ReportDryMatter
            self.ReportDryMatter3 = False
        elif self.Copy == '3':
            self.ReportDryMatter1 = self.ReportDryMatter2 = self.ReportDryMatter3 = self.ReportDryMatter
        else:
            pass

    @api.onchange('CopyInvoiceExclude')
    def copy_invoice_exclude(self):
        if self.Copy == '1':
            self.InvoiceExclude1 = self.InvoiceExclude
            self.InvoiceExclude2 = self.InvoiceExclude3 = False
        elif self.Copy == '2':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude
            self.InvoiceExclude3 = False
        elif self.Copy == '3':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude
        else:
            pass

    @api.onchange('CopyPriority')
    def copy_priority(self):
        if self.Copy == '1':
            self.Priority1 = self.Priority
            self.Priority2 = self.Priority3 = None
        elif self.Copy == '2':
            self.Priority1 = self.Priority2 = self.Priority
            self.Priority3 = None
        elif self.Copy == '3':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority
        else:
            pass

    @api.multi
    def action_report_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        emails_send = []
        for email in self.CCEmails:
            emails_send.append(email.name)
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('olims', 'email_template_edi_ar')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self._context)
        ctx.update({
            'default_model': 'olims.analysis_request',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'send_email': ",".join(emails_send)
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.onchange("DateSampled")
    def show_warning_for_payment_not_current_on_create(self):
        warning = {}
        if self._context.get('client_context', None):
            client = self.env["olims.client"].search([("id", "=", self._context.get('client_context'))])
            if client.payment_not_current:
                title = _("Warning for %s") % client.Name
                message = _("Payment not Current for %s") % client.Name
                warning.update({
                    'title': title,
                    'message': message
                    })
                return {'warning': warning}
    @api.depends("is_billed")
    def set_billing_status(self):
        for record in self:
            if record.is_billed == True:
                record.billing_status = "Billed"

    @api.onchange("Analyses")
    def update_ar_prices(self):
        lsit_of_service_ids = []
        self.Discount = 0.00
        self.Subtotal = 0.00
        self.VAT = 0.00
        self.Total = 0.00
        for service in self.AnalysisProfile.Service:
            lsit_of_service_ids.append(service.Services.id)
        for service_record in self.Analyses:
            if service_record.Services.id in lsit_of_service_ids and self.AnalysisProfile and self.AnalysisProfile.UseAnalysisProfilePrice:
                self.Discount = self.AnalysisProfile.AnalysisProfilePrice * self.Client.M_Discount / 100
                self.Subtotal = self.AnalysisProfile.AnalysisProfilePrice - self.Discount
                self.VAT = self.AnalysisProfile.AnalysisProfileVAT / 100 * self.Subtotal
                self.Total = self.Subtotal + self.VAT
            else:
                self.Discount += service_record.Services.Price * self.Client.M_Discount / 100
                self.Subtotal += service_record.Services.Price - (service_record.Services.Price *self.Client.M_Discount / 100)
                self.VAT += service_record.Services.VAT * (service_record.Services.Price - (service_record.Services.Price * self.Client.M_Discount / 100)) /100
                self.Total = self.Subtotal + self.VAT

    @api.onchange("Template","Template1","Template2","Template3")
    def add_contact_and_email_of_template(self):
        self.Contact = self.Template.contact_id
        self.CCEmails = self.Template.email_id
        self.AnalysisProfile = self.Template.AnalysisProfile
        self.SampleType = self.Template.SampleType
        self.Priority = self.Template.priority
        if self.Template1:
            self.Contact1 = self.Template1.contact_id
            self.CCEmails1 = self.Template1.email_id
            self.AnalysisProfile1 = self.Template1.AnalysisProfile
            self.SampleType1 = self.Template1.SampleType
            self.Priority1 = self.Template1.priority
        if self.Template2:
            self.Contact2 = self.Template2.contact_id
            self.CCEmails2 = self.Template2.email_id
            self.AnalysisProfile2 = self.Template2.AnalysisProfile
            self.SampleType2 = self.Template2.SampleType
            self.Priority2 = self.Template2.priority
        if self.Template3:
            self.Contact3 = self.Template3.contact_id
            self.CCEmails3 = self.Template3.email_id
            self.AnalysisProfile3 = self.Template3.AnalysisProfile
            self.SampleType3 = self.Template3.SampleType
            self.Priority3 = self.Template3.priority

    @api.onchange("SampleType")
    def return_profile_domain(self):
        res = {}
        if self.SampleType:
            profile_ids = []
            for profile in self.SampleType.profile:
                profile_ids.append(profile.id)
            res['domain'] = {'AnalysisProfile':[('id', 'in', profile_ids)]}
        else:
            res['domain'] = {'AnalysisProfile': []}
        return res

    @api.onchange("SampleType1")
    def return_profile1_domain(self):
        res = {}
        if self.SampleType1:
            profile_ids = []
            for profile in self.SampleType1.profile:
                profile_ids.append(profile.id)
            res['domain'] = {'AnalysisProfile1':[('id', 'in', profile_ids)]}
        else:
            res['domain'] = {'AnalysisProfile1': []}
        return res

    @api.onchange("SampleType2")
    def return_profile2_domain(self):
        res = {}
        if self.SampleType2:
            profile_ids = []
            for profile in self.SampleType2.profile:
                profile_ids.append(profile.id)
            res['domain'] = {'AnalysisProfile2':[('id', 'in', profile_ids)]}
        else:
            res['domain'] = {'AnalysisProfile2': []}
        return res

    @api.onchange("SampleType3")
    def return_profile3_domain(self):
        res = {}
        if self.SampleType3:
            profile_ids = []
            for profile in self.SampleType3.profile:
                profile_ids.append(profile.id)
            res['domain'] = {'AnalysisProfile3':[('id', 'in', profile_ids)]}
        else:
            res['domain'] = {'AnalysisProfile3': []}
        return res

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        ids_list_lab_manage_results = []
        ids_list_field_manage_results = []
        ids_list_manage_analyses = []
        for obj in self.Lab_Manage_Result:
            lab_res_val_dict = {'Category': obj.Category.id,
            'LabService': obj.LabService.id,
             'Due Date': datetime.datetime.now(),
             'Min': obj.Min,
             'Specifications': ">" + str(obj.Min) + ", <" + str(obj.Max),
             'Max': obj.Max,
             'Error': obj.Error}
            ids_list_lab_manage_results.append([0, 0, lab_res_val_dict])
        for obj in self.Field_Manage_Result:
            field_res_val_dict = {'Category': obj.Category.id,
            'Service': obj.LabService.id,
             'Due Date': datetime.datetime.now(),
             'Min': obj.Min,
             'Specifications': ">" + str(obj.Min) + ", <" + str(obj.Max),
             'Max': obj.Max,
             'Error': obj.Error}
            ids_list_field_manage_results.append([0, 0, field_res_val_dict])
        for obj in self.Analyses:
            analyses_val_dict = {
            'Priority': self.Priority.id,
            'Partition': self.Partition.id,
            'Category': obj.Category.id,
            'Services': obj.Services.id,
            'Min': obj.Min,
            'Max': obj.Max,
            }
            ids_list_manage_analyses.append([0, 0, analyses_val_dict])
        default.update({
            'Sample_id': self.Sample_id.id,
            'Lab_Manage_Result': ids_list_lab_manage_results,
            'Field_Manage_Result': ids_list_field_manage_results,
            'Analyses': ids_list_manage_analyses
            })
        return super(AnalysisRequest, self).copy(default)

class FieldAnalysisService(models.Model, BaseOLiMSModel):
    _name = 'olims.field_analysis_service'

    @api.onchange('Service','LabService')
    def _ComputeFieldResults(self):
        for item in self:
            if item.Service:
                item.CommercialID = item.Service.CommercialID
                item.ProtocolID  = item.Service.ProtocolID
                item.Min = item.Service.Min
                item.Max = item.Service.Max
            if item.LabService:
                item.CommercialID = item.LabService.CommercialID
                item.ProtocolID  = item.LabService.ProtocolID
                item.Min = item.LabService.Min
                item.Max = item.LabService.Max

class ManageAnalyses(models.Model, BaseOLiMSModel):
    _inherit = 'olims.field_analysis_service'
    _name = 'olims.manage_analyses'


    @api.onchange("Result")
    def save_results(self):
        for item in self:
            data_res = item.Result
        record_obj = self.pool.get('olims.manage_analyses')
        record = record_obj.browse(self.env.cr, self.env.uid, self._origin.id)
        record.write({
                'Result': data_res
            })
        self.env.cr.commit()


    @api.onchange("Result_string")
    def set_result_value(self):
        data_res = self.Result_string
        if data_res:
            if data_res.find('>')!=-1:
                data_res.index('>')
                data = float(data_res[data_res.index('>')+1:]) +1
            elif data_res.find('<')!=-1:
                data_res.index('<')
                data = float(data_res[data_res.index('<')+1:])-1
            else:
                data = float(data_res)
        else:
            data = 0
        record_obj = self.pool.get('olims.manage_analyses')
        record = record_obj.browse(self.env.cr, self.env.uid, self._origin.id)
        record.write({
            'Result': data,
            'Result_string': data_res
            })
        #Updating Result in Worksheet
        ws_record_obj = self.pool.get('olims.ws_manage_results')
        if record.manage_analysis_id:
            ws_record_id = ws_record_obj.search(self.env.cr, self.env.uid, [('request_analysis_id', '=', record.manage_analysis_id.id),('category','=',record.Category.id),('analysis','=',record.Service.id)])[0]
        if record.lab_manage_analysis_id:
            ws_record_id = ws_record_obj.search(self.env.cr, self.env.uid, [('request_analysis_id', '=', record.lab_manage_analysis_id.id),('category','=',record.Category.id),('analysis','=',record.LabService.id)])[0]
        ws_record = ws_record_obj.browse(self.env.cr, self.env.uid, ws_record_id)
        ws_record.write({
            'result': data,
            'result_string': data_res
            })
        self.env.cr.commit()

    @api.multi
    def bulk_verify(self):
        ar_ids = []
        analysis_ids = []
        for record in self:
            if record.state == "verified":
                continue
            record.write({"state":"to_be_verified"})
            if len(record.Service) != 0:
                analysis_id = record.Service.id
                request_id = record.manage_analysis_id.id
            else:
                analysis_id = record.LabService.id
                request_id = record.lab_manage_analysis_id.id
            analyses = self.env["olims.ws_manage_results"].search([
                ("analysis","=",analysis_id),
                ("request_analysis_id","=",request_id)
                ])
            for analysis in analyses:
                if analysis.id not in analysis_ids:
                    analysis_ids.append(analysis.id)
                analysis.write({"state":"to_be_verified","result":record.Result,"result_string":record.Result_string})
            arecs = self.env["olims.manage_analyses"].search([
                "|",("manage_analysis_id","=",request_id),
                    ("lab_manage_analysis_id","=",request_id)
                ])
            all_submitted = True
            for arec in arecs:
                if arec.state != "to_be_verified" and arec.state != "verified":
                    all_submitted = False
                    break
            if all_submitted:
                ar_ids.append(request_id)
        self.env["olims.analysis_request"].browse(ar_ids).signal_workflow("submit")
        # Updating state of worksheet if all submitted
        worksheets = self.env['olims.worksheet'].search([("ManageResult","in",analysis_ids)])
        for worksheet in worksheets:
            ws_all_submitted = True
            for ws_result in worksheet.ManageResult:
                if ws_result.state != "to_be_verified":
                    ws_all_submitted = False
                    break
            if ws_all_submitted:
                self.env["olims.worksheet"].browse(worksheet.id).signal_workflow("submit")
        return True

    @api.multi
    def verify_analyses_and_ws(self):
        res_user = self.env["res.users"].search([('id', '=', self.env.uid)])
        ar_ids = []
        analysis_ids = []
        for record in self:
            if record.state == "to_be_verified" and record.write_uid.id == self.env.uid and res_user.two_step_verification:
                message = _("You are not allowed to verify")
                raise Warning(message)
            if not record.state != "verified":
                continue
            record.write({"state":"verified"})
            if len(record.Service) != 0:
                analysis_id = record.Service.id
                request_id = record.manage_analysis_id.id
            else:
                analysis_id = record.LabService.id
                request_id = record.lab_manage_analysis_id.id
            analyses = self.env["olims.ws_manage_results"].search([
                ("analysis","=",analysis_id),
                ("request_analysis_id","=",request_id)
                ])
            for analysis in analyses:
                if analysis.id not in analysis_ids:
                    analysis_ids.append(analysis.id)
                analysis.write({"state":"verified"})
            arecs = self.env["olims.manage_analyses"].search([
                "|",("manage_analysis_id","=",request_id),
                    ("lab_manage_analysis_id","=",request_id)
                ])
            all_verified = True
            for arec in arecs:
                if arec.state != "verified":
                    all_verified = False
                    break
            if all_verified:
                ar_ids.append(request_id)
        self.env["olims.analysis_request"].browse(ar_ids).signal_workflow("verify")
        # Updating state of worksheet if all verified
        worksheets = self.env['olims.worksheet'].search([("ManageResult","in",analysis_ids)])
        for worksheet in worksheets:
            ws_all_verified = True
            for ws_result in worksheet.ManageResult:
                if ws_result.state != "verified":
                    ws_all_verified = False
                    break
            if ws_all_verified and worksheet.State != "closed":
                self.env["olims.worksheet"].browse(worksheet.id).signal_workflow("verify")
        return True

    @api.depends('Result', 'Min', 'Max')
    def insert_flag(self):
        for record in self:
            if record.Result < record.Min or record.Result > record.Max:
                record.flag = "flag"
            else:
                record.flag = False

AnalysisRequest.initialze(schema)
FieldAnalysisService.initialze(schema_analysis)
ManageAnalyses.initialze(manage_result_schema)