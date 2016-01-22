from openerp import fields, models
from openerp.tools.translate import _
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.boolean_field import BooleanField
from fields.file_field import FileField
from fields.date_time_field import DateTimeField
from fields.integer_field import IntegerField
from fields.widget.widget import StringWidget, DateTimeWidget, \
                                FileWidget, IntegerWidget

AR_IMPORT_STATES = (
                    ('imported','Imported'),
                    ('submitted','Submitted'),
                    ('cancelled','Cancelled'),
                    )                                
schema = (
    StringField('FileName',
        searchable = True,
        widget = StringWidget(
            label = _("Filename"),
        ),
    ),
    FileField('OriginalFile',
        searchable = True,
        widget = FileWidget(
            label = _("Original File"),
            visible={'edit': 'invisible',
                     'view': 'visible', 'add': 'invisible'},
        ),
    ),
    StringField('ClientTitle',
        searchable = True,
        widget = StringWidget(
            label = _("Client Name"),
        ),
    ),
    StringField('ClientPhone',
        widget = StringWidget(
            label = _("Client Phone"),
        ),
    ),
    StringField('ClientFax',
        widget = StringWidget(
            label = _("Client Fax"),
        ),
    ),
    StringField('ClientAddress',
        widget = StringWidget(
            label = _("Client Address"),
        ),
    ),
    StringField('ClientCity',
        widget = StringWidget(
            label = _("Client City"),
        ),
    ),
    StringField('ClientID',
        searchable = True,
        widget = StringWidget(
            label = _("Client ID"),
        ),
    ),
    StringField('ContactID',
        widget = StringWidget(
            label = _("Contact ID"),
        ),
    ),
    StringField('ContactName',
        widget = StringWidget(
            label = _("Contact Name"),
        ),
    ),
          
    fields.Many2many(string='Contact', comodel_name='olims.contact', relation='arimport_contact'
                     ),
    
    StringField('ClientEmail',
        widget = StringWidget(
            label = _("Client Email"),
        ),
    ),
    StringField('CCContactID',
        widget = StringWidget(
            label = _("CC Contact ID"),
        ),
    ),


    fields.Many2one(string='CCContact',
                    comodel_name='olims.contact',
                    help="Select a default preservation for this " + \
                                    "analysis service. If the preservation depends on " + \
                                    "the sample type combination, specify a preservation " + \
                                    "per sample type in the table below",
                    required=False,
    ),


    StringField('CCNamesReport',
        widget = StringWidget(
            label = _("Report Contact Names"),
        ),
    ),
    StringField('CCEmailsReport',
        widget = StringWidget(
            label = _("CC Email - Report"),
        ),
    ),
    StringField('CCEmailsInvoice',
        widget = StringWidget(
            label = _("CC Email - Invoice"),
        ),
    ),
    StringField('OrderID',
        searchable = True,
        widget = StringWidget(
            label = _("Order ID"),
        ),
    ),
    StringField('QuoteID',
        searchable = True,
        widget = StringWidget(
            label = _("QuoteID"),
        ),
    ),
    StringField('SamplePoint',
        searchable = True,
        widget = StringWidget(
            label = _("Sample Point"),
        ),
    ),
    StringField('Temperature',
        widget = StringWidget(
            label = _("Temperature"),
        ),
    ),
    DateTimeField('DateImported',
        required = 1,
        widget = DateTimeWidget(
            label = _("Date Imported"),
            size=12,
            visible={'edit': 'visible', 'view': 'visible', 'add': 'visible',
                     'secondary': 'invisible'},
        ),
    ),
    DateTimeField('DateApplied',
        widget = DateTimeWidget(
            label = _("Date Applied"),
            size=12,
            visible={'edit': 'visible', 'view': 'visible', 'add': 'visible',
                     'secondary': 'invisible'},
        ),
    ),
    IntegerField('NumberSamples',
        widget = IntegerWidget(
            label = _("Number of samples"),
        ),
    ),
    BooleanField('Status',
        searchable = True,
        widget = StringWidget(
            label = _("Status"),
        ),
    ),

    fields.Many2one(string='Priority',
                    comodel_name='olims.ar_priority',
    ),
    fields.Selection(string='state',
                     selection=AR_IMPORT_STATES,
                     default='imported',
                     select=True,
                     required=True, readonly=True,
                     copy=False, track_visibility='always'
    ),
          
)

class ARImport(models.Model, BaseOLiMSModel):#(BaseFolder):
    _name = 'olims.ar_import'


    # workflow methods
    
    def workflow_script_submit(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'submitted',
        }, context = context)
        return True

    def workflow_script_cancel(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'cancelled',
        }, context = context)
        return True

ARImport.initialze(schema)
