# # ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~

# from dependencies.dependency import *
# from dependencies.dependency import ClassSecurityInfo
# from lims import bikaMessageFactory as _
# from lims.browser.widgets import DateTimeWidget
# from lims.browser.widgets import ReferenceWidget as BikaReferenceWidget
# from lims.config import PROJECTNAME
# from lims.content.bikaschema import BikaSchema
# from lims.interfaces import ISupplyOrder
# from lims.utils import t
# from dependencies.dependency import DateTime
# from dependencies.dependency import PersistentMapping
# from dependencies.dependency import Decimal
# from dependencies import atapi
# from dependencies.dependency import View
# from dependencies.dependency import IConstrainTypes
# from dependencies.dependency import implements



from lims import bikaMessageFactory as _
from openerp import fields, models, api
from fields.string_field import StringField
from fields.text_field import TextField
from fields.date_time_field import DateTimeField
from fields.fixed_point_field import FixedPointField

from fields.widget.widget import TextAreaWidget, StringWidget, DateTimeWidget, \
                                DecimalWidget
from base_olims_model import BaseOLiMSModel
import datetime
ORDER_STAES = (
               ('pending','Order pending'),
               ('dispatched','Dispatched'),
               )

#schema = BikaSchema.copy() + Schema((
schema = (

  fields.Many2one(string='Contact',
        comodel_name='olims.contact',
        requried =True,
#         vocabulary_display_path_bound=sys.maxsize,
    #   allowed_types=('Contact',),
    #   referenceClass=HoldingReference,
    #   relationship='SupplyOrderContact',
    #   widget=BikaReferenceWidget(
    #     render_own_label=True,
    #     showOn=True,
    #     colModel=[
    #       {'columnName': 'UID', 'hidden': True},
    #       {'columnName': 'Fullname', 'width': '50', 'label': _('Name')},
    #       {'columnName': 'EmailAddress', 'width': '50', 'label': _('Email Address')},
    #     ],
    ),

    fields.Char(string='OrderNumber',
                compute='compute_order_id',
    ),

    fields.Many2one(string='Invoice',
        comodel_name='olims.invoice',
        requried =False,
         help =    'contact',
    # vocabulary_display_path_bound=sys.maxsize,
    #                allowed_types=('Invoice',),
    #                referenceClass=HoldingReference,
    #                relationship='OrderInvoice',
    ),

    DateTimeField(
      'OrderDate',
      required=1,
      default_method='current_date',
      widget=DateTimeWidget(
        label=_("Order Date"),
        size=12,
        render_own_label=True,
        visible={
          'edit': 'visible',
          'view': 'visible',
          'add': 'visible',
          'secondary': 'invisible'
        },
      ),
    ),
    DateTimeField('DateDispatched',readonly=True,
                  widget=DateTimeWidget(
                      label=_("Date Dispatched"),
                      ),
                  ),
    TextField('Remarks',
        searchable=True,
        default_content_type='text/plain',
        allowed_content_types=('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            macro="bika_widgets/remarks",
            label=_("Remarks"),
            append_only=True,
        ),
    ),
    fields.Float(string='SubTotal',
                compute='compute_subtotal'
    ),
    fields.Float(string='VAT',
                compute='compute_VATAmount'
    ),
    fields.Float(string='Total',
                compute='compute_Total'
    ),
    fields.Selection(string='state',selection=ORDER_STAES,
        default='pending', select=True,
        required=True, readonly=True,
        copy=False, track_visibility='always'
        ),
    fields.One2many('olims.supply_order_line',
                                 'supply_order_id',
                                 string='OrderLines'
    ),

# ~~~~~~~ To be implemented ~~~~~~~
    # ComputedField('ClientUID',
    #               expression = 'here.aq_parent.UID()',
    #               widget = ComputedWidget(
    #                   visible=False,
    #                   ),
    #               ),
    # ComputedField('ProductUID',
    #               expression = 'context.getProductUIDs()',
    #               widget = ComputedWidget(
    #                   visible=False,
    #                   ),
    #               ),
)
schema_order_line = (TextField('Description',
                               compute='_ComputeFieldsValues',
    widget=TextAreaWidget(
        label=_('Description'),
        description=_('Used in item listings and search results.'),
        ),
    ),
    StringField('Volume',
                compute='_ComputeFieldsValues',
        widget = StringWidget(
            label=_("Volume"),
        )
    ),
    StringField('Unit',
#                 store=True,
                compute='_ComputeFieldsValues',
        widget = StringWidget(
            label=_("Unit"),
        )
    ),
    FixedPointField('VAT',
                    compute='_ComputeFieldsValues',
        default=14.00,
        default_method = 'getDefaultVAT',
        widget = DecimalWidget(
            label=_("VAT %"),
            description=_("Enter percentage value eg. 14.0"),
        ),
    ),
    FixedPointField('Price',
                    compute='_ComputeFieldsValues',
                    required=0,
                    widget = DecimalWidget(
                                           label=_("Price excluding VAT"),
                                           )
    ),
    StringField('Quantity',
                required=0,
                searchable=True,
                widget=StringWidget(
                    label=_("Quantity"),
                    ),
                ),
    fields.Many2one('olims.supply_order',
                    string='supply_order_id',
                    required=False,
                    ondelete='cascade',
                    index=True, copy=False
                    ),
    fields.Many2one('olims.lab_product',
                    string='Products',
                    ondelete='restrict',
                    required=True
                    ),
    fields.Float(string='Total',
                compute='_ComputeFieldsValues'
    ),
    )

#schema['title'].required = False

# class SupplyOrderLineItem(PersistentMapping):
#     pass

class SupplyOrder(models.Model, BaseOLiMSModel): #BaseFolder
    _name='olims.supply_order'
    def compute_subtotal(self):
        if self.OrderLines:
            for records in self.OrderLines:
                if records.Quantity and records.Price:
                    quantity = records.Quantity
                    product_price_excluding_VAT = records.Price
                    self.SubTotal +=  int(quantity) * product_price_excluding_VAT
    def compute_order_id(self):
        order_string = 'O-'
        for record in self:
            record.OrderNumber = order_string + str(record.id)
    def compute_VATAmount(self):
        if self.OrderLines:
            for records in self.OrderLines:
                if records.Quantity and records.Price:
                    vat_amount = records.VAT
                    self.VAT +=  (vat_amount * records.Total)/100
#                     for item in records.Products:
#                         self.VAT +=  (vat_amount * item.TotalPrice)/100
    def compute_Total(self):
        for recod in self:
            recod.Total = self.SubTotal + self.VAT
    # implements(ISupplyOrder, IConstrainTypes)
    #
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    # _at_rename_after_creation = True
    # supplyorder_lineitems = []
    #
    # def _renameAfterCreation(self, check_auto_id=False):
    #     from lims.idserver import renameAfterCreation
    #     renameAfterCreation(self)
    #
    # def getInvoiced(self):
    #     if self.getInvoice():
    #         return True
    #     else:
    #         return False
    #
    # def Title(self):
    #     """ Return the OrderNumber as title """
    #     return safe_unicode(self.getOrderNumber()).encode('utf-8')
    #
    # def getOrderNumber(self):
    #     return safe_unicode(self.getId()).encode('utf-8')
    #
    # def getContacts(self):
    #     adapter = getAdapter(self.aq_parent, name='getContacts')
    #     return adapter()
    #
    # #security.declarePublic('getContactUIDForUser')
    #
    # def getContactUIDForUser(self):
    #     """ get the UID of the contact associated with the authenticated
    #         user
    #     """
    #     user = self.REQUEST.AUTHENTICATED_USER
    #     user_id = user.getUserName()
    #     r = self.portal_catalog(
    #         portal_type='Contact',
    #         getUsername=user_id
    #     )
    #     if len(r) == 1:
    #         return r[0].UID
    #
    # #security.declareProtected(View, 'getTotalQty')
    #
    # def getTotalQty(self):
    #     """ Compute total qty """
    #     if self.supplyorder_lineitems:
    #         return sum(
    #             [obj['Quantity'] for obj in self.supplyorder_lineitems])
    #     return 0
    #
    # #security.declareProtected(View, 'getSubtotal')
    #
    # def getSubtotal(self):
    #     """ Compute Subtotal """
    #     if self.supplyorder_lineitems:
    #         return sum(
    #             [(Decimal(obj['Quantity']) * Decimal(obj['Price'])) for obj in self.supplyorder_lineitems])
    #     return 0
    #
    # #security.declareProtected(View, 'getVATAmount')
    #
    # def getVATAmount(self):
    #     """ Compute VAT """
    #     return Decimal(self.getTotal()) - Decimal(self.getSubtotal())
    #
    # #security.declareProtected(View, 'getTotal')
    #
    # def getTotal(self):
    #     """ Compute TotalPrice """
    #     total = 0
    #     for lineitem in self.supplyorder_lineitems:
    #         total += Decimal(lineitem['Quantity']) * \
    #                  Decimal(lineitem['Price']) *  \
    #                  ((Decimal(lineitem['VAT']) /100) + 1)
    #     return total
    #
    def workflow_script_dispatch(self, cr, uid, ids, context=None):
        """ dispatch order """
        dispatchdate = datetime.datetime.now()
        return self.write(cr, 
                          uid, ids, 
                          {
                           'state': 'dispatched', 
                           'DateDispatched': dispatchdate
                           }, 
                          context=context)
        
#         self.setDateDispatched(DateTime())
#         self.reindexObject()
    #
    # #security.declareProtected(View, 'getProductUIDs')
    #
    # def getProductUIDs(self):
    #     """ return the uids of the products referenced by order items
    #     """
    #     uids = []
    #     for orderitem in self.objectValues('XupplyOrderItem'):
    #         product = orderitem.getProduct()
    #         if product is not None:
    #             uids.append(orderitem.getProduct().UID())
    #     return uids
    #
    # #security.declarePublic('current_date')
    #
    # def current_date(self):
    #     """ return current date """
    #     return DateTime()

class SupplyOrderLine(models.Model, BaseOLiMSModel):
    _name = 'olims.supply_order_line'

    @api.onchange('Products')
    def _onchange_product(self):
        # set auto-changing field
        if self.Products:
            self.Description = self.Products.Description
            self.Volume = self.Products.Volume
            self.Unit = self.Products.Unit
            self.VAT = self.Products.VAT
            self.Price = self.Products.Price
    @api.onchange('Products','Quantity')
    def _ComputeFieldsValues(self):
#         print self
#         pass
        for s in self:
            if s.Products:
                s.Total = s.Products.Price * float(s.Quantity)
                s.Description = s.Products.Description
                s.Volume = s.Products.Volume
                s.Unit = s.Products.Unit
                s.VAT = s.Products.VAT
                s.Price = s.Products.Price

#atapi.registerType(SupplyOrder, PROJECTNAME)
SupplyOrder.initialze(schema)
SupplyOrderLine.initialze(schema_order_line)