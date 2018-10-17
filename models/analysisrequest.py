"""The request for analysis by a client. It contains analysis instances.
"""
import datetime
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.date_time_field import DateTimeField
from fields.fixed_point_field import FixedPointField
from fields.widget.widget import StringWidget, TextAreaWidget, \
                                BooleanWidget, DateTimeWidget, \
                                DecimalWidget, RichWidget
from openerp import fields, models, api,netsvc
from openerp.tools.translate import _
from openerp.osv import osv
import logging
import openerp
import base64
from models import InMemoryZip
from lxml import etree
from openerp.osv.orm import setup_modifiers
_logger = logging.getLogger(__name__)

AR_STATES = (
    ('sample_registered','Sample Registered'),
    ('not_requested','Not Requested'),
    ('pre_enter','Pre-enter'),
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
    ('3', '4'),
    ('4', '5'),
    ('5', '6'),
    ('6', '7'),
    ('7', '8'),
    ('8', '9'),
    ('9', '10'),
    )

schema = (fields.Char(string='RequestID',
                      compute='compute_analysisRequestId',
                      store=True
        ),
    fields.Integer(string='ar_counter'),
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
    fields.Many2many(string='Contact4',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact5',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact6',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact7',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact8',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=False
    ),
    fields.Many2many(string='Contact9',
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
    fields.Many2many(string='CCContact4',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact5',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact6',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact7',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact8',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    fields.Many2many(string='CCContact9',
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
    fields.Many2many(
        string='CCEmails4',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails5',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails6',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails7',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails8',
        comodel_name="olims.email"
    ),
    fields.Many2many(
        string='CCEmails9',
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
    fields.Many2one(string='Sample_id4',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id5',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id6',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id7',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id8',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Sample_id9',
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
    fields.Many2one(string='Batch4',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch5',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch6',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch7',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch8',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='Batch9',
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
    fields.Many2one(string='SubGroup4',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup5',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup6',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup7',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup8',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='SubGroup9',
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
    fields.Many2one(string='Template4',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template5',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template6',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template7',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template8',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='Template9',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2many(string='AnalysisProfile',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile1',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile2',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile3',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile4',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile5',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile6',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile7',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile8',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.Many2many(string='AnalysisProfile9',
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
    fields.Many2one(string='Sampler4',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler5',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler6',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler7',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler8',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    fields.Many2one(string='Sampler9',
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
    DateTimeField(
        'SamplingDate4',
        required=0,
    ),
    DateTimeField(
        'SamplingDate5',
        required=0,
    ),
    DateTimeField(
        'SamplingDate6',
        required=0,
    ),
    DateTimeField(
        'SamplingDate7',
        required=0,
    ),
    DateTimeField(
        'SamplingDate8',
        required=0,
    ),
    DateTimeField(
        'SamplingDate9',
        required=0,
    ),
    fields.Many2one(string='SampleType',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=True

    ),
    fields.Many2one(string='SampleType1',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType2',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType3',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType4',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType5',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType6',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType7',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType8',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
                        required=False

    ),
    fields.Many2one(string='SampleType9',
                        comodel_name='olims.sample_type',
                        domain="[('Deactivated', '=',False )]",
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
    fields.Many2one(string='Specification4',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification5',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification6',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification7',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification8',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='Specification9',
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
    fields.Many2one(string='SamplePoint4',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint5',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint6',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint7',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint8',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='SamplePoint9',
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
    fields.Many2one(string='StorageLocation4',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation5',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation6',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation7',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation8',
                        comodel_name='olims.storage_location',

    ),
    fields.Many2one(string='StorageLocation9',
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
    StringField(
        'LotID4',
    ),
    StringField(
        'LotID5',
    ),
    StringField(
        'LotID6',
    ),
    StringField(
        'LotID7',
    ),
    StringField(
        'LotID8',
    ),
    StringField(
        'LotID9',
    ),
    #Batch ID Field

    StringField(
        'BatchID',
    ),
    StringField(
        'BatchID1',
    ),
    StringField(
        'BatchID2',
    ),
    StringField(
        'BatchID3',
    ),
    StringField(
        'BatchID4',
    ),
    StringField(
        'BatchID5',
    ),
    StringField(
        'BatchID6',
    ),
    StringField(
        'BatchID7',
    ),
    StringField(
        'BatchID8',
    ),
    StringField(
        'BatchID9',
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
    StringField(
        'ClientReference4',
        searchable=True,
    ),
    StringField(
        'ClientReference5',
        searchable=True,
    ),
    StringField(
        'ClientReference6',
        searchable=True,
    ),
    StringField(
        'ClientReference7',
        searchable=True,
    ),
    StringField(
        'ClientReference8',
        searchable=True,
    ),
    StringField(
        'ClientReference9',
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
    StringField(
        'ClientSampleID4',
        searchable=True,
    ),
    StringField(
        'ClientSampleID5',
        searchable=True,
    ),
    StringField(
        'ClientSampleID6',
        searchable=True,
    ),
    StringField(
        'ClientSampleID7',
        searchable=True,
    ),
    StringField(
        'ClientSampleID8',
        searchable=True,
    ),
    StringField(
        'ClientSampleID9',
        searchable=True,
    ),
    #Inventory ID Field
    StringField(
        'InventoryID',
        searchable=True,
    ),
    StringField(
        'InventoryID1',
        searchable=True,
    ),
    StringField(
        'InventoryID2',
        searchable=True,
    ),
    StringField(
        'InventoryID3',
        searchable=True,
    ),
    StringField(
        'InventoryID4',
        searchable=True,
    ),
    StringField(
        'InventoryID5',
        searchable=True,
    ),
    StringField(
        'InventoryID6',
        searchable=True,
    ),
    StringField(
        'InventoryID7',
        searchable=True,
    ),
    StringField(
        'InventoryID8',
        searchable=True,
    ),
    StringField(
        'InventoryID9',
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
    fields.Many2one(string='SamplingDeviation4',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation5',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation6',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation7',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation8',
                        comodel_name='olims.sampling_deviation',

    ),
    fields.Many2one(string='SamplingDeviation9',
                        comodel_name='olims.sampling_deviation',

    ),
    # Sample field
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
    fields.Many2one(string='SampleCondition4',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition5',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition6',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition7',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition8',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='SampleCondition9',
                        comodel_name='olims.sample_condition',

    ),

    # Sample field
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
    fields.Many2one(string='DefaultContainerType4',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType5',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType6',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType7',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType8',
                        comodel_name='olims.container_type',

    ),
    fields.Many2one(string='DefaultContainerType9',
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
    BooleanField(
        'AdHoc4',
        default=False,
    ),
    BooleanField(
        'AdHoc5',
        default=False,
    ),
    BooleanField(
        'AdHoc6',
        default=False,
    ),
    BooleanField(
        'AdHoc7',
        default=False,
    ),
    BooleanField(
        'AdHoc8',
        default=False,
    ),
    BooleanField(
        'AdHoc9',
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
        'Composite4',
        default=False,
    ),
    BooleanField(
        'Composite5',
        default=False,
    ),
    BooleanField(
        'Composite6',
        default=False,
    ),
    BooleanField(
        'Composite7',
        default=False,
    ),
    BooleanField(
        'Composite8',
        default=False,
    ),
    BooleanField(
        'Composite9',
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
    BooleanField(
        'InvoiceExclude4',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude5',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude6',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude7',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude8',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude9',
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
    TextField(
      string='Remarks1',
      compute='get_remarks_of_ar',
      inverse='set_remarks_remark1',
    ),
    TextField(
      string='Remarks2',
      compute='get_remarks_of_ar',
      inverse='set_remarks_remark2',
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
                   required=1,
                    default=lambda self: self.env['olims.ar_priority'].search([('Default', '=', True)]),

    ),

    TextField('PriorityDescription',
              related='Priority.Description',
              store=True,
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
    fields.Many2one(string='Priority4',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority5',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority6',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority7',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority8',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    fields.Many2one(string='Priority9',
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
    fields.Float(string='Discount4',
                 default=0.00,
    ),
    fields.Float(string='Discount5',
                 default=0.00,
    ),
    fields.Float(string='Discount6',
                 default=0.00,
    ),
    fields.Float(string='Discount7',
                 default=0.00,
    ),
    fields.Float(string='Discount8',
                 default=0.00,
    ),
    fields.Float(string='Discount9',
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
    fields.Float(string='Subtotal4',
                 default=0.00,
    ),
    fields.Float(string='Subtotal5',
                 default=0.00,
    ),
    fields.Float(string='Subtotal6',
                 default=0.00,
    ),
    fields.Float(string='Subtotal7',
                 default=0.00,
    ),
    fields.Float(string='Subtotal8',
                 default=0.00,
    ),
    fields.Float(string='Subtotal9',
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
    fields.Float(string='VAT4',
                 default=0.00,
    ),
    fields.Float(string='VAT5',
                 default=0.00,
    ),
    fields.Float(string='VAT6',
                 default=0.00,
    ),
    fields.Float(string='VAT7',
                 default=0.00,
    ),
    fields.Float(string='VAT8',
                 default=0.00,
    ),
    fields.Float(string='VAT9',
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
    fields.Float(string='Total4',
                 default=0.00,
    ),
    fields.Float(string='Total5',
                 default=0.00,
    ),
    fields.Float(string='Total6',
                 default=0.00,
    ),
    fields.Float(string='Total7',
                 default=0.00,
    ),
    fields.Float(string='Total8',
                 default=0.00,
    ),
    fields.Float(string='Total9',
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

    fields.One2many(string="Field_Published_Result",
        comodel_name="olims.manage_analyses",
        inverse_name="manage_analysis_id"),
    fields.One2many(string="Lab_Published_Result",
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
    fields.Many2one(string='client_contact_email_template',
        comodel_name="olims.template"),
    fields.Many2one(string='client_contact_email_template1',
        comodel_name="olims.template"),
    fields.Many2one(string='client_contact_email_template2',
        comodel_name="olims.template"),
    fields.Many2one(string='client_contact_email_template3',
        comodel_name="olims.template"),
    fields.Boolean(string='is_flagged',
        default=False),
    fields.Char(string="flagged_status",compute='set_flagged_status', store=True),
    TextField(
        string='flagged_comments',
        searchable=True,
    ),
    fields.Boolean(
        string='pre_enter',
        default=False,
        ),
    # fields.Many2one(string='worksheet',
    #     comodel_name='olims.worksheet'
    # ),
    fields.Many2many(string='ar_worksheets',
                    comodel_name='olims.worksheet',
                    relation='olims_ar_worksheets',
                    required=False
    ),
    fields.Boolean(string='paid_cash',
        default=False),
    fields.Boolean(string='paid_cash1',
        default=False),
    fields.Boolean(string='paid_cash2',
        default=False),
    fields.Boolean(string='paid_cash3',
        default=False),
    fields.Boolean(string='paid_cash4',
        default=False),
    fields.Boolean(string='paid_cash5',
        default=False),
    fields.Boolean(string='paid_cash6',
        default=False),
    fields.Boolean(string='paid_cash7',
        default=False),
    fields.Boolean(string='paid_cash8',
        default=False),
    fields.Boolean(string='paid_cash9',
        default=False),
    fields.Boolean(string="copy_paid_cash", default=False),


    StringField(
        'SampleMassReceived',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived1',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived2',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived3',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived4',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived5',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived6',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived7',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived8',
        searchable=True,
    ),
    StringField(
        'SampleMassReceived9',
        searchable=True,
    ),
    fields.Boolean(
        string='CopySampleMassReceived',
        default=False,
    )

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
    fields.Char(string="flag", compute="insert_flag"),
    fields.Boolean(string="is_pre_enter", compute='compute_ar_state'),
    )

class AnalysisRequest(models.Model, BaseOLiMSModel): #(BaseFolder):
    _name = 'olims.analysis_request'
    _rec_name = "RequestID"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(AnalysisRequest, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if self.env.user.has_group('olims.group_clients'):
            doc = etree.XML(res['arch'])
            if doc.xpath("//group[@name='direct_enter_ar']"):
                node = doc.xpath("//group[@name='direct_enter_ar']")[0]
                node.set('invisible', '1')
                setup_modifiers(node)
                res['arch'] = etree.tostring(doc)

        return res

    @api.multi
    def get_remarks_of_ar(self):
        for record in self:
            record.Remarks1 = record.Remarks
            record.Remarks2 = record.Remarks

    @api.multi
    def set_remarks_remark2(self):
        for record in self:
            record.write({'Remarks': record.Remarks2})

    @api.multi
    def set_remarks_remark1(self):
        for record in self:
            record.write({'Remarks': record.Remarks1})


    def cancel_analysis_request_action(self, cr, uid, ids, context=None):
        selected_ars = self.pool.get('olims.analysis_request').browse(cr, uid, ids)
        view_id = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=','Cancel Analyses Request')],\
                                                     context=context)
        for ar in selected_ars:
            if len(selected_ars) > 1:
                if ar.state in ['sample_registered','not_requested','pre_enter','sampled',\
                                'to_be_preserved','sample_due','sample_received','attachment_due','to_be_verified',\
                                'verified']:
                    raise osv.except_osv(_('error'),
                                         _('Analysis Requests can not be canceled.'))


        return {
            'name': _('Cancel'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'olims.message_dialog_box',
            'view_id' : view_id[0],
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context' : context,
        }

    def fill_olims_analysis_request_sample_rel(self,cr, uid, context=None):
        analysis_request  = self.pool.get('olims.analysis_request')
        sample_objs = self.pool.get('olims.sample').search_read(cr, uid, [])
        for obj_dict in sample_objs:
            corresponding_ars = analysis_request.search(cr, uid, [('Sample_id', '=', obj_dict.get('id'))])
            if corresponding_ars:
                self.pool.get('olims.sample').write(cr, uid, [obj_dict.get('id')], {'Corresponding_ARs':  [(6,0, [corresponding_ars])]})


    @api.onchange('SampleType')
    def _sampletype_onchange(self):

        profile_list = []
        res = {}
        client = False
        if self._context.get('client_context'):
            client = self._context.get('client_context')
        elif self._context.get('default_Client'):
            # default_Client passed in context when creating AR from Samples
            client = self._context.get('default_Client')
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles =  client_obj.Analysis_Profile
        for profile in self.SampleType.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile': [('id', 'in', profile_list)]}
        return res


    @api.onchange('SampleType1')
    def _sampletype1_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles =  client_obj.Analysis_Profile
        for profile in self.SampleType1.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile1': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType2')
    def _sampletype2_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType2.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile2': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType3')
    def _sampletype3_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType3.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile3': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType4')
    def _sampletype4_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType4.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile4': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType5')
    def _sampletype5_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType5.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile5': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType6')
    def _sampletype6_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType6.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile6': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType7')
    def _sampletype7_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType7.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile7': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType8')
    def _sampletype8_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType8.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile8': [('id', 'in', profile_list)]}
        return res

    @api.onchange('SampleType9')
    def _sampletype9_onchange(self):

        profile_list = []
        res = {}
        client = self._context.get('client_context', None)
        client_obj = self.env['olims.client'].search([("id", "=", client)])
        client_profiles = client_obj.Analysis_Profile
        for profile in self.SampleType9.AnalysisProfile:
            if profile in client_profiles:
                profile_list.append(profile.id)

        res['domain'] = {'AnalysisProfile9': [('id', 'in', profile_list)]}
        return res

    @api.model
    def _generate_order_by(self, order_spec, query):
        sort_order = """ to_number(textcat('0', SUBSTRING("RequestID",3,LENGTH("RequestID"))), text('99999999')) ,"RequestID"  """
        if order_spec:
            if order_spec == "AnalysisProfile ASC" or order_spec == "AnalysisProfile DESC":
                return super(AnalysisRequest, self)._generate_order_by(order_spec, query)

            return super(AnalysisRequest, self)._generate_order_by(order_spec, query) + ", " + sort_order
        return " order by " + sort_order

    @api.depends("Contact")
    def compute_analysisRequestId(self):
        for record in self:
            record.RequestID = 'Not Assigned'

    def compute_analysis_request_number(self, cr, uid, ids):

        cr.execute('select ar_counter from olims_analysis_request  where "ar_counter" is not null order by ar_counter desc limit 1')
        id_returned = cr.fetchone()
        return id_returned[0] # return id only

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
        sample_id = values.get('Sample_id')
        list_of_dicts = []
        count = 0
        analysis_request_0_dict, analysis_request_1_dict, analysis_request_2_dict,\
        analysis_request_3_dict, analysis_request_4_dict, analysis_request_5_dict,\
        analysis_request_6_dict, analysis_request_7_dict, analysis_request_8_dict,\
        analysis_request_9_dict = self.get_fields_value_dicts(values)
        data, data1, data2, data3,\
        data4, data5, data6, data7,\
        data8, data9,\
        field_result_list, lab_result_list,\
        field_result_list_profile1, lab_result_list_profile1,\
        field_result_list_profile2, lab_result_list_profile2,\
        field_result_list_profile3, lab_result_list_profile3,\
        field_result_list_profile4, lab_result_list_profile4,\
        field_result_list_profile5, lab_result_list_profile5,\
        field_result_list_profile6, lab_result_list_profile6,\
        field_result_list_profile7, lab_result_list_profile7,\
        field_result_list_profile8, lab_result_list_profile8,\
        field_result_list_profile9, lab_result_list_profile9 = self.create_field_and_lab_analyses(values)

        analysis_request_0_dict.update({"Field_Manage_Result": field_result_list,
            "Lab_Manage_Result": lab_result_list})
        analysis_request_1_dict.update({"Field_Manage_Result": field_result_list_profile1,
            "Lab_Manage_Result": lab_result_list_profile1})
        analysis_request_2_dict.update({"Field_Manage_Result": field_result_list_profile2,
            "Lab_Manage_Result": lab_result_list_profile2})
        analysis_request_3_dict.update({"Field_Manage_Result": field_result_list_profile3,
                                        "Lab_Manage_Result": lab_result_list_profile3})
        analysis_request_4_dict.update({"Field_Manage_Result": field_result_list_profile4,
            "Lab_Manage_Result": lab_result_list_profile4})
        analysis_request_5_dict.update({"Field_Manage_Result": field_result_list_profile5,
            "Lab_Manage_Result": lab_result_list_profile5})
        analysis_request_6_dict.update({"Field_Manage_Result": field_result_list_profile6,
                                        "Lab_Manage_Result": lab_result_list_profile6})
        analysis_request_7_dict.update({"Field_Manage_Result": field_result_list_profile7,
            "Lab_Manage_Result": lab_result_list_profile7})
        analysis_request_8_dict.update({"Field_Manage_Result": field_result_list_profile8,
            "Lab_Manage_Result": lab_result_list_profile8})
        analysis_request_9_dict.update({"Field_Manage_Result": field_result_list_profile9,
                                        "Lab_Manage_Result": lab_result_list_profile9})

        list_of_dicts.append(analysis_request_0_dict)
        list_of_dicts.append(analysis_request_1_dict)
        list_of_dicts.append(analysis_request_2_dict)
        list_of_dicts.append(analysis_request_3_dict)
        list_of_dicts.append(analysis_request_4_dict)
        list_of_dicts.append(analysis_request_5_dict)
        list_of_dicts.append(analysis_request_6_dict)
        list_of_dicts.append(analysis_request_7_dict)
        list_of_dicts.append(analysis_request_8_dict)
        list_of_dicts.append(analysis_request_9_dict)

        for ar_values in list_of_dicts:
            if ar_values.get("Contact") and ar_values.get('SamplingDate') and ar_values.get('SampleType'):
                if ar_values.get("InvoiceExclude", None):
                    ar_values["Discount"] = 0.0
                    ar_values["Subtotal"] = 0.0
                    ar_values["VAT"] = 0.0
                    ar_values["Total"] = 0.0
                res = super(AnalysisRequest, self).create(ar_values)
                if not values.get('pre_enter',None):
                    res.write({'state':'pre_enter'})
                else:
                    ar_counter_id = self.env["olims.analysis_request"].search([('ar_counter', '!=', False)],order='ar_counter desc', limit=1)
                    last_id = ar_counter_id.ar_counter
                    new_id = int(last_id) + 1
                    request_id = 'R-0' + str(new_id)
                    res.write({'RequestID': request_id, 'ar_counter' : new_id, 'pre_enter': True})
                if not values.get('Sample_id',None):
                    new_sample = self.create_sample(ar_values, res)
                    analysis_object = super(AnalysisRequest, self).search([('id', '=',res.id)])
                    analysis_object.write({"Sample_id":new_sample.id})
                    sample_id = new_sample.id
                else:
                    analysis_object = super(AnalysisRequest, self).search([('id', '=',res.id)])
                    analysis_object.write({"Sample_id":values.get('Sample_id',None),
                                           "SamplingDate":values.get('SamplingDate',None),
                                           "SampleType":values.get('SampleType',None),
                                           "ClientReference":values.get('ClientReference',None),
                                           "ClientSampleID":values.get('ClientSampleID',None),
                                           "SamplePoint":values.get('SamplePoint',None),
                                           "StorageLocation":values.get('StorageLocation',None),
                                           "SamplingDeviation":values.get('SamplingDeviation',None),
                                           "SampleCondition":values.get('SampleCondition',None),
                                           "LotID":values.get('LotID',None)
                                           })

                ar_p = self.create_ar_partitions(res)
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
                elif count == 4:
                    for rec in data4:
                        self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                elif count == 5:
                    for rec in data5:
                        self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                elif count == 6:
                    for rec in data6:
                        self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                elif count == 7:
                    for rec in data7:
                        self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                elif count == 8:
                    for rec in data8:
                        self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                elif count == 9:
                    for rec in data9:
                        self.create_analyses(ar_analysis_object, ar_p, ar_values, rec, res)
                count += 1

        query = "insert into olims_analysis_request_sample_rel values ("+str(sample_id)+\
                ","+str(res.id)+")"
        self.env.cr.execute(query)
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
            'InventoryID':ar_values.get('InventoryID'),
            'BatchID':ar_values.get('BatchID'),
            'Contact':ar_values.get('Contact'),
            'CCEmails':ar_values.get('CCEmails'),
            'Sampler':ar_values.get('Sampler')
        }
        sample_object = self.env["olims.sample"]
        new_sample = sample_object.create(smaple_vals_dict)
        return new_sample

    def create_field_and_lab_analyses(self, values):
        data = []
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        data7 = []
        data8 = []
        data9 = []
        lab_result_list = []
        field_result_list = []
        lab_result_list_p1 = []
        field_result_list_p1 = []
        lab_result_list_p2 = []
        field_result_list_p2 = []
        lab_result_list_p3 = []
        field_result_list_p3 = []
        lab_result_list_p4 = []
        field_result_list_p4 = []
        lab_result_list_p5 = []
        field_result_list_p5 = []
        lab_result_list_p6 = []
        field_result_list_p6 = []
        lab_result_list_p7 = []
        field_result_list_p7 = []
        lab_result_list_p8 = []
        field_result_list_p8 = []
        lab_result_list_p9 = []
        field_result_list_p9 = []
        profile_analysis_id_list = []
        profile1_analysis_id_list = []
        profile2_analysis_id_list = []
        profile3_analysis_id_list = []
        profile4_analysis_id_list = []
        profile5_analysis_id_list = []
        profile6_analysis_id_list = []
        profile7_analysis_id_list = []
        profile8_analysis_id_list = []
        profile9_analysis_id_list = []
        if values.get('AnalysisProfile', None):
            for val in values.get('AnalysisProfile', None):
                print "----", val
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile1', None):
            for val in values.get('AnalysisProfile1', None):
                print "----", val
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile1_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile2', None):
            for val in values.get('AnalysisProfile2', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile2_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile3', None):
            for val in values.get('AnalysisProfile3', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile3_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile4', None):
            for val in values.get('AnalysisProfile4', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile4_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile5', None):
            for val in values.get('AnalysisProfile5', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile5_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile6', None):
            for val in values.get('AnalysisProfile6', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile6_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile7', None):
            for val in values.get('AnalysisProfile7', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile7_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile8', None):
            for val in values.get('AnalysisProfile8', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile8_analysis_id_list.append(analysis.Services.id)

        if values.get('AnalysisProfile9', None):
            for val in values.get('AnalysisProfile9', None):
                for ids in val[2]:
                    print "----", ids
                    analysis_profile_obj = self.env["olims.analysis_profile"].search([('id', '=', ids)])
                    for analysis in analysis_profile_obj.Service:
                        profile9_analysis_id_list.append(analysis.Services.id)

        for LabService in values.get('LabService'):
            if LabService[2]['LabService'] in profile_analysis_id_list:
                self.update_lab_service_obj(LabService, data, lab_result_list)
            if LabService[2]['LabService'] in profile1_analysis_id_list:
                self.update_lab_service_obj(LabService, data1, lab_result_list_p1)
            if LabService[2]['LabService'] in profile2_analysis_id_list:
                self.update_lab_service_obj(LabService, data2, lab_result_list_p2)
            if LabService[2]['LabService'] in profile3_analysis_id_list:
                self.update_lab_service_obj(LabService, data3, lab_result_list_p3)
            if LabService[2]['LabService'] in profile4_analysis_id_list:
                self.update_lab_service_obj(LabService, data4, lab_result_list_p4)
            if LabService[2]['LabService'] in profile5_analysis_id_list:
                self.update_lab_service_obj(LabService, data5, lab_result_list_p5)
            if LabService[2]['LabService'] in profile6_analysis_id_list:
                self.update_lab_service_obj(LabService, data6, lab_result_list_p6)
            if LabService[2]['LabService'] in profile7_analysis_id_list:
                self.update_lab_service_obj(LabService, data7, lab_result_list_p7)
            if LabService[2]['LabService'] in profile8_analysis_id_list:
                self.update_lab_service_obj(LabService, data8, lab_result_list_p8)
            if LabService[2]['LabService'] in profile9_analysis_id_list:
                self.update_lab_service_obj(LabService, data9, lab_result_list_p9)

            if LabService[2]['LabService'] not in profile_analysis_id_list and \
                            LabService[2]['LabService'] not in profile1_analysis_id_list and \
                            LabService[2]['LabService'] not in profile2_analysis_id_list and \
                            LabService[2]['LabService'] not in profile3_analysis_id_list and \
                            LabService[2]['LabService'] not in profile4_analysis_id_list and \
                            LabService[2]['LabService'] not in profile5_analysis_id_list and \
                            LabService[2]['LabService'] not in profile6_analysis_id_list and \
                            LabService[2]['LabService'] not in profile7_analysis_id_list and \
                            LabService[2]['LabService'] not in profile8_analysis_id_list and \
                            LabService[2]['LabService'] not in profile9_analysis_id_list:
                Specification = ">" + str(LabService[2]['Min']) + ", <" + str(LabService[2]['Max'])
                service_instance = self.env['olims.analysis_service'].search([('id', '=', LabService[2]['LabService'])])
                if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
                    LabService[2].update({'Method': service_instance._Method.id})
                elif service_instance.InstrumentEntryOfResults:
                    LabService[2].update({'Method': None, 'Instrument': service_instance.Instrument})
                LabService[2].update({'Specifications': Specification,
                              "Due Date": datetime.datetime.now()})
                lab_result_list.append([0, 0, LabService[2]])
                lab_result_list_p1.append([0, 0, LabService[2]])
                lab_result_list_p2.append([0, 0, LabService[2]])
                lab_result_list_p3.append([0, 0, LabService[2]])
                lab_result_list_p4.append([0, 0, LabService[2]])
                lab_result_list_p5.append([0, 0, LabService[2]])
                lab_result_list_p6.append([0, 0, LabService[2]])
                lab_result_list_p7.append([0, 0, LabService[2]])
                lab_result_list_p8.append([0, 0, LabService[2]])
                lab_result_list_p9.append([0, 0, LabService[2]])
                data.append(LabService)
                data1.append(LabService)
                data2.append(LabService)
                data3.append(LabService)
                data4.append(LabService)
                data5.append(LabService)
                data6.append(LabService)
                data7.append(LabService)
                data8.append(LabService)
                data9.append(LabService)
        for FieldService in values.get('FieldService'):

            if FieldService[2]['Service'] in profile_analysis_id_list:
                self.update_field_service_obj(FieldService, data, field_result_list)
            if FieldService[2]['Service'] in profile1_analysis_id_list:
                self.update_field_service_obj(FieldService, data1, field_result_list_p1)
            if FieldService[2]['Service'] in profile2_analysis_id_list:
                self.update_field_service_obj(FieldService, data2, field_result_list_p2)
            if FieldService[2]['Service'] in profile3_analysis_id_list:
                self.update_field_service_obj(FieldService, data3, field_result_list_p3)
            if FieldService[2]['Service'] in profile4_analysis_id_list:
                self.update_field_service_obj(FieldService, data4, field_result_list_p4)
            if FieldService[2]['Service'] in profile5_analysis_id_list:
                self.update_field_service_obj(FieldService, data5, field_result_list_p5)
            if FieldService[2]['Service'] in profile6_analysis_id_list:
                self.update_field_service_obj(FieldService, data6, field_result_list_p6)
            if FieldService[2]['Service'] in profile7_analysis_id_list:
                self.update_field_service_obj(FieldService, data7, field_result_list_p7)
            if FieldService[2]['Service'] in profile8_analysis_id_list:
                self.update_field_service_obj(FieldService, data8, field_result_list_p8)
            if FieldService[2]['Service'] in profile9_analysis_id_list:
                self.update_field_service_obj(FieldService, data9, field_result_list_p9)

            if FieldService[2]['Service'] not in profile_analysis_id_list and \
                            FieldService[2]['Service'] not in profile1_analysis_id_list and \
                            FieldService[2]['Service'] not in profile2_analysis_id_list and \
                            FieldService[2]['Service'] not in profile3_analysis_id_list and \
                            FieldService[2]['Service'] not in profile4_analysis_id_list and \
                            FieldService[2]['Service'] not in profile5_analysis_id_list and \
                            FieldService[2]['Service'] not in profile6_analysis_id_list and \
                            FieldService[2]['Service'] not in profile7_analysis_id_list and \
                            FieldService[2]['Service'] not in profile8_analysis_id_list and \
                            FieldService[2]['Service'] not in profile9_analysis_id_list:
                Specification = ">" + str(FieldService[2]['Min']) + ", <" + str(FieldService[2]['Max'])
                service_instance = self.env['olims.analysis_service'].search([('id', '=', FieldService[2]['Service'])])
                if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
                    FieldService[2].update({'Method': service_instance._Method.id})
                elif service_instance.InstrumentEntryOfResults:
                    FieldService[2].update({'Method': None, 'Instrument': service_instance.Instrument})
                FieldService[2].update({'Specifications': Specification,
                                "Due Date": datetime.datetime.now()})
                field_result_list.append([0, 0, FieldService[2]])
                data.append(FieldService)
                field_result_list_p1.append([0, 0, FieldService[2]])
                data1.append(FieldService)
                field_result_list_p2.append([0, 0, FieldService[2]])
                data2.append(FieldService)
                field_result_list_p3.append([0, 0, FieldService[2]])
                data3.append(FieldService)
                field_result_list_p4.append([0, 0, FieldService[2]])
                data4.append(FieldService)
                field_result_list_p5.append([0, 0, FieldService[2]])
                data5.append(FieldService)
                field_result_list_p6.append([0, 0, FieldService[2]])
                data6.append(FieldService)
                field_result_list_p7.append([0, 0, FieldService[2]])
                data7.append(FieldService)
                field_result_list_p8.append([0, 0, FieldService[2]])
                data8.append(FieldService)
                field_result_list_p9.append([0, 0, FieldService[2]])
                data9.append(FieldService)

        return data, data1, data2, data3,\
               data4, data5, data6, data7,\
               data8, data9,\
               field_result_list, lab_result_list,\
               field_result_list_p1, lab_result_list_p1,\
               field_result_list_p2, lab_result_list_p2,\
               field_result_list_p3, lab_result_list_p3,\
               field_result_list_p4, lab_result_list_p4,\
               field_result_list_p5, lab_result_list_p5,\
               field_result_list_p6, lab_result_list_p6,\
               field_result_list_p7, lab_result_list_p7,\
               field_result_list_p8, lab_result_list_p8,\
               field_result_list_p9, lab_result_list_p9

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
            'InventoryID': values.get('InventoryID', None),
            'LotID': values.get('LotID', None),
            'BatchID': values.get('BatchID', None),
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
            'paid_cash': values.get('paid_cash', None),
            'SampleMassReceived': values.get('SampleMassReceived',None),
            'Sampler':values.get('Sampler',None)
        }

        analysis_request_1_dict = {
            'StorageLocation': values.get('StorageLocation1', None),
            'AdHoc': values.get('AdHoc1', None),
            'Template': values.get('Template1', None),
            'AnalysisProfile': values.get('AnalysisProfile1', None),
            'ClientSampleID': values.get('ClientSampleID1', None),
            'InventoryID': values.get('InventoryID1', None),
            'LotID': values.get('LotID1', None),
            'BatchID': values.get('BatchID1', None),
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
            'paid_cash': values.get('paid_cash1', None),
            'SampleMassReceived': values.get('SampleMassReceived1',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_2_dict = {
            'StorageLocation': values.get('StorageLocation2', None),
            'AdHoc': values.get('AdHoc2', None),
            'Template': values.get('Template2', None),
            'AnalysisProfile': values.get('AnalysisProfile2', None),
            'ClientSampleID': values.get('ClientSampleID2', None),
            'InventoryID': values.get('InventoryID2', None),
            'LotID': values.get('LotID2', None),
            'BatchID': values.get('BatchID2', None),
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
            'paid_cash': values.get('paid_cash2', None),
            'SampleMassReceived': values.get('SampleMassReceived2',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_3_dict = {
            'StorageLocation': values.get('StorageLocation3', None),
            'AdHoc': values.get('AdHoc3', None),
            'Template': values.get('Template3', None),
            'AnalysisProfile': values.get('AnalysisProfile3', None),
            'ClientSampleID': values.get('ClientSampleID3', None),
            'InventoryID': values.get('InventoryID3', None),
            'LotID': values.get('LotID3', None),
            'BatchID': values.get('BatchID3', None),
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
            'paid_cash': values.get('paid_cash3', None),
            'SampleMassReceived': values.get('SampleMassReceived3',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_4_dict = {
            'StorageLocation': values.get('StorageLocation4', None),
            'AdHoc': values.get('AdHoc4', None),
            'Template': values.get('Template4', None),
            'AnalysisProfile': values.get('AnalysisProfile4', None),
            'ClientSampleID': values.get('ClientSampleID4', None),
            'InventoryID': values.get('InventoryID4', None),
            'LotID': values.get('LotID4', None),
            'BatchID': values.get('BatchID4', None),
            'SubGroup': values.get('SubGroup4', None),
            'SampleType': values.get('SampleType4', None),
            'Batch': values.get('Batch4', None),
            'SamplingDeviation': values.get('SamplingDeviation4', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint4', None),
            'Specification': values.get('Specification4', None),
            'Priority': values.get('Priority4', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate4', None),
            'Contact': values.get('Contact4', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails4', None),
            'CCContact': values.get('CCContact4', None),
            'Sampler': values.get('Sampler4', None),
            'Composite': values.get('Composite4', None),
            'Sample_id': values.get('Sample_id4', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude4', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition4', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType4', None),
            'ClientReference': values.get('ClientReference4',None),
            'Subtotal': values.get('Subtotal4',None),
            'Discount': values.get('Discount4',None),
            'VAT': values.get('VAT4',None),
            'Total': values.get('Total4',None),
            'paid_cash': values.get('paid_cash4', None),
            'SampleMassReceived': values.get('SampleMassReceived4',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_5_dict = {
            'StorageLocation': values.get('StorageLocation5', None),
            'AdHoc': values.get('AdHoc5', None),
            'Template': values.get('Template5', None),
            'AnalysisProfile': values.get('AnalysisProfile5', None),
            'ClientSampleID': values.get('ClientSampleID5', None),
            'InventoryID': values.get('InventoryID5', None),
            'LotID': values.get('LotID5', None),
            'BatchID': values.get('BatchID5', None),
            'SubGroup': values.get('SubGroup5', None),
            'SampleType': values.get('SampleType5', None),
            'Batch': values.get('Batch5', None),
            'SamplingDeviation': values.get('SamplingDeviation5', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint5', None),
            'Specification': values.get('Specification5', None),
            'Priority': values.get('Priority5', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate5', None),
            'Contact': values.get('Contact5', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails5', None),
            'CCContact': values.get('CCContact5', None),
            'Sampler': values.get('Sampler5', None),
            'Composite': values.get('Composite5', None),
            'Sample_id': values.get('Sample_id5', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude5', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition5', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType5', None),
            'ClientReference': values.get('ClientReference5',None),
            'Subtotal': values.get('Subtotal5',None),
            'Discount': values.get('Discount5',None),
            'VAT': values.get('VAT5',None),
            'Total': values.get('Total5',None),
            'paid_cash': values.get('paid_cash5', None),
            'SampleMassReceived': values.get('SampleMassReceived5',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_6_dict = {
            'StorageLocation': values.get('StorageLocation6', None),
            'AdHoc': values.get('AdHoc6', None),
            'Template': values.get('Template6', None),
            'AnalysisProfile': values.get('AnalysisProfile6', None),
            'ClientSampleID': values.get('ClientSampleID6', None),
            'InventoryID': values.get('InventoryID6', None),
            'LotID': values.get('LotID6', None),
            'BatchID': values.get('BatchID6', None),
            'SubGroup': values.get('SubGroup6', None),
            'SampleType': values.get('SampleType6', None),
            'Batch': values.get('Batch6', None),
            'SamplingDeviation': values.get('SamplingDeviation6', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint6', None),
            'Specification': values.get('Specification6', None),
            'Priority': values.get('Priority6', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate6', None),
            'Contact': values.get('Contact6', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails6', None),
            'CCContact': values.get('CCContact6', None),
            'Sampler': values.get('Sampler6', None),
            'Composite': values.get('Composite6', None),
            'Sample_id': values.get('Sample_id6', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude6', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition6', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType6', None),
            'ClientReference': values.get('ClientReference6',None),
            'Subtotal': values.get('Subtotal6',None),
            'Discount': values.get('Discount6',None),
            'VAT': values.get('VAT6',None),
            'Total': values.get('Total6',None),
            'paid_cash': values.get('paid_cash6', None),
            'SampleMassReceived': values.get('SampleMassReceived6',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_7_dict = {
            'StorageLocation': values.get('StorageLocation7', None),
            'AdHoc': values.get('AdHoc7', None),
            'Template': values.get('Template7', None),
            'AnalysisProfile': values.get('AnalysisProfile7', None),
            'ClientSampleID': values.get('ClientSampleID7', None),
            'InventoryID': values.get('InventoryID7', None),
            'LotID': values.get('LotID7', None),
            'BatchID': values.get('BatchID7', None),
            'SubGroup': values.get('SubGroup7', None),
            'SampleType': values.get('SampleType7', None),
            'Batch': values.get('Batch7', None),
            'SamplingDeviation': values.get('SamplingDeviation7', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint7', None),
            'Specification': values.get('Specification7', None),
            'Priority': values.get('Priority7', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate7', None),
            'Contact': values.get('Contact7', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails7', None),
            'CCContact': values.get('CCContact7', None),
            'Sampler': values.get('Sampler7', None),
            'Composite': values.get('Composite7', None),
            'Sample_id': values.get('Sample_id7', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude7', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition7', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType7', None),
            'ClientReference': values.get('ClientReference7',None),
            'Subtotal': values.get('Subtotal7',None),
            'Discount': values.get('Discount7',None),
            'VAT': values.get('VAT7',None),
            'Total': values.get('Total7',None),
            'paid_cash': values.get('paid_cash7', None),
            'SampleMassReceived': values.get('SampleMassReceived7',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_8_dict = {
            'StorageLocation': values.get('StorageLocation8', None),
            'AdHoc': values.get('AdHoc8', None),
            'Template': values.get('Template8', None),
            'AnalysisProfile': values.get('AnalysisProfile8', None),
            'ClientSampleID': values.get('ClientSampleID8', None),
            'InventoryID': values.get('InventoryID8', None),
            'LotID': values.get('LotID8', None),
            'BatchID': values.get('BatchID8', None),
            'SubGroup': values.get('SubGroup8', None),
            'SampleType': values.get('SampleType8', None),
            'Batch': values.get('Batch8', None),
            'SamplingDeviation': values.get('SamplingDeviation8', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint8', None),
            'Specification': values.get('Specification8', None),
            'Priority': values.get('Priority8', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate8', None),
            'Contact': values.get('Contact8', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails8', None),
            'CCContact': values.get('CCContact8', None),
            'Sampler': values.get('Sampler8', None),
            'Composite': values.get('Composite8', None),
            'Sample_id': values.get('Sample_id8', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude8', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition8', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType8', None),
            'ClientReference': values.get('ClientReference8',None),
            'Subtotal': values.get('Subtotal8',None),
            'Discount': values.get('Discount8',None),
            'VAT': values.get('VAT8',None),
            'Total': values.get('Total8',None),
            'paid_cash': values.get('paid_cash8', None),
            'SampleMassReceived': values.get('SampleMassReceived8',None),
            'Sampler': values.get('Sampler', None)
        }
        analysis_request_9_dict = {
            'StorageLocation': values.get('StorageLocation9', None),
            'AdHoc': values.get('AdHoc9', None),
            'Template': values.get('Template9', None),
            'AnalysisProfile': values.get('AnalysisProfile9', None),
            'ClientSampleID': values.get('ClientSampleID9', None),
            'InventoryID': values.get('InventoryID9', None),
            'LotID': values.get('LotID9', None),
            'BatchID': values.get('BatchID9', None),
            'SubGroup': values.get('SubGroup9', None),
            'SampleType': values.get('SampleType9', None),
            'Batch': values.get('Batch9', None),
            'SamplingDeviation': values.get('SamplingDeviation9', None),
            'ResultsInterpretation': values.get('ResultsInterpretation', None),
            'Sample Partition': values.get('Sample Partition', None),
            'SamplePoint': values.get('SamplePoint9', None),
            'Specification': values.get('Specification9', None),
            'Priority': values.get('Priority9', None),
            'Partition': values.get('Partition', None),
            'SamplingDate': values.get('SamplingDate9', None),
            'Contact': values.get('Contact9', None),
            'FieldService': values.get('FieldService', None),
            'CCEmails': values.get('CCEmails9', None),
            'CCContact': values.get('CCContact9', None),
            'Sampler': values.get('Sampler9', None),
            'Composite': values.get('Composite9', None),
            'Sample_id': values.get('Sample_id9', None),
            'Analyses': values.get('Analyses', None),
            'Client': client,
            'InvoiceExclude': values.get('InvoiceExclude9', None),
            'LabService': values.get('LabService', None),
            'Lab_Manage_Result': values.get('Lab_Manage_Result', None),
            'result_option': values.get('result_option', None),
            'Field_Manage_Result': values.get('Field_Manage_Result', None),
            'SampleCondition': values.get('SampleCondition9', None),
            'Remarks': values.get('Remarks', None),
            'DefaultContainerType': values.get('DefaultContainerType9', None),
            'ClientReference': values.get('ClientReference9',None),
            'Subtotal': values.get('Subtotal9',None),
            'Discount': values.get('Discount9',None),
            'VAT': values.get('VAT9',None),
            'Total': values.get('Total9',None),
            'paid_cash': values.get('paid_cash9', None),
            'SampleMassReceived': values.get('SampleMassReceived9',None),
            'Sampler': values.get('Sampler', None)
        }
        return analysis_request_0_dict, analysis_request_1_dict, analysis_request_2_dict,\
               analysis_request_3_dict, analysis_request_4_dict, analysis_request_5_dict,\
               analysis_request_6_dict, analysis_request_7_dict, analysis_request_8_dict,\
               analysis_request_9_dict


    @api.multi
    def write(self, values):
        for record in self:
            if values.get("InvoiceExclude", None):
                record.write({"Discount": 0.0, "Subtotal": 0.0, "VAT": 0.0, "Total":0.0})
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

            if values.get('Adjustment', None):
                total = 0.00
                if not values.get('InvoiceExclude', None):
                    if values.get('adjustment_option') == 'amount':
                        total = record.Total + values.get('Adjustment')
                    else:
                        total = record.Total + (record.Total * values.get('Adjustment') / 100)
                    values.update({'Total': total})

        res = super(AnalysisRequest, self).write(values)
        return res  

    @api.multi
    def publish_analysis_request(self):
        if self.env.context is None:
            context = {}
        data = self.read()[0]
        self_browse = self.browse()

        datas = {
        'ids': [data.get('id')],
        'model': 'olims.analysis_request',
        'form': data
        }
        if self.LotID and self.ClientReference:
            name = self.LotID + '-' + self.ClientReference
        elif self.LotID:
            name = self.LotID
        elif self.ClientReference:
            name = self.ClientReference
        else:
            name = 'COA'


        return {
        'type': 'ir.actions.report.xml',
        'report_name': 'olims.report_certificate_of_analysis',
        'datas': datas,
        'name': name
        }

    def actionToBeSampled(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_sampled',
        }, context=context)
        return True

    def getSubtotalTotalPrice(self):
        """ Compute the price with VAT but no member discount"""
        return self.getSubtotal() + self.getSubtotalVATAmount()

    @api.onchange('Client')
    def on_client_change(self):
        #for record in self:
        if self.create_uid:
            self.Contact = None
            self.CCContact = None
            self.CCEmails = None
            self.Discount = 0.00
            self.Adjustment = 0.00
            self.VAT = 0.00
            self.Subtotal = 0.00
            self.Total = 0.00
            self.ar_worksheets = None

    @api.onchange('adjustment_option','Adjustment','InvoiceExclude')
    def Computetotalamount(self):
        total = 0.00
        for record in self:
            if record.InvoiceExclude == True:
                record.Total = total
            else :
                if record.adjustment_option =='amount':
                    total = self._origin.Total + record.Adjustment
                else:
                    total = self._origin.Total + (self._origin.Total*record.Adjustment/100)
                record.Total = total

    @api.onchange('LabService','FieldService', 'Priority', 'Priority1', 'Priority2', 'Priority3', 'Priority4'
                  'Priority5', 'Priority6', 'Priority7', 'Priority8', 'Priority9')
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

            service_discount4 = 0.0
            service_subtotal4 = 0.0
            service_vat4 = 0.0
            service_total4 = 0.0

            service_discount5 = 0.0
            service_subtotal5 = 0.0
            service_vat5 = 0.0
            service_total5 = 0.0

            service_discount6 = 0.0
            service_subtotal6 = 0.0
            service_vat6 = 0.0
            service_total6 = 0.0

            service_discount7 = 0.0
            service_subtotal7 = 0.0
            service_vat7 = 0.0
            service_total7 = 0.0

            service_discount8 = 0.0
            service_subtotal8 = 0.0
            service_vat8 = 0.0
            service_total8 = 0.0

            service_discount9 = 0.0
            service_subtotal9 = 0.0
            service_vat9 = 0.0
            service_total9 = 0.0

            profile_services_price = {}
            profile_services_VAT = {}

            profile1_services_price = {}
            profile1_services_VAT = {}

            profile2_services_price = {}
            profile2_services_VAT = {}

            profile3_services_price = {}
            profile3_services_VAT = {}

            profile4_services_price = {}
            profile4_services_VAT = {}

            profile5_services_price = {}
            profile5_services_VAT = {}

            profile6_services_price = {}
            profile6_services_VAT = {}

            profile7_services_price = {}
            profile7_services_VAT = {}

            profile8_services_price = {}
            profile8_services_VAT = {}

            profile9_services_price = {}
            profile9_services_VAT = {}

            f_service_ids_list_p1 = []
            f_service_ids_list_p2 = []
            f_service_ids_list_p3 = []
            f_service_ids_list_p4 = []
            f_service_ids_list_p5 = []
            f_service_ids_list_p6 = []
            f_service_ids_list_p7 = []
            f_service_ids_list_p8 = []
            f_service_ids_list_p9 = []
            f_service_ids_list_p10 = []

            service_ids_list_p1 = []
            service_ids_list_p2 = []
            service_ids_list_p3 = []
            service_ids_list_p4 = []
            service_ids_list_p5 = []
            service_ids_list_p6 = []
            service_ids_list_p7 = []
            service_ids_list_p8 = []
            service_ids_list_p9 = []
            service_ids_list_p10 = []

            premium_percentage1 = 0
            premium_percentage2 = 0
            premium_percentage3 = 0
            premium_percentage4 = 0
            premium_percentage5 = 0
            premium_percentage6 = 0
            premium_percentage7 = 0
            premium_percentage8 = 0
            premium_percentage9 = 0
            premium_percentage10 = 0

            for rec in record.AnalysisProfile:
                for service_p1 in rec.Service:
                    if service_p1.Services.PointOfCapture == "lab":
                        service_ids_list_p1.append(service_p1.Services.id)
                    else:
                        f_service_ids_list_p1.append(service_p1.Services.id)

            for rec in record.AnalysisProfile1:
                for service_p2 in rec.Service:
                    if service_p2.Services.PointOfCapture == "lab":
                        service_ids_list_p2.append(service_p2.Services.id)
                    else:
                        f_service_ids_list_p2.append(service_p2.Services.id)

            for rec in record.AnalysisProfile2:
                for service_p3 in rec.Service:
                    if service_p3.Services.PointOfCapture == "lab":
                        service_ids_list_p3.append(service_p3.Services.id)
                    else:
                        f_service_ids_list_p3.append(service_p3.Services.id)

            for rec in record.AnalysisProfile3:
                for service_p4 in rec.Service:
                    if service_p4.Services.PointOfCapture == "lab":
                        service_ids_list_p4.append(service_p4.Services.id)
                    else:
                        f_service_ids_list_p4.append(service_p4.Services.id)

            for rec in record.AnalysisProfile4:
                for service_p5 in rec.Service:
                    if service_p5.Services.PointOfCapture == "lab":
                        service_ids_list_p5.append(service_p5.Services.id)
                    else:
                        f_service_ids_list_p5.append(service_p5.Services.id)

            for rec in record.AnalysisProfile5:
                for service_p6 in rec.Service:
                    if service_p6.Services.PointOfCapture == "lab":
                        service_ids_list_p6.append(service_p6.Services.id)
                    else:
                        f_service_ids_list_p6.append(service_p6.Services.id)

            for rec in record.AnalysisProfile6:
                for service_p7 in rec.Service:
                    if service_p7.Services.PointOfCapture == "lab":
                        service_ids_list_p7.append(service_p7.Services.id)
                    else:
                        f_service_ids_list_p7.append(service_p7.Services.id)

            for rec in record.AnalysisProfile7:
                for service_p8 in rec.Service:
                    if service_p8.Services.PointOfCapture == "lab":
                        service_ids_list_p8.append(service_p8.Services.id)
                    else:
                        f_service_ids_list_p8.append(service_p8.Services.id)

            for rec in record.AnalysisProfile8:
                for service_p9 in rec.Service:
                    if service_p9.Services.PointOfCapture == "lab":
                        service_ids_list_p9.append(service_p9.Services.id)
                    else:
                        f_service_ids_list_p9.append(service_p9.Services.id)

            for rec in record.AnalysisProfile9:
                for service_p10 in rec.Service:
                    if service_p10.Services.PointOfCapture == "lab":
                        service_ids_list_p10.append(service_p10.Services.id)
                    else:
                        f_service_ids_list_p10.append(service_p10.Services.id)


            for service in record.LabService:
                if service.LabService.id in service_ids_list_p1:
                    for rec in record.AnalysisProfile:
                        if record.Priority:
                            premium_percentage1 = float(record.Priority.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add1 = float(rec.AnalysisProfilePrice) * premium_percentage1
                            profile_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add1
                            profile_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add1 = service.LabService.Price * premium_percentage1
                            service_price = service.LabService.Price + charges_to_add1
                            service_discount += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal += float(service_price) - float(discount)
                            # compute VAT
                            service_vat += (float(service_price) - float(discount)) * service.LabService.VAT / 100
                            service_total = service_subtotal + service_vat

            for profile, profile_price in profile_services_price.iteritems():
                service_price = profile_price
                service_discount = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal += float(service_price) - float(discount)
                # compute VAT
                service_vat = (float(service_price) - float(discount)) * profile_services_VAT[profile] / 100
                service_total += (float(service_price) - float(discount)) + service_vat

                if service.LabService.id in service_ids_list_p2:
                    for rec in record.AnalysisProfile1:
                        if record.Priority1:
                            premium_percentage2 = float(record.Priority1.Premium) / 100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add2 = float(rec.AnalysisProfilePrice) * premium_percentage2
                            profile1_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add2
                            profile1_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add2 = service.LabService.Price * premium_percentage2
                            service_price = service.LabService.Price +charges_to_add2
                            service_discount1 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal1 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat1 += (service_price - discount) * service.LabService.VAT / 100
                            service_total1 = service_subtotal1 + service_vat1

            for profile, profile_price in profile1_services_price.iteritems():
                service_price = profile_price
                service_discount1 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal1 += float(service_price) - float(discount)
                # compute VAT
                service_vat1 = (float(service_price) - float(discount)) * profile1_services_VAT[profile] / 100
                service_total1 += (float(service_price) - float(discount)) + service_vat1


                if service.LabService.id in service_ids_list_p3:
                    for rec in record.AnalysisProfile2:
                        if record.Priority2:
                            premium_percentage3 = float(record.Priority2.Premium) / 100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add3 = float(rec.AnalysisProfilePrice) * premium_percentage3
                            profile2_services_price[rec.id] = float(rec.AnalysisProfilePrice) +charges_to_add3
                            profile2_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add3 = service.LabService.Price * premium_percentage3
                            service_price = service.LabService.Price + charges_to_add3
                            service_discount2 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal2 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat2 += (service_price - discount) * service.LabService.VAT / 100
                            service_total2 = service_subtotal2 + service_vat2

            for profile, profile_price in profile2_services_price.iteritems():
                service_price = profile_price
                service_discount2 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal2 += float(service_price) - float(discount)
                # compute VAT
                service_vat2 = (float(service_price) - float(discount)) * profile2_services_VAT[profile] / 100
                service_total2 += (float(service_price) - float(discount)) + service_vat2


                if service.LabService.id in service_ids_list_p4:
                    for rec in record.AnalysisProfile3:
                        if record.Priority3:
                            premium_percentage4 = float(record.Priority3.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add4 = float(rec.AnalysisProfilePrice) * premium_percentage4
                            profile3_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add4
                            profile3_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add4 = service.LabService.Price * premium_percentage4
                            service_price = service.LabService.Price + charges_to_add4
                            service_discount3 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal3 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat3 += (service_price - (service_price * client_obj.M_Discount / 100)) * service.LabService.VAT / 100
                            service_total3 = service_subtotal3 + service_vat3

            for profile, profile_price in profile3_services_price.iteritems():
                service_price = profile_price
                service_discount3 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal3 += float(service_price) - float(discount)
                # compute VAT
                service_vat3 = (float(service_price) - float(discount)) * profile3_services_VAT[profile] / 100
                service_total3 += (float(service_price) - float(discount)) + service_vat3

                if service.LabService.id in service_ids_list_p5:
                    for rec in record.AnalysisProfile4:
                        if record.Priority4:
                            premium_percentage5 = float(record.Priority4.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add5 = float(rec.AnalysisProfilePrice) * premium_percentage5
                            profile4_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add5
                            profile4_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add5 = service.LabService.Price * premium_percentage5
                            service_price = service.LabService.Price + charges_to_add5
                            service_discount4 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal4 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat4 += (service_price - discount) * service.LabService.VAT / 100
                            service_total4 = service_subtotal4 + service_vat4

            for profile, profile_price in profile4_services_price.iteritems():
                service_price = profile_price
                service_discount4 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal4 += float(service_price) - float(discount)
                # compute VAT
                service_vat4 = (float(service_price) - float(discount)) * profile4_services_VAT[profile] / 100
                service_total4 += (float(service_price) - float(discount)) + service_vat4


                if service.LabService.id in service_ids_list_p6:
                    for rec in record.AnalysisProfile5:
                        if record.Priority5:
                            premium_percentage6 = float(record.Priority5.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add6 = float(rec.AnalysisProfilePrice) * premium_percentage6
                            profile5_services_price[rec.id] = float(rec.AnalysisProfilePrice) +charges_to_add6
                            profile5_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add6 = service.LabService.Price * premium_percentage6
                            service_price = service.LabService.Price +charges_to_add6
                            service_discount5 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal5 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat5 += (service_price - discount) * service.LabService.VAT / 100
                            service_total5 = service_subtotal5 + service_vat5

            for profile, profile_price in profile5_services_price.iteritems():
                service_price = profile_price
                service_discount5 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal5 += float(service_price) - float(discount)
                # compute VAT
                service_vat5 = (float(service_price) - float(discount)) * profile5_services_VAT[profile] / 100
                service_total5 += (float(service_price) - float(discount)) + service_vat5


                if service.LabService.id in service_ids_list_p7:
                    for rec in record.AnalysisProfile6:
                        if record.Priority6:
                            premium_percentage7 = float(record.Priority6.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add7 = float(rec.AnalysisProfilePrice) * premium_percentage7
                            profile6_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add7
                            profile6_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add7 = service.LabService.Price * premium_percentage7
                            service_price = service.LabService.Price + charges_to_add7
                            service_discount6 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal6 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat6 += (service_price - (service_price * client_obj.M_Discount / 100)) * service.LabService.VAT / 100
                            service_total6 = service_subtotal6 + service_vat6

            for profile, profile_price in profile6_services_price.iteritems():
                service_price = profile_price
                service_discount6 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal6 += float(service_price) - float(discount)
                # compute VAT
                service_vat6 = (float(service_price) - float(discount)) * profile6_services_VAT[profile] / 100
                service_total6 += (float(service_price) - float(discount)) + service_vat6


                if service.LabService.id in service_ids_list_p8:
                    for rec in record.AnalysisProfile7:
                        if record.Priority7:
                            premium_percentage8 = float(record.Priority7.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add8 = float(rec.AnalysisProfilePrice) * premium_percentage8
                            profile7_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add8
                            profile7_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add8 = service.LabService.Price * premium_percentage8
                            service_price = service.LabService.Price + charges_to_add8
                            service_discount7 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal7 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat7 += (service_price - discount) * service.LabService.VAT / 100
                            service_total7 = service_subtotal7 + service_vat7

            for profile, profile_price in profile7_services_price.iteritems():
                service_price = profile_price
                service_discount7 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal7 += float(service_price) - float(discount)
                # compute VAT
                service_vat7 = (float(service_price) - float(discount)) * profile7_services_VAT[profile] / 100
                service_total7 += (float(service_price) - float(discount)) + service_vat7


                if service.LabService.id in service_ids_list_p9:
                    for rec in record.AnalysisProfile8:
                        if record.Priority8:
                            premium_percentage9 = float(record.Priority8.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add9 = float(rec.AnalysisProfilePrice) * premium_percentage9
                            profile8_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add9
                            profile8_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add9 = service.LabService.Price * premium_percentage9
                            service_price = service.LabService.Price + charges_to_add9
                            service_discount8 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal8 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat8 += (service_price - discount) * service.LabService.VAT / 100
                            service_total8 = service_subtotal8 + service_vat8

            for profile, profile_price in profile8_services_price.iteritems():
                service_price = profile_price
                service_discount8 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal8 += float(service_price) - float(discount)
                # compute VAT
                service_vat8 = (float(service_price) - float(discount)) * profile8_services_VAT[profile] / 100
                service_total8 += (float(service_price) - float(discount)) + service_vat8


                if service.LabService.id in service_ids_list_p10:
                    for rec in record.AnalysisProfile9:
                        if record.Priority9:
                            premium_percentage10 = float(record.Priority9.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add10 = float(rec.AnalysisProfilePrice) * premium_percentage10
                            profile9_services_price[rec.id] = float(rec.AnalysisProfilePrice) + charges_to_add10
                            profile9_services_VAT[rec.id] = rec.AnalysisProfileVAT
                        else:
                            charges_to_add10 = service.LabService.Price * premium_percentage10
                            service_price = service.LabService.Price + charges_to_add10
                            service_discount9 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal9 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat9 += (service_price - (service_price * client_obj.M_Discount / 100)) * service.LabService.VAT / 100
                            service_total9 = service_subtotal9 + service_vat9

            for profile, profile_price in profile9_services_price.iteritems():
                service_price = profile_price
                service_discount9 = service_price * client_obj.M_Discount / 100
                discount = service_price * client_obj.M_Discount / 100
                service_subtotal9 += float(service_price) - float(discount)
                # compute VAT
                service_vat9 = (float(service_price) - float(discount)) * profile9_services_VAT[profile] / 100
                service_total9 += (float(service_price) - float(discount)) + service_vat9

                if service.LabService.id not in service_ids_list_p1 and \
                                service.LabService.id not in service_ids_list_p2 and \
                                service.LabService.id not in service_ids_list_p3 and \
                                service.LabService.id not in service_ids_list_p4 and \
                                service.LabService.id not in service_ids_list_p5 and \
                                service.LabService.id not in service_ids_list_p6 and \
                                service.LabService.id not in service_ids_list_p7 and \
                                service.LabService.id not in service_ids_list_p8 and \
                                service.LabService.id not in service_ids_list_p9 and \
                                service.LabService.id not in service_ids_list_p10:
                    service_price = float(service.LabService.Price)
                    discount = service_price * client_obj.M_Discount / 100
                    service_discount, service_subtotal, service_total, service_vat = self.calculate_lab_service_amount_for_ar(
                        discount, service, service_discount, service_price, service_subtotal, service_total,
                        service_vat,client_obj)
                    if record.Copy == '1' or record.AnalysisProfile1 and not record.AnalysisProfile2 and not record.AnalysisProfile3 and not \
                            record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not\
                            record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                    elif record.Copy == '2' or record.AnalysisProfile1 and record.AnalysisProfile2 and not record.AnalysisProfile3 and not \
                        record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                    elif record.Copy == '3' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and not \
                         record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                         record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                    elif record.Copy == '4' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                         record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                         record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                        service_discount4, service_subtotal4, service_total4, service_vat4 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount4, service_price, service_subtotal4, service_total4,
                            service_vat4,client_obj)

                    elif record.Copy == '5' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                         record.AnalysisProfile4 and record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                         record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                        service_discount4, service_subtotal4, service_total4, service_vat4 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount4, service_price, service_subtotal4, service_total4,
                            service_vat4,client_obj)

                        service_discount5, service_subtotal5, service_total5, service_vat5 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount5, service_price, service_subtotal5, service_total5,
                            service_vat5,client_obj)

                    elif record.Copy == '6' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                         record.AnalysisProfile4 and record.AnalysisProfile5 and  record.AnalysisProfile6 and not \
                         record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                        service_discount4, service_subtotal4, service_total4, service_vat4 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount4, service_price, service_subtotal4, service_total4,
                            service_vat4,client_obj)

                        service_discount5, service_subtotal5, service_total5, service_vat5 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount5, service_price, service_subtotal5, service_total5,
                            service_vat5,client_obj)

                        service_discount6, service_subtotal6, service_total6, service_vat6 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount6, service_price, service_subtotal6, service_total6,
                            service_vat6,client_obj)

                    elif record.Copy == '7' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                         record.AnalysisProfile4 and record.AnalysisProfile5 and  record.AnalysisProfile6 and \
                         record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                        service_discount4, service_subtotal4, service_total4, service_vat4 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount4, service_price, service_subtotal4, service_total4,
                            service_vat4,client_obj)

                        service_discount5, service_subtotal5, service_total5, service_vat5 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount5, service_price, service_subtotal5, service_total5,
                            service_vat5,client_obj)

                        service_discount6, service_subtotal6, service_total6, service_vat6 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount6, service_price, service_subtotal6, service_total6,
                            service_vat6,client_obj)

                        service_discount7, service_subtotal7, service_total7, service_vat7 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount7, service_price, service_subtotal7, service_total7,
                            service_vat7,client_obj)

                    elif record.Copy == '8' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                         record.AnalysisProfile4 and record.AnalysisProfile5 and  record.AnalysisProfile6 and \
                         record.AnalysisProfile7 and record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                        service_discount4, service_subtotal4, service_total4, service_vat4 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount4, service_price, service_subtotal4, service_total4,
                            service_vat4,client_obj)

                        service_discount5, service_subtotal5, service_total5, service_vat5 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount5, service_price, service_subtotal5, service_total5,
                            service_vat5,client_obj)

                        service_discount6, service_subtotal6, service_total6, service_vat6 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount6, service_price, service_subtotal6, service_total6,
                            service_vat6,client_obj)

                        service_discount7, service_subtotal7, service_total7, service_vat7 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount7, service_price, service_subtotal7, service_total7,
                            service_vat7,client_obj)

                        service_discount8, service_subtotal8, service_total8, service_vat8 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount8, service_price, service_subtotal8, service_total8,
                            service_vat8,client_obj)

                    elif record.Copy == '9' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                         record.AnalysisProfile4 and record.AnalysisProfile5 and  record.AnalysisProfile6 and \
                         record.AnalysisProfile7 and record.AnalysisProfile8 and record.AnalysisProfile9:
                        service_discount1, service_subtotal1, service_total1, service_vat1 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount1, service_price, service_subtotal1, service_total1,
                            service_vat1,client_obj)

                        service_discount2, service_subtotal2, service_total2, service_vat2 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount2, service_price, service_subtotal2, service_total2,
                            service_vat2,client_obj)

                        service_discount3, service_subtotal3, service_total3, service_vat3 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount3, service_price, service_subtotal3, service_total3,
                            service_vat3,client_obj)

                        service_discount4, service_subtotal4, service_total4, service_vat4 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount4, service_price, service_subtotal4, service_total4,
                            service_vat4,client_obj)

                        service_discount5, service_subtotal5, service_total5, service_vat5 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount5, service_price, service_subtotal5, service_total5,
                            service_vat5,client_obj)

                        service_discount6, service_subtotal6, service_total6, service_vat6 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount6, service_price, service_subtotal6, service_total6,
                            service_vat6,client_obj)

                        service_discount7, service_subtotal7, service_total7, service_vat7 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount7, service_price, service_subtotal7, service_total7,
                            service_vat7,client_obj)

                        service_discount8, service_subtotal8, service_total8, service_vat8 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount8, service_price, service_subtotal8, service_total8,
                            service_vat8,client_obj)

                        service_discount9, service_subtotal9, service_total9, service_vat9 = self.calculate_lab_service_amount_for_ar(
                            discount, service, service_discount9, service_price, service_subtotal9, service_total9,
                            service_vat9,client_obj)

            for FService in record.FieldService:
                if FService.Service.id in f_service_ids_list_p1:
                    for rec in record.AnalysisProfile:
                        if record.Priority:
                            premium_percentage1 = float(record.Priority.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add1 = float(rec.AnalysisProfilePrice) * premium_percentage1
                            service_price = float(rec.AnalysisProfilePrice) + charges_to_add1
                            service_discount = service_price * client_obj.M_Discount / 100
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal = float(service_price) - float(discount)
                            # compute VAT
                            service_vat = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT / 100
                            service_total = service_subtotal + service_vat
                        else:
                            charges_to_add1 = FService.Service.Price * premium_percentage1
                            service_price = FService.Service.Price + charges_to_add1
                            service_discount += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal += float(service_price) - float(discount)
                            # compute VAT
                            service_vat += (float(service_price) - float(discount)) * FService.Service.VAT / 100
                            service_total = service_subtotal + service_vat

                if FService.Service.id in f_service_ids_list_p2:
                    for rec in record.AnalysisProfile1:
                        if record.Priority1:
                            premium_percentage2 = float(record.Priority1.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add2 = rec.AnalysisProfilePrice * premium_percentage2
                            service_price = rec.AnalysisProfilePrice + charges_to_add2
                            service_discount1 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal1 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat1 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT / 100
                            service_total1 = service_subtotal1 + service_vat1
                        else:
                            charges_to_add2 = FService.Service.Price * premium_percentage2
                            service_price = FService.Service.Price + charges_to_add2
                            service_discount1 += service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal1 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat1 += (float(service_price) - float(discount)) * FService.Service.VAT / 100
                            service_total1 = service_subtotal1 + service_vat1

                if FService.Service.id in f_service_ids_list_p3:
                    for rec in record.AnalysisProfile2:
                        if record.Priority2:
                            premium_percentage3 = float(record.Priority2.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add3 = rec.AnalysisProfilePrice * premium_percentage3
                            service_price = rec.AnalysisProfilePrice + charges_to_add3
                            service_discount2 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal2 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat2 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT / 100
                            service_total2 = service_subtotal2 + service_vat2
                        else:
                            charges_to_add3 = FService.Service.Price * premium_percentage3
                            service_price = FService.Service.Price + charges_to_add3
                            service_discount2 += service_price * client_obj.M_Discount / 100
                            # compute sf_ubtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal2 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat2 += (float(service_price) - float(discount)) * FService.Service.VAT / 100
                            service_total2 = service_subtotal2 + service_vat2

                if FService.Service.id in f_service_ids_list_p4:
                    for rec in record.AnalysisProfile3:
                        if record.Priority3:
                            premium_percentage4 = float(record.Priority3.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add4 = rec.AnalysisProfilePrice * premium_percentage4
                            service_price = rec.AnalysisProfilePrice + charges_to_add4
                            service_discount3 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal3 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat3 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total3 = service_subtotal3 + service_vat3
                        else:
                            charges_to_add4 = FService.Service.Price * premium_percentage4
                            service_price = FService.Service.Price + charges_to_add4
                            service_discount3 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal3 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat3 += service_subtotal3 * FService.Service.VAT / 100
                            service_total3 = service_subtotal3 + service_vat3

                if FService.Service.id in f_service_ids_list_p5:
                    for rec in record.AnalysisProfile4:
                        if record.Priority4:
                            premium_percentage5 = float(record.Priority4.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add5 = rec.AnalysisProfilePrice * premium_percentage5
                            service_price = rec.AnalysisProfilePrice + charges_to_add5
                            service_discount4 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal4 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat4 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total4 = service_subtotal4 + service_vat4
                        else:
                            charges_to_add5 = FService.Service.Price * premium_percentage5
                            service_price = FService.Service.Price + charges_to_add5
                            service_discount4 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal4 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                            service_total4 = service_subtotal4 + service_vat4

                if FService.Service.id in f_service_ids_list_p6:
                    for rec in record.AnalysisProfile5:
                        if record.Priority5:
                            premium_percentage6 = float(record.Priority5.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add6 = rec.AnalysisProfilePrice * premium_percentage6
                            service_price = rec.AnalysisProfilePrice + charges_to_add6
                            service_discount5 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal5 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat5 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total5 = service_subtotal5 + service_vat5
                        else:
                            charges_to_add6 = FService.Service.Price * premium_percentage6
                            service_price = FService.Service.Price + charges_to_add6
                            service_discount5 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal5 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat5 += service_subtotal5 * FService.Service.VAT / 100
                            service_total5 = service_subtotal5 + service_vat5

                if FService.Service.id in f_service_ids_list_p7:
                    for rec in record.AnalysisProfile6:
                        if record.Priority6:
                            premium_percentage7 = float(record.Priority6.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add7 = rec.AnalysisProfilePrice * premium_percentage7
                            service_price = rec.AnalysisProfilePrice + charges_to_add7
                            service_discount6 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal6 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat6 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total6 = service_subtotal6 + service_vat6
                        else:
                            charges_to_add7 = FService.Service.Price * premium_percentage7
                            service_price = FService.Service.Price +charges_to_add7
                            service_discount6 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal6 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat6 += service_subtotal6 * FService.Service.VAT / 100
                            service_total6 = service_subtotal6 + service_vat6

                if FService.Service.id in f_service_ids_list_p8:
                    for rec in record.AnalysisProfile7:
                        if record.Priority7:
                            premium_percentage8 = float(record.Priority7.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add8 = rec.AnalysisProfilePrice * premium_percentage8
                            service_price = rec.AnalysisProfilePrice + charges_to_add8
                            service_discount7 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal7 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat7 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total7 = service_subtotal7 + service_vat7
                        else:
                            charges_to_add8 = FService.Service.Price * premium_percentage8
                            service_price = FService.Service.Price + charges_to_add8
                            service_discount7 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal7 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat7 += service_subtotal7 * FService.Service.VAT / 100
                            service_total7 = service_subtotal7 + service_vat7

                if FService.Service.id in f_service_ids_list_p9:
                    for rec in record.AnalysisProfile8:
                        if record.Priority8:
                            premium_percentage9 = float(record.Priority8.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add9 = rec.AnalysisProfilePrice * premium_percentage9
                            service_price = rec.AnalysisProfilePrice + charges_to_add9
                            service_discount8 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal8 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat8 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total8 = service_subtotal8 + service_vat8
                        else:
                            charges_to_add9 = FService.Service.Price * premium_percentage9
                            service_price = FService.Service.Price + charges_to_add9
                            service_discount8 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal8 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat8 += service_subtotal8 * FService.Service.VAT / 100
                            service_total8 = service_subtotal8 + service_vat8

                if FService.Service.id in f_service_ids_list_p10:
                    for rec in record.AnalysisProfile9:
                        if record.Priority9:
                            premium_percentage10 = float(record.Priority9.Premium)/100
                        if rec.UseAnalysisProfilePrice:
                            charges_to_add10 = rec.AnalysisProfilePrice * premium_percentage10
                            service_price = rec.AnalysisProfilePrice + charges_to_add10
                            service_discount9 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal9 = float(service_price) - float(discount)
                            # compute VAT
                            service_vat9 = (float(service_price) - float(discount)) * rec.AnalysisProfileVAT /100
                            service_total9 = service_subtotal9 + service_vat9
                        else:
                            charges_to_add10 = FService.Service.Price * premium_percentage10
                            service_price = FService.Service.Price + charges_to_add10
                            service_discount9 = service_price * client_obj.M_Discount / 100
                            # compute subtotal
                            discount = service_price * client_obj.M_Discount / 100
                            service_subtotal9 += float(service_price) - float(discount)
                            # compute VAT
                            service_vat9 += service_subtotal9 * FService.Service.VAT / 100
                            service_total9 = service_subtotal9 + service_vat9

                if FService.Service.id not in f_service_ids_list_p1 and \
                                FService.Service.id not in f_service_ids_list_p2 and \
                                FService.Service.id not in f_service_ids_list_p3 and \
                                FService.Service.id not in f_service_ids_list_p4 and \
                                FService.Service.id not in f_service_ids_list_p5 and \
                                FService.Service.id not in f_service_ids_list_p6 and \
                                FService.Service.id not in f_service_ids_list_p7 and \
                                FService.Service.id not in f_service_ids_list_p8 and \
                                FService.Service.id not in f_service_ids_list_p9 and \
                                FService.Service.id not in f_service_ids_list_p10:
                    service_price = float(FService.Service.Price)
                    service_discount += service_price * client_obj.M_Discount / 100
                    # compute subtotal
                    discount = service_price * client_obj.M_Discount / 100
                    service_subtotal += float(service_price) - float(discount)
                    # compute VAT
                    service_vat += service_subtotal * FService.Service.VAT / 100
                    service_total = service_subtotal + service_vat

                    if record.Copy == '1' or record.AnalysisProfile1 and not record.AnalysisProfile2 and not record.AnalysisProfile3 and not \
                        record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        # compute subtotal
                        # discount = service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        # compute VAT
                        service_vat1 += service_subtotal1 * FService.Service.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1

                    elif record.Copy == '2' or record.AnalysisProfile1 and record.AnalysisProfile2 and not record.AnalysisProfile3 and not \
                        record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
                        service_discount1 += service_price * client_obj.M_Discount / 100
                        service_subtotal1 += float(service_price) - float(discount)
                        service_vat1 += service_subtotal1 * FService.Service.VAT / 100
                        service_total1 = service_subtotal1 + service_vat1

                        service_discount2 += service_price * client_obj.M_Discount / 100
                        service_subtotal2 += float(service_price) - float(discount)
                        service_vat2 += service_subtotal2 * FService.Service.VAT / 100
                        service_total2 = service_subtotal2 + service_vat2

                    elif record.Copy == '3' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and not\
                        record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
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

                    elif record.Copy == '4' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                        record.AnalysisProfile4 and not record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
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

                        service_discount4 += service_price * client_obj.M_Discount / 100
                        service_subtotal4 += float(service_price) - float(discount)
                        service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                        service_total4 = service_subtotal4 + service_vat4

                    elif record.Copy == '5' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                        record.AnalysisProfile4 and record.AnalysisProfile5 and not record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
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

                        service_discount4 += service_price * client_obj.M_Discount / 100
                        service_subtotal4 += float(service_price) - float(discount)
                        service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                        service_total4 = service_subtotal4 + service_vat4

                        service_discount5 += service_price * client_obj.M_Discount / 100
                        service_subtotal5 += float(service_price) - float(discount)
                        service_vat5 += service_subtotal5 * FService.Service.VAT / 100
                        service_total5 = service_subtotal5 + service_vat5

                    elif record.Copy == '6' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                        record.AnalysisProfile4 and record.AnalysisProfile5 and record.AnalysisProfile6 and not \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
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

                        service_discount4 += service_price * client_obj.M_Discount / 100
                        service_subtotal4 += float(service_price) - float(discount)
                        service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                        service_total4 = service_subtotal4 + service_vat4

                        service_discount5 += service_price * client_obj.M_Discount / 100
                        service_subtotal5 += float(service_price) - float(discount)
                        service_vat5 += service_subtotal5 * FService.Service.VAT / 100
                        service_total5 = service_subtotal5 + service_vat5

                        service_discount6 += service_price * client_obj.M_Discount / 100
                        service_subtotal6 += float(service_price) - float(discount)
                        service_vat6 += service_subtotal6 * FService.Service.VAT / 100
                        service_total6 = service_subtotal6 + service_vat6

                    elif record.Copy == '7' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                        record.AnalysisProfile4 and record.AnalysisProfile5 and record.AnalysisProfile6 and \
                        record.AnalysisProfile7 and not record.AnalysisProfile8 and not record.AnalysisProfile9:
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

                        service_discount4 += service_price * client_obj.M_Discount / 100
                        service_subtotal4 += float(service_price) - float(discount)
                        service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                        service_total4 = service_subtotal4 + service_vat4

                        service_discount5 += service_price * client_obj.M_Discount / 100
                        service_subtotal5 += float(service_price) - float(discount)
                        service_vat5 += service_subtotal5 * FService.Service.VAT / 100
                        service_total5 = service_subtotal5 + service_vat5

                        service_discount6 += service_price * client_obj.M_Discount / 100
                        service_subtotal6 += float(service_price) - float(discount)
                        service_vat6 += service_subtotal6 * FService.Service.VAT / 100
                        service_total6 = service_subtotal6 + service_vat6

                        service_discount7 += service_price * client_obj.M_Discount / 100
                        service_subtotal7 += float(service_price) - float(discount)
                        service_vat7 += service_subtotal7 * FService.Service.VAT / 100
                        service_total7 = service_subtotal7 + service_vat7

                    elif record.Copy == '8' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                        record.AnalysisProfile4 and record.AnalysisProfile5 and record.AnalysisProfile6 and \
                        record.AnalysisProfile7 and record.AnalysisProfile8 and not record.AnalysisProfile9:
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

                        service_discount4 += service_price * client_obj.M_Discount / 100
                        service_subtotal4 += float(service_price) - float(discount)
                        service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                        service_total4 = service_subtotal4 + service_vat4

                        service_discount5 += service_price * client_obj.M_Discount / 100
                        service_subtotal5 += float(service_price) - float(discount)
                        service_vat5 += service_subtotal5 * FService.Service.VAT / 100
                        service_total5 = service_subtotal5 + service_vat5

                        service_discount6 += service_price * client_obj.M_Discount / 100
                        service_subtotal6 += float(service_price) - float(discount)
                        service_vat6 += service_subtotal6 * FService.Service.VAT / 100
                        service_total6 = service_subtotal6 + service_vat6

                        service_discount7 += service_price * client_obj.M_Discount / 100
                        service_subtotal7 += float(service_price) - float(discount)
                        service_vat7 += service_subtotal7 * FService.Service.VAT / 100
                        service_total7 = service_subtotal7 + service_vat7

                        service_discount8 += service_price * client_obj.M_Discount / 100
                        service_subtotal8 += float(service_price) - float(discount)
                        service_vat8 += service_subtotal8 * FService.Service.VAT / 100
                        service_total8 = service_subtotal8 + service_vat8

                    elif record.Copy == '8' or record.AnalysisProfile1 and record.AnalysisProfile2 and record.AnalysisProfile3 and \
                        record.AnalysisProfile4 and record.AnalysisProfile5 and record.AnalysisProfile6 and \
                        record.AnalysisProfile7 and record.AnalysisProfile8 and record.AnalysisProfile9:
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

                        service_discount4 += service_price * client_obj.M_Discount / 100
                        service_subtotal4 += float(service_price) - float(discount)
                        service_vat4 += service_subtotal4 * FService.Service.VAT / 100
                        service_total4 = service_subtotal4 + service_vat4

                        service_discount5 += service_price * client_obj.M_Discount / 100
                        service_subtotal5 += float(service_price) - float(discount)
                        service_vat5 += service_subtotal5 * FService.Service.VAT / 100
                        service_total5 = service_subtotal5 + service_vat5

                        service_discount6 += service_price * client_obj.M_Discount / 100
                        service_subtotal6 += float(service_price) - float(discount)
                        service_vat6 += service_subtotal6 * FService.Service.VAT / 100
                        service_total6 = service_subtotal6 + service_vat6

                        service_discount7 += service_price * client_obj.M_Discount / 100
                        service_subtotal7 += float(service_price) - float(discount)
                        service_vat7 += service_subtotal7 * FService.Service.VAT / 100
                        service_total7 = service_subtotal7 + service_vat7

                        service_discount8 += service_price * client_obj.M_Discount / 100
                        service_subtotal8 += float(service_price) - float(discount)
                        service_vat8 += service_subtotal8 * FService.Service.VAT / 100
                        service_total8 = service_subtotal8 + service_vat8

                        service_discount9 += service_price * client_obj.M_Discount / 100
                        service_subtotal9 += float(service_price) - float(discount)
                        service_vat9 += service_subtotal9 * FService.Service.VAT / 100
                        service_total9 = service_subtotal9 + service_vat9

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

            record.Discount4 = service_discount4
            record.Subtotal4 = service_subtotal4
            record.VAT4 = service_vat4
            record.Total4 = service_total4

            record.Discount5 = service_discount5
            record.Subtotal5 = service_subtotal5
            record.VAT5 = service_vat5
            record.Total5 = service_total5

            record.Discount6 = service_discount6
            record.Subtotal6 = service_subtotal6
            record.VAT6 = service_vat6
            record.Total6 = service_total6

            record.Discount7 = service_discount7
            record.Subtotal7 = service_subtotal7
            record.VAT7 = service_vat7
            record.Total7 = service_total7

            record.Discount8 = service_discount8
            record.Subtotal8 = service_subtotal8
            record.VAT8 = service_vat8
            record.Total8 = service_total8

            record.Discount9 = service_discount9
            record.Subtotal9 = service_subtotal9
            record.VAT9 = service_vat9
            record.Total9 = service_total9

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
                if items.Category.id not in ar_cate_ids_list:
                    ar_cate_ids_list.append(items.Category.id)
            for cate_id in ar_cate_ids_list:
                analysis_dict = {}
                if not ar_object.AnalysisProfile:
                    analysis_dict.update({
                        'category':cate_id,
                        'client': ar_object.Client.id,
                        'order':ar_object.LotID,
                        'priority':ar_object.Priority.id,
                        'due_date':ar_object.DateDue,
                        'received_date':datetime.datetime.now(),
                        'analysis_profile': None,
                        'sample_type': ar_object.SampleType.id,
                        'add_analysis_id':ar_object.id
                        })
                    data_list.append([0, 0, analysis_dict])
                else:
                    for profile in ar_object.AnalysisProfile:
                        for service in profile.Service:
                            if service.Category.id == cate_id:
                                 analysis_dict = {
                                    'category':cate_id,
                                    'client': ar_object.Client.id,
                                    'order':ar_object.LotID,
                                    'priority':ar_object.Priority.id,
                                    'due_date':ar_object.DateDue,
                                    'received_date':datetime.datetime.now(),
                                    'analysis_profile': profile.id,
                                    'sample_type': ar_object.SampleType.id,
                                    'add_analysis_id':ar_object.id
                                    }
                                 data_list.append([0, 0, analysis_dict])
                                 break
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

    def workflow_script_to_be_sampled(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_sampled', 'DateDue':datetime.datetime.now()
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

    @api.multi
    def ar_publish(self):
        if self.Client.payment_not_current:
            view_id = self.env['ir.ui.view'].search([('name', '=', 'Payment Not Current Dialog Box')])
            context = self.env.context.copy()
            context.update({'do_action': 'publish'})
            return {
                'name': _('Payment Not Current'),
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'olims.message_dialog_box',
                'view_id': [view_id.id],
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': context,
            }
        else:
            self.signal_workflow('publish')

        return True

    def workflow_script_cancel(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids,{
            'state': 'cancelled'
        },context)
        return True

    @api.multi
    @api.onchange("AnalysisProfile","AnalysisProfile1","AnalysisProfile2","AnalysisProfile3",
            "AnalysisProfile4","AnalysisProfile5","AnalysisProfile6","AnalysisProfile7",
            "AnalysisProfile8","AnalysisProfile9")
    def _add_values_in_analyses(self):
        service_ids_list = []
        profile_ids = []
        
        for record in self:
            if record.state != "sample_registered":
                record.Field_Manage_Result = None
                record.Lab_Manage_Result = None
                record.Analyses = None
                for rec in record.AnalysisProfile:
                    for services in rec.Service:
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
            for rec in record.AnalysisProfile:
                for service in rec.Service:
                    if  service.Services.PointOfCapture == 'lab':
                        l_service = {'LabService':service.Services.id,
                            'Category':service.Services.category.id}
                        if service.Services.id not in service_ids_list:
                            record.LabService += record.LabService.new(l_service)
                    if service.Services.PointOfCapture == 'field':
                        f_service = {'Service':service.Services.id,
                        'Category':service.Services.category.id}
                        record.FieldService += record.FieldService.new(f_service)
                    service_ids_list.append(service.Services.id)

            for rec in record.AnalysisProfile1:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile2:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile3:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile4:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile5:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile6:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile7:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile8:
                for service in rec.Service:
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

            for rec in record.AnalysisProfile9:
                for service in rec.Service:
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



    def bulk_change_states_pre(self, state, cr, uid, ids, context=None):
        previous_state = ""
        data = {}
        if state == "sample_due":
            previous_state = "to_be_sampled"
        elif state == "sample_received":
            previous_state = "sample_due"
        requests = self.browse(cr,uid,sorted(ids))
        sample_ids = []
        for request in requests:
            if request.state == 'pre_enter':
                if state == "to_be_sampled":
                    last_id = self.compute_analysis_request_number(cr, uid, ids)
                    new_id = int(last_id)+1
                    request_id = 'R-0' + str(new_id)
                    data = {"RequestID":request_id,'ar_counter':new_id}
                    sample_ids.append(request.Sample_id.id)
                    data["state"] = state
                    res = self.browse(cr,uid,request.id).write(data)
                elif request.state != previous_state:
                    ids.remove(request.id)
                else:
                    sample_ids.append(request.Sample_id.id)
            else:
                raise osv.except_osv(_('error'),
                                     _('AR Number have already been assigned !'))

        self.browse(cr,uid,ids).signal_workflow(state)
        res = self.pool.get("olims.sample").browse(cr,uid,sample_ids).write({"state":state})
        if state != "to_be_sampled":
            data["state"] = state
            res = self.browse(cr,uid,request.id).write(data)
        return True

    @api.model
    def download_zip(self):
        ir_actions_report = self.env['ir.actions.report.xml'].search([('name', '=', 'Certificate of Analysis (COA)')])
        if ir_actions_report:
            report_service = 'report.' + ir_actions_report.report_name
            service = netsvc.LocalService(report_service)
            ids = self.env.context.get('active_ids')
            ar_object = self.env['olims.analysis_request'].search([('id','in',ids)])
            imz = InMemoryZip()
            index = 0
            for id in ids:
                result, format = openerp.report.render_report(self.env.cr, self.env.uid, [id],
                                                          ir_actions_report.report_name, {'model': self._name},
                                                          context=self.env.context)
                if ar_object[index].LotID and ar_object[index].ClientReference:
                    title = ar_object[index].LotID + '-'+ ar_object[index].ClientReference
                else :
                    title = ar_object[index].RequestID
                title = title.replace('/','-')
                imz.append(str(title) + '.pdf', result)
                index +=1
        compressed_file = imz.read()

        attachment_obj = self.env['ir.attachment']

        filename = str(datetime.date.today()) +'-AR.zip'
        new_attachemet_obj = attachment_obj.create(
                                                   {
                                                       'name': filename,
                                                       'datas': base64.b64encode(compressed_file),
                                                       'datas_fname': filename,
                                                       'type': 'binary'
                                                   })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/' + str(new_attachemet_obj.id) + '?download=true',
        }




    def bulk_change_states(self, state, cr, uid, ids, context=None):
        previous_state = ""
        if state == "sample_due":
            previous_state = "to_be_sampled"
        elif state == "sample_received":
            previous_state = "sample_due"
        elif state == "to_be_sampled":
            previous_state = "pre_enter"
        requests = self.browse(cr,uid,ids)
        sample_ids = []
        for request in requests:
            if request.state != previous_state:
                ids.remove(request.id)
            else:
                sample_ids.append(request.Sample_id.id)
                
        self.browse(cr,uid,ids).signal_workflow(state)
        res = self.pool.get("olims.sample").browse(cr,uid,sample_ids).write({"state":state})
        return True

    def bulk_verify_request(self,cr,uid,ids,context=None, ids_to_verify = None):
        requests = self.pool.get('olims.analysis_request').browse(cr,uid,ids,context)
        if ids_to_verify == None:
            if requests.Client.payment_not_current:
                view_id = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'Payment Not Current Dialog Box')], \
                                                             context=context)
                context = context.copy()
                context.update({'do_action' : 'verify'})
                return {
                    'name': _('Payment Not Current'),
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'olims.message_dialog_box',
                    'view_id': view_id[0],
                    'target': 'new',
                    'type': 'ir.actions.act_window',
                    'context': context,
                }
        else:
            requests = self.pool.get('olims.analysis_request').browse(cr, uid, ids_to_verify, context)


        for request in requests:
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
            self.Contact2 = self.Contact3 = self.Contact4 = self.Contact5 = self.Contact6 = self.Contact7 = self.Contact8 = self.Contact9 = None
        elif self.Copy == '2':
            self.Contact1 = self.Contact2 = self.Contact
            self.Contact3 = self.Contact4 = self.Contact5 = self.Contact6 = self.Contact7 = self.Contact8 = self.Contact9 = None
        elif self.Copy == '3':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact
            self.Contact4 = self.Contact5 = self.Contact6 = self.Contact7 = self.Contact8 = self.Contact9 = None
        elif self.Copy == '4':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact4 = self.Contact
            self.Contact5 = self.Contact6 = self.Contact7 = self.Contact8 = self.Contact9 = None
        elif self.Copy == '5':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact4 = self.Contact5 = self.Contact
            self.Contact6 = self.Contact7 = self.Contact8 = self.Contact9 = None
        elif self.Copy == '6':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact4 = self.Contact5 = self.Contact6 = self.Contact
            self.Contact7 = self.Contact8 = self.Contact9 = None
        elif self.Copy == '7':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact4 = self.Contact5 = self.Contact6 = self.Contact7 = self.Contact
            self.Contact8 = self.Contact9 = None
        elif self.Copy == '8':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact4 = self.Contact5 = self.Contact6 = self.Contact7 = self.Contact8 = self.Contact
            self.Contact9 = None
        elif self.Copy == '9':
            self.Contact1 = self.Contact2 = self.Contact3 = self.Contact4 = self.Contact5 = self.Contact6 = self.Contact7 = self.Contact8 = self.Contact9 = self.Contact
        else:
            pass

    @api.onchange('CopyCCContact')
    def copy_cccontact(self):
        if self.Copy == '1':
            self.CCContact1 = self.CCContact
            self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '2':
            self.CCContact1 = self.CCContact2 = self.CCContact
            self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '3':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact
            self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '4':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact
            self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '5':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact
            self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '6':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact
            self.CCContact7 = self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '7':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact
            self.CCContact8 = self.CCContact9 = None
        elif self.Copy == '8':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact
            self.CCContact9 = None
        elif self.Copy == '9':
            self.CCContact1 = self.CCContact2 = self.CCContact3 = self.CCContact4 = self.CCContact5 = self.CCContact6 = self.CCContact7 = self.CCContact8 = self.CCContact9 = self.CCContact
        else:
            pass
    @api.onchange('CopyEmail')
    def copy_email(self):
        if self.Copy == '1':
            self.CCEmails1 = self.CCEmails
            self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '2':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails
            self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '3':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails
            self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '4':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails
            self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '5':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails
            self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '6':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails
            self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '7':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails
            self.CCEmails8 = self.CCEmails9 = None
        elif self.Copy == '8':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails
            self.CCEmails9 = None
        elif self.Copy == '9':
            self.CCEmails1 = self.CCEmails2 = self.CCEmails3 = self.CCEmails4 = self.CCEmails5 = self.CCEmails6 = self.CCEmails7 = self.CCEmails8 = self.CCEmails9 = self.CCEmails
        else:
            pass

    @api.onchange('Copysample')
    def copy_sample(self):
        if self.Copy == '1':
            self.Sample_id1 = self.Sample_id
            self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '2':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id
            self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '3':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id
            self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '4':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id
            self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '5':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id
            self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '6':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id
            self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '7':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id
            self.Sample_id8 = self.Sample_id9 = None
        elif self.Copy == '8':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id
            self.Sample_id9 = None
        elif self.Copy == '9':
            self.Sample_id1 = self.Sample_id2 = self.Sample_id3 = self.Sample_id4 = self.Sample_id5 = self.Sample_id6 = self.Sample_id7 = self.Sample_id8 = self.Sample_id9 = self.Sample_id
        else:
            pass


    @api.onchange('Copysubgroup')
    def copy_subgroup(self):
        if self.Copy == '1':
            self.SubGroup1 = self.SubGroup
            self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '2':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup
            self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '3':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup
            self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '4':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup
            self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '5':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup
            self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '6':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup
            self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '7':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup
            self.SubGroup8 = self.SubGroup9 = None
        elif self.Copy == '8':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup
            self.SubGroup9 = None
        elif self.Copy == '9':
            self.SubGroup1 = self.SubGroup2 = self.SubGroup3 = self.SubGroup4 = self.SubGroup5 = self.SubGroup6 = self.SubGroup7 = self.SubGroup8 = self.SubGroup9 = self.SubGroup
        else:
            pass

    @api.onchange('Copytemplate')
    def copy_template(self):
        if self.Copy == '1':
            self.Template1 = self.Template
            self.Template2 = self.Template3 = self.Template4 = self.Template5 = self.Template6 = self.Template7 = self.Template8 = self.Template9 = None
        elif self.Copy == '2':
            self.Template1 = self.Template2 = self.Template
            self.Template3 = self.Template4 = self.Template5 = self.Template6 = self.Template7 = self.Template8 = self.Template9 = None
        elif self.Copy == '3':
            self.Template1 = self.Template2 = self.Template3 = self.Template
            self.Template4 = self.Template5 = self.Template6 = self.Template7 = self.Template8 = self.Template9 = None
        elif self.Copy == '4':
            self.Template1 = self.Template2 = self.Template3 = self.Template4 = self.Template
            self.Template5 = self.Template6 = self.Template7 = self.Template8 = self.Template9 = None
        elif self.Copy == '5':
            self.Template1 = self.Template2 = self.Template3 = self.Template4 = self.Template5 = self.Template
            self.Template6 = self.Template7 = self.Template8 = self.Template9 = None
        elif self.Copy == '6':
            self.Template1 = self.Template2 = self.Template3 = self.Template4 = self.Template5 = self.Template6 = self.Template
            self.Template7 = self.Template8 = self.Template9 = None
        elif self.Copy == '7':
            self.Template1 = self.Template2 = self.Template3 = self.Template4 = self.Template5 = self.Template6 = self.Template7 = self.Template
            self.Template8 = self.Template9 = None
        elif self.Copy == '8':
            self.Template1 = self.Template2 = self.Template3 = self.Template4 = self.Template5 = self.Template6 = self.Template7 = self.Template8 = self.Template
            self.Template9 = None
        elif self.Copy == '9':
            self.Template1 = self.Template2 = self.Template3 = self.Template4 = self.Template5 = self.Template6 = self.Template7 = self.Template8 = self.Template9 = self.Template
        else:
            pass

    @api.onchange('Copyprofile')
    def copy_profile(self):
        if self.Copy == '1':
            self.AnalysisProfile1 = self.AnalysisProfile
            self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '2':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile
            self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '3':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile
            self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '4':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile
            self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '5':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile
            self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '6':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile
            self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '7':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile
            self.AnalysisProfile8 = self.AnalysisProfile9 = None
        elif self.Copy == '8':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile
            self.AnalysisProfile9 = None
        elif self.Copy == '9':
            self.AnalysisProfile1 = self.AnalysisProfile2 = self.AnalysisProfile3 = self.AnalysisProfile4 = self.AnalysisProfile5 = self.AnalysisProfile6 = self.AnalysisProfile7 = self.AnalysisProfile8 = self.AnalysisProfile9 = self.AnalysisProfile
        else:
            pass

    @api.onchange('Copysmaplingdate')
    def copy_sampledate(self):
        if self.Copy == '1':
            self.SamplingDate1 = self.SamplingDate
            self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '2':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate
            self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '3':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate
            self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '4':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate
            self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '5':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate
            self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '6':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate
            self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '7':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate
            self.SamplingDate8 = self.SamplingDate9 = None
        elif self.Copy == '8':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate
            self.SamplingDate9 = None
        elif self.Copy == '9':
            self.SamplingDate1 = self.SamplingDate2 = self.SamplingDate3 = self.SamplingDate4 = self.SamplingDate5 = self.SamplingDate6 = self.SamplingDate7 = self.SamplingDate8 = self.SamplingDate9 = self.SamplingDate
        else:
            pass

    @api.onchange('Copysampler')
    def copy_sampler(self):
        if self.Copy == '1':
            self.Sampler1 = self.Sampler
            self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '2':
            self.Sampler1 = self.Sampler2 = self.Sampler
            self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '3':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler
            self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '4':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler
            self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '5':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler
            self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '6':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler
            self.Sampler7 = self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '7':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler
            self.Sampler8 = self.Sampler9 = None
        elif self.Copy == '8':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler
            self.Sampler9 = None
        elif self.Copy == '9':
            self.Sampler1 = self.Sampler2 = self.Sampler3 = self.Sampler4 = self.Sampler5 = self.Sampler6 = self.Sampler7 = self.Sampler8 = self.Sampler9 = self.Sampler
        else:
            pass

    @api.onchange('Copysampletype')
    def copy_sample_type(self):
        if self.Copy == '1':
            self.SampleType1 = self.SampleType
            self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '2':
            self.SampleType1 = self.SampleType2 = self.SampleType
            self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '3':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType
            self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '4':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType
            self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '5':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType
            self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '6':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType
            self.SampleType7 = self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '7':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType
            self.SampleType8 = self.SampleType9 = None
        elif self.Copy == '8':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType
            self.SampleType9 = None
        elif self.Copy == '9':
            self.SampleType1 = self.SampleType2 = self.SampleType3 = self.SampleType4 = self.SampleType5 = self.SampleType6 = self.SampleType7 = self.SampleType8 = self.SampleType9 = self.SampleType
        else:
            pass

    @api.onchange('Copyspecification')
    def copy_specification(self):
        if self.Copy == '1':
            self.Specification1 = self.Specification
            self.Specification2 = self.Specification3 = self.Specification4 = self.Specification5 = self.Specification6 = self.Specification7 = self.Specification8 = self.Specification9 = None
        elif self.Copy == '2':
            self.Specification1 = self.Specification2 = self.Specification
            self.Specification3 = self.Specification4 = self.Specification5 = self.Specification6 = self.Specification7 = self.Specification8 = self.Specification9 = None
        elif self.Copy == '3':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification
            self.Specification4 = self.Specification5 = self.Specification6 = self.Specification7 = self.Specification8 = self.Specification9 = None
        elif self.Copy == '4':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification4 = self.Specification
            self.Specification5 = self.Specification6 = self.Specification7 = self.Specification8 = self.Specification9 = None
        elif self.Copy == '5':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification4 = self.Specification5 = self.Specification
            self.Specification6 = self.Specification7 = self.Specification8 = self.Specification9 = None
        elif self.Copy == '6':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification4 = self.Specification5 = self.Specification6 = self.Specification
            self.Specification7 = self.Specification8 = self.Specification9 = None
        elif self.Copy == '7':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification4 = self.Specification5 = self.Specification6 = self.Specification7 = self.Specification
            self.Specification8 = self.Specification9 = None
        elif self.Copy == '8':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification4 = self.Specification5 = self.Specification6 = self.Specification7 = self.Specification8 = self.Specification
            self.Specification9 = None
        elif self.Copy == '9':
            self.Specification1 = self.Specification2 = self.Specification3 = self.Specification4 = self.Specification5 = self.Specification6 = self.Specification7 = self.Specification8 = self.Specification9 = self.Specification
        else:
            pass


    @api.onchange('CopyClientReference')
    def copy_client_reference(self):
        if self.Copy == '1':
            self.ClientReference1 = self.ClientReference
            self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '2':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference
            self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '3':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference
            self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '4':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference
            self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '5':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference
            self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '6':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference
            self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '7':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference
            self.ClientReference8 = self.ClientReference9 = None
        elif self.Copy == '8':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference
            self.ClientReference9 = None
        elif self.Copy == '9':
            self.ClientReference1 = self.ClientReference2 = self.ClientReference3 = self.ClientReference4 = self.ClientReference5 = self.ClientReference6 = self.ClientReference7 = self.ClientReference8 = self.ClientReference9 = self.ClientReference
        else:
            pass

    @api.onchange('CopySampleCondition')
    def copy_sample_condition(self):
        if self.Copy == '1':
            self.SampleCondition1 = self.SampleCondition
            self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '2':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition
            self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '3':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition
            self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '4':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition
            self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '5':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition
            self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '6':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition
            self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '7':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition
            self.SampleCondition8 = self.SampleCondition9 = None
        elif self.Copy == '8':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition
            self.SampleCondition9 = None
        elif self.Copy == '9':
            self.SampleCondition1 = self.SampleCondition2 = self.SampleCondition3 = self.SampleCondition4 = self.SampleCondition5 = self.SampleCondition6 = self.SampleCondition7 = self.SampleCondition8 = self.SampleCondition9 = self.SampleCondition
        else:
            pass

    @api.onchange('CopyAdHoc')
    def copy_adhoc(self):
        if self.Copy == '1':
            self.AdHoc1 = self.AdHoc
            self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '2':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc
            self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '3':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc
            self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '4':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc
            self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '5':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc
            self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '6':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc
            self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '7':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc
            self.AdHoc8 = self.AdHoc9 = None
        elif self.Copy == '8':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc
            self.AdHoc9 = None
        elif self.Copy == '9':
            self.AdHoc1 = self.AdHoc2 = self.AdHoc3 = self.AdHoc4 = self.AdHoc5 = self.AdHoc6 = self.AdHoc7 = self.AdHoc8 = self.AdHoc9 = self.AdHoc
        else:
            pass

    @api.onchange('CopyComposite')
    def copy_composite(self):
        if self.Copy == '1':
            self.Composite1 = self.Composite
            self.Composite2 = self.Composite3 = self.Composite4 = self.Composite5 = self.Composite6 = self.Composite7 = self.Composite8 = self.Composite9 = None
        elif self.Copy == '2':
            self.Composite1 = self.Composite2 = self.Composite
            self.Composite3 = self.Composite4 = self.Composite5 = self.Composite6 = self.Composite7 = self.Composite8 = self.Composite9 = None
        elif self.Copy == '3':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite
            self.Composite4 = self.Composite5 = self.Composite6 = self.Composite7 = self.Composite8 = self.Composite9 = None
        elif self.Copy == '4':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite4 = self.Composite
            self.Composite5 = self.Composite6 = self.Composite7 = self.Composite8 = self.Composite9 = None
        elif self.Copy == '5':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite4 = self.Composite5 = self.Composite
            self.Composite6 = self.Composite7 = self.Composite8 = self.Composite9 = None
        elif self.Copy == '6':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite4 = self.Composite5 = self.Composite6 = self.Composite
            self.Composite7 = self.Composite8 = self.Composite9 = None
        elif self.Copy == '7':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite4 = self.Composite5 = self.Composite6 = self.Composite7 = self.Composite
            self.Composite8 = self.Composite9 = None
        elif self.Copy == '8':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite4 = self.Composite5 = self.Composite6 = self.Composite7 = self.Composite8 = self.Composite
            self.Composite9 = None
        elif self.Copy == '9':
            self.Composite1 = self.Composite2 = self.Composite3 = self.Composite4 = self.Composite5 = self.Composite6 = self.Composite7 = self.Composite8 = self.Composite9 = self.Composite
        else:
            pass



    @api.onchange('CopyInvoiceExclude')
    def copy_invoice_exclude(self):
        if self.Copy == '1':
            self.InvoiceExclude1 = self.InvoiceExclude
            self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '2':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude
            self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '3':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude
            self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '4':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude
            self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '5':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude
            self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '6':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude
            self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '7':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude
            self.InvoiceExclude8 = self.InvoiceExclude9 = None
        elif self.Copy == '8':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude
            self.InvoiceExclude9 = None
        elif self.Copy == '9':
            self.InvoiceExclude1 = self.InvoiceExclude2 = self.InvoiceExclude3 = self.InvoiceExclude4 = self.InvoiceExclude5 = self.InvoiceExclude6 = self.InvoiceExclude7 = self.InvoiceExclude8 = self.InvoiceExclude9 = self.InvoiceExclude
        else:
            pass

    @api.onchange('CopyPriority')
    def copy_priority(self):
        if self.Copy == '1':
            self.Priority1 = self.Priority
            self.Priority2 = self.Priority3 = self.Priority4 = self.Priority5 = self.Priority6 = self.Priority7 = self.Priority8 = self.Priority9 = None
        elif self.Copy == '2':
            self.Priority1 = self.Priority2 = self.Priority
            self.Priority3 = self.Priority4 = self.Priority5 = self.Priority6 = self.Priority7 = self.Priority8 = self.Priority9 = None
        elif self.Copy == '3':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority
            self.Priority4 = self.Priority5 = self.Priority6 = self.Priority7 = self.Priority8 = self.Priority9 = None
        elif self.Copy == '4':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority4 = self.Priority
            self.Priority5 = self.Priority6 = self.Priority7 = self.Priority8 = self.Priority9 = None
        elif self.Copy == '5':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority4 = self.Priority5 = self.Priority
            self.Priority6 = self.Priority7 = self.Priority8 = self.Priority9 = None
        elif self.Copy == '6':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority4 = self.Priority5 = self.Priority6 = self.Priority
            self.Priority7 = self.Priority8 = self.Priority9 = None
        elif self.Copy == '7':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority4 = self.Priority5 = self.Priority6 = self.Priority7 = self.Priority
            self.Priority8 = self.Priority9 = None
        elif self.Copy == '8':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority4 = self.Priority5 = self.Priority6 = self.Priority7 = self.Priority8 = self.Priority
            self.Priority9 = None
        elif self.Copy == '9':
            self.Priority1 = self.Priority2 = self.Priority3 = self.Priority4 = self.Priority5 = self.Priority6 = self.Priority7 = self.Priority8 = self.Priority9 = self.Priority
        else:
            pass

    @api.onchange('CopySampleMassReceived')
    def copy_sample_mass_received(self):
        if self.Copy == '1':
            self.SampleMassReceived1 = self.SampleMassReceived
            self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '2':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived
            self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '3':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived
            self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '4':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived
            self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '5':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived
            self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '6':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived
            self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '7':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived
            self.SampleMassReceived8 = self.SampleMassReceived9 = None
        elif self.Copy == '8':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived
            self.SampleMassReceived9 = None
        elif self.Copy == '9':
            self.SampleMassReceived1 = self.SampleMassReceived2 = self.SampleMassReceived3 = self.SampleMassReceived4 = self.SampleMassReceived5 = self.SampleMassReceived6 = self.SampleMassReceived7 = self.SampleMassReceived8 = self.SampleMassReceived9 = self.SampleMassReceived
        else:
            pass

    @api.multi
    def action_report_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        if not self.env.context.get('open_wizard'):
            requests = self.pool.get('olims.analysis_request').browse(self.env.cr, self.env.uid, self._ids)
            if requests.Client.payment_not_current:
                view_id = self.pool.get('ir.ui.view').search(self.env.cr, self.env.uid,\
                                                         [('name', '=', 'Payment Not Current Dialog Box')],\
                                                             context=self.env.context)
                context = self.env.context.copy()
                context.update({'do_action': 'send_COA_mail'})
                return {
                    'name': _('Payment Not Current'),
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'olims.message_dialog_box',
                    'view_id': view_id,
                    'target': 'new',
                    'type': 'ir.actions.act_window',
                    'context': context,
                }


        emails_send = []
        for email in self.CCEmails:
            emails_send.append(email.name)
        ir_model_data = self.env['ir.model.data']
        data = self.env['olims.analysis_request'].search([("id","in",self._ids)])
        if self.LotID and self.ClientReference:
            name = self.LotID + '-' + self.ClientReference
        elif self.LotID:
            name = self.LotID
        elif self.ClientReference:
            name = self.ClientReference
        else:
            name = 'COA'
        try:
            template_data = self.env["mail.template"].search([('name', '=', 'OLiMS Email Template')])
            template_data.report_name = name
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

    @api.depends("is_flagged")
    def set_flagged_status(self):
        for record in self:
            if record.is_flagged == True:
                record.flagged_status = "Flagged"

    @api.onchange("Analyses")
    def update_ar_prices(self):
        list_of_service_ids = []
        self.Discount = 0.00
        self.Subtotal = 0.00
        self.VAT = 0.00
        self.Total = 0.00
        profiles_price = {}
        profiles_VAT = {}

        self.Analyses = None
        for rec in self.AnalysisProfile:
            for service in rec.Service:
                self.Analyses += self.Analyses.new({'Category':service.Services.category.id,
                                    'Services':service.Services.id,
                                    'Min':service.Services.Min,
                                    'Max':service.Services.Max,
                                    'Partition': self.Partition.id})

        for rec in self.AnalysisProfile:
            for service in rec.Service:
                list_of_service_ids.append(service.Services.id)

        for service_record in self.Analyses:
            for rec in self.AnalysisProfile:
                if service_record.Services.id in list_of_service_ids and rec and rec.UseAnalysisProfilePrice:
                    profiles_price[rec.id] = rec.AnalysisProfilePrice
                    profiles_VAT[rec.id] = rec.AnalysisProfileVAT

                else:
                    self.Discount += service_record.Services.Price * self.Client.M_Discount / 100
                    self.Subtotal += service_record.Services.Price - (service_record.Services.Price *self.Client.M_Discount / 100)
                    self.VAT += service_record.Services.VAT * (service_record.Services.Price - (service_record.Services.Price * self.Client.M_Discount / 100)) /100
                    self.Total = self.Subtotal + self.VAT

        for profile, profile_price in profiles_price.iteritems():
            self.Discount = profile_price * self.Client.M_Discount / 100
            self.Subtotal += profile_price - self.Discount
            self.VAT = profiles_VAT[profile] / 100 * self.Subtotal
            self.Total += (profile_price - self.Discount) + self.VAT

    @api.onchange("Template","Template1","Template2","Template3",\
                "Template4","Template5","Template6","Template7",\
                "Templat8","Template9")
    def add_contact_and_email_of_template(self):
        if self.Template:
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
        if self.Template4:
            self.Contact4 = self.Template4.contact_id
            self.CCEmails4 = self.Template4.email_id
            self.AnalysisProfile4 = self.Template4.AnalysisProfile
            self.SampleType4 = self.Template4.SampleType
            self.Priority4 = self.Template4.priority
        if self.Template5:
            self.Contact5 = self.Template5.contact_id
            self.CCEmails5 = self.Template5.email_id
            self.AnalysisProfile5 = self.Template5.AnalysisProfile
            self.SampleType5 = self.Template5.SampleType
            self.Priority5 = self.Template5.priority
        if self.Template6:
            self.Contact6 = self.Template6.contact_id
            self.CCEmails6 = self.Template6.email_id
            self.AnalysisProfile6 = self.Template6.AnalysisProfile
            self.SampleType6 = self.Template6.SampleType
            self.Priority6 = self.Template6.priority
        if self.Template7:
            self.Contact7 = self.Template7.contact_id
            self.CCEmails7 = self.Template7.email_id
            self.AnalysisProfile7 = self.Template7.AnalysisProfile
            self.SampleType7 = self.Template7.SampleType
            self.Priority7 = self.Template7.priority
        if self.Template8:
            self.Contact8 = self.Template8.contact_id
            self.CCEmails8 = self.Template8.email_id
            self.AnalysisProfile8 = self.Template8.AnalysisProfile
            self.SampleType8 = self.Template8.SampleType
            self.Priority8 = self.Template8.priority
        if self.Template9:
            self.Contact9 = self.Template9.contact_id
            self.CCEmails9 = self.Template9.email_id
            self.AnalysisProfile9 = self.Template9.AnalysisProfile
            self.SampleType9 = self.Template9.SampleType
            self.Priority9 = self.Template9.priority

    @api.onchange("copy_paid_cash")
    def CopyPaidCash(self):
        if self.Copy == '1':
            self.paid_cash1 = self.paid_cash
            self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '2':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash
            self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '3':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash
            self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '4':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash
            self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '5':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash
            self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '6':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash
            self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '7':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash
            self.paid_cash8 = self.paid_cash9 = None
        elif self.Copy == '8':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash
            self.paid_cash9 = None
        elif self.Copy == '9':
            self.paid_cash1 = self.paid_cash2 = self.paid_cash3 = self.paid_cash4 = self.paid_cash5 = self.paid_cash6 = self.paid_cash7 = self.paid_cash8 = self.paid_cash9 = self.paid_cash
        else:
            pass
    def workflow_script_unpublish(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {'state': 'sample_received'}, context=context)
        return True

    @api.multi
    def unpublish_analysis_request(self):
        manage_results_obj = self.env["olims.manage_analyses"].search(["|",("manage_analysis_id","=",self.id),
            ("lab_manage_analysis_id","=",self.id)
            ]).write({"state": "sample_received"})
        self.signal_workflow("unpublish")

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
            ws_record_id = ws_record_obj.search(self.env.cr, self.env.uid, [('request_analysis_id', '=', record.manage_analysis_id.id),('category','=',record.Category.id),('analysis','=',record.Service.id)])
            if ws_record_id:
                ws_record_id = ws_record_id[0]
        if record.lab_manage_analysis_id:
            ws_record_id = ws_record_obj.search(self.env.cr, self.env.uid, [('request_analysis_id', '=', record.lab_manage_analysis_id.id),('category','=',record.Category.id),('analysis','=',record.LabService.id)])
            if ws_record_id:
                ws_record_id = ws_record_id[0]
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
        ar_ids = []
        analysis_ids = []
        for record in self:
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

    def compute_ar_state(self):
        for record in self:
            record.is_pre_enter = (record.lab_manage_analysis_id.state == 'pre_enter')

class ParticularReport(models.AbstractModel):
    _name = 'report.olims.report_certificate_of_analysis'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('olims.report_certificate_of_analysis')
        self_browse = self.browse()
        data = self.env['olims.analysis_request'].search([("id","in",self._ids)])

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': data,
        }

        return report_obj.render('olims.report_certificate_of_analysis', docargs)

AnalysisRequest.initialze(schema)
FieldAnalysisService.initialze(schema_analysis)
ManageAnalyses.initialze(manage_result_schema)