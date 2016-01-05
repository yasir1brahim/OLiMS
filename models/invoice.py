
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~

#from dependencies.dependency import ClassSecurityInfo
#from lims.content.bikaschema import BikaSchema
#from lims.interfaces import IInvoice
#from dependencies.dependency import DateTimeField, DateTimeWidget
#from dependencies.dependency import DateTime
#from dependencies.dependency import implements
#from lims.config import ManageInvoices, ManageBika, PROJECTNAME\
#from dependencies.dependency import PersistentMapping
#from dependencies.dependency import View

from dependencies.dependency import Decimal
from dependencies.dependency import getToolByName
from dependencies.dependency import safe_unicode
from lims import bikaMessageFactory as _
from lims.utils import t
from lims.utils import to_utf8


from datetime import date
from openerp import fields, models, api
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.date_time_field import DateTimeField
from fields.file_field import FileField
from fields.reference_field import ReferenceField
from fields.widget.widget import StringWidget, TextAreaWidget, BooleanWidget, FileWidget, DateTimeWidget
import datetime
import logging
import sys
_logger = logging.getLogger(__name__)


#schema = BikaSchema.copy() + Schema((
schema = (StringField(string='title',required=1),
    StringField(string='InvoiceNumber',
                compute='_ComputeInvoiceId',
                required=0),
    fields.Many2one(string='Client',
        required=0,
        comodel_name='olims.client',
#         vocabulary_display_path_bound=sys.maxsize,
#         allowed_types=('Client',),
#         relationship='ClientInvoice',
    ),
    DateTimeField('Invoice Date',
#         required=1,
#         vocabulary_display_path_bound=sys.maxsize,
#         allowed_types=('AnalysisRequest',),
#         relationship='AnalysisRequestInvoice',
    ),

    DateTimeField('StartDate',
        required=1,
        default_method='current_date',
        widget=DateTimeWidget(
            label=_("Date"),
        ),
    ),
    DateTimeField('EndDate',
        required=1,
        default_method='end_date',
        widget=DateTimeWidget(
            label=_("End Date"),
        ),
    ),
    TextField('Remarks',
        searchable=True,
        #default_content_type='text/plain',
        #allowed_content_types=('text/plain', ),
        #default_output_type="text/plain",
        widget=TextAreaWidget(
         #   macro="bika_widgets/remarks",
            label=_("Remarks"),
            append_only=True,
        ),
    ),

    fields.Float(string='Subtotal',
        compute='_getSubtotal'
        # widget=ComputedWidget(
        #     label=_("Subtotal"),
        #     visible=False,
        # ),
    ),
    fields.Float(string='VAT',
        compute='_getVATAmount',
    #     widget=ComputedWidget(
    #         label=_("VAT Total"),
    #         visible=False,
    #     ),
    ),
    fields.Float('Total',
        compute='_getTotal',
#         widget=ComputedWidget(
#             label=_("Total"),
#             visible=False,
#         ),
    ),
    # ComputedField('ClientUID',
    #     expression='here.getClient() and here.getClient().UID()',
    #     widget=ComputedWidget(
    #         visible=False,
    #     ),
    # ),
    fields.Many2one(string='Order_id',
        comodel_name='olims.supply_order',
    ),
)

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# TitleField = schema['title']
# TitleField.required = 0
# TitleField.widget.visible = False


# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# class InvoiceLineItem(PersistentMapping):
#     pass


class Invoice(models.Model, BaseOLiMSModel): #(BaseFolder):
    _name='olims.invoice'
    _rec_name = 'title'
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
    # implements(IInvoice)
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema
    def _ComputeInvoiceId(self):
        for record in self:
            invoiceid = 'I-0' + str(record.id)
            record.InvoiceNumber = invoiceid
    @api.model
    def create(self, values):
        order_date1 = datetime.datetime.strptime(values.get('StartDate'), "%Y-%m-%d %H:%M:%S")
        order_date2 = datetime.datetime.strptime(values.get('EndDate'), "%Y-%m-%d %H:%M:%S")

        stringdate1 = order_date1.strftime("%Y-%m-%d %H:%M:%S")
        stringdate2 = order_date2.strftime("%Y-%m-%d %H:%M:%S")
        order_object = self.env['olims.supply_order']

        order_object_ids = order_object.search([('DateDispatched', '>=', stringdate1),('DateDispatched', '<=', stringdate2)])
        if order_object_ids:
            for obj in order_object_ids:
                line = order_object.browse(obj.id)
                client_id = line.Client.id #.encode('ascii','ignore')
                supply_order_value_dict = {'Invoice Date': datetime.datetime.now(),
                                           'Client': client_id,
                                           'Order_id' : line.id
                                           }
                values.update(supply_order_value_dict)
                res = super(Invoice, self).create(values)
            return res
        else:
            res = super(Invoice, self).create(values)
            return res

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        """ Return the Invoice Id as title """
        return safe_unicode(self.getId()).encode('utf-8')

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
    #security.declareProtected(View, 'getSubtotal')

    def _getSubtotal(self):
        """ Compute Subtotal """
        for record in self:
            total = record.Order_id.SubTotal
            record.Subtotal = total
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
    #security.declareProtected(View, 'getVATAmount')

    def _getVATAmount(self):
        """ Compute VAT """
        for record in self:
            
            record.VAT = record.Order_id.VAT

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
    #security.declareProtected(View, 'getTotal')

    def _getTotal(self):
        """ Compute Total """
        for record in self:
            record.Total = record.Order_id.Total
        # total = sum([float(obj['Total']) for obj in self.invoice_lineitems])
        

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
    #security.declareProtected(View, 'getInvoiceSearchableText')

    def getInvoiceSearchableText(self):
        """ Aggregate text of all line items for querying """
        s = ''
        for item in self.invoice_lineitems:
            s = s + item['ItemDescription']
        return s

    # XXX workflow script
    def workflow_script_dispatch(self):
        """ dispatch order """
        self.setDateDispatched(DateTime())

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
    #security.declarePublic('current_date')

    def current_date(self):
        """ return current date """
        return DateTime()

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
#registerType(Invoice, PROJECTNAME)
Invoice.initialze(schema)