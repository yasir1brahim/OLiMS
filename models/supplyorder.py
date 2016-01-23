from openerp.tools.translate import _
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

schema = (

  fields.Many2one(string='Contact',
        comodel_name='olims.contact',
        required =False,
    ),

    fields.Char(string='OrderNumber',
                compute='compute_order_id',
    ),

#     fields.Many2one(string='Invoice',
#         comodel_name='olims.invoice',
#         required =False,
#          help =    'contact',
#     # vocabulary_display_path_bound=sys.maxsize,
#     #                allowed_types=('Invoice',),
#     #                referenceClass=HoldingReference,
#     #                relationship='OrderInvoice',
#     ),

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
                compute='computeFieldsOnChange'
    ),
    fields.Float(string='VAT',
                compute='computeFieldsOnChange'
    ),
    fields.Float(string='Total',
                compute='computeFieldsOnChange'
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

    fields.Many2one(string='Client',
            comodel_name='olims.client',
                  ),
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

class SupplyOrder(models.Model, BaseOLiMSModel):
    _name='olims.supply_order'

    def compute_order_id(self):
        order_string = 'O-'
        for record in self:
            record.OrderNumber = order_string + str(record.id)

    @api.onchange('OrderLines')
    def computeFieldsOnChange(self):
        subTotal = vatAmount = 0.0;
        for s in self:
            subTotal = 0.0
            vatAmount = 0.0
            if s.OrderLines:
                for row in s.OrderLines:
                    if row.Quantity and row.Price and row.VAT:
                        subTotal += float(row.Quantity) * row.Price
                        vatAmount += (float(row.Quantity) * row.Price * float(row.VAT))/100
            s.SubTotal = subTotal
            s.VAT = vatAmount
            s.Total = s.SubTotal + s.VAT

    @api.multi
    def print_order(self):
        return self.env['report'].get_action(self, 'olims.report_order_detail')

    
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
        for s in self:
            if s.Products:
                s.Total = s.Products.Price * float(s.Quantity)
                s.Description = s.Products.Description
                s.Volume = s.Products.Volume
                s.Unit = s.Products.Unit
                s.VAT = s.Products.VAT
                s.Price = s.Products.Price


SupplyOrder.initialze(schema)
SupplyOrderLine.initialze(schema_order_line)