from openerp.tools.translate import _
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
from openerp.exceptions import Warning

schema = (StringField(string='title',required=1),
    StringField(string='InvoiceNumber',
                compute='_ComputeInvoiceId',
                required=0),
    fields.Many2one(string='Client',
        required=0,
        comodel_name='olims.client',
    ),
    DateTimeField('Invoice Date',
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
        widget=TextAreaWidget(
            label=_("Remarks"),
            append_only=True,
        ),
    ),

    fields.Float(string='Subtotal',
        compute='_getSubtotal'
    ),
    fields.Float(string='VAT',
        compute='_getVATAmount',
    ),
    fields.Float('Total',
        compute='_getTotal',
    ),
    fields.Many2one(string='Order_id',
        comodel_name='olims.supply_order',
    ),
)

class Invoice(models.Model, BaseOLiMSModel):
    _name='olims.invoice'
    _rec_name = 'title'

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


    def _getSubtotal(self):
        """ Compute Subtotal """
        for record in self:
            total = record.Order_id.SubTotal
            record.Subtotal = total

    def _getVATAmount(self):
        """ Compute VAT """
        for record in self:
            
            record.VAT = record.Order_id.VAT


    def _getTotal(self):
        """ Compute Total """
        for record in self:
            record.Total = record.Order_id.Total

class ARInvoice(models.Model):
    _name = "olims.ar_invoice"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Invoice Id", compute="_compute_invoice_id",
        store=True)
    receipt_number = fields.Char(string="Receipt Number", compute="_compute_receipt_number",
        store=True)
    client_id = fields.Many2one(string="Client",comodel_name="olims.client")
    analysis_request_id = fields.Many2many(string="Analysis Request ID",
        comodel_name="olims.analysis_request")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="Start Date")
    published_date = fields.Datetime(string="Published Date")
    sub_total = fields.Float(string="Sub Total", compute='_get_subtotal', store=True)
    total = fields.Float(string="Total Amount", compute='_get_total', store=False)
    state = fields.Selection(selection=(
        ('open', 'Open'),
        ('closed','Closed'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled')),
    string="State",
    default="open")
    adjust_percent = fields.Float(string='Adjustment(Percentage)')
    adjust_percent_text = fields.Char(string='Adjustment', default="Adjustment percentage")
    adjust_amount_text = fields.Char(string='Adjustment Amount', default="Adjustment, dollars")
    adjust_amount = fields.Float(string='Adjustment(Amount)')
    adjusted_total = fields.Float(string="Adjusted Total", compute="update_total_adjusted", store=False)

    @api.multi
    def unlink(self):
        for record in self:
            print record.state
            if record.state!='open':
                raise Warning(_("Invoice cannot be deleted in %s state") % str(record.state).capitalize())
            else:
                pass
        return super(ARInvoice, self).unlink()


    @api.depends("client_id")
    def _compute_invoice_id(self):
        for record in self:
            if record.id < 10:
                record.name = "INV-0"+str(record.id)
            else:
                record.name = "INV-"+str(record.id)

    @api.depends("client_id")
    def _compute_receipt_number(self):
        for record in self:
            record.receipt_number = "1000"+str(record.id)

    @api.depends("analysis_request_id.Total")
    def _get_total(self):
        for record in self:
            for ar_record in record.analysis_request_id:
                record.total += ar_record.Total
            if record.client_id.Invoice_Discount:
                discount = record.total - (record.total * record.client_id.Invoice_Discount / 100)
                record.total = discount

    @api.model
    def create(self, values):
        if values.get('analysis_request_id',None):
            analysis_request = values.get('analysis_request_id')[0]
            ar_object = self.env["olims.analysis_request"].search([('id', 'in', analysis_request[2])])
            for ar_record in ar_object:
                if not ar_record.InvoiceExclude:
                    profile_service_ids_list = []
                    amount_subtotal = 0.00
                    amount_vat = 0.00
                    amount_total = 0.00
                    s_amount_subtotal = 0.00
                    s_amount_vat = 0.00
                    s_amount_total = 0.00
                    profiles_price = {}
                    profiles_VAT = {}

                    for profile_record in ar_record.AnalysisProfile:
                        for service in profile_record.Service:
                            profile_service_ids_list.append(service.Services.id)

                    for ar_service in ar_record.Analyses:
                        for rec in ar_record.AnalysisProfile:
                            if ar_service.Services.id in profile_service_ids_list and rec.UseAnalysisProfilePrice:
                                profiles_price[rec.id] = rec.AnalysisProfilePrice
                                profiles_VAT[rec.id] = rec.AnalysisProfileVAT

                            else:
                                s_amount_subtotal = ar_service.Services.Price - (ar_service.Services.Price * ar_record.Client.M_Discount /100)
                                s_amount_vat = s_amount_subtotal * ar_service.Services.VAT / 100
                                s_amount_total += s_amount_subtotal + s_amount_vat

                    for profile, profile_price in profiles_price.iteritems():
                        amount_subtotal += profile_price - (profile_price * ar_record.Client.M_Discount /100)
                        amount_vat = amount_subtotal * profiles_VAT[profile] / 100
                        amount_total += (profile_price - (profile_price * ar_record.Client.M_Discount /100)) + amount_vat

                    ar_record.write({"Total": (amount_total + s_amount_total)})
                else:
                    ar_record.write({"Discount": 0.0, "Subtotal": 0.0, "VAT": 0.0, "Total":0.0})
            res = super(ARInvoice,self).create(values)
            ar_object.write({'ar_invoice_id': res.id})
            return res
        else:
            res = super(ARInvoice,self).create(values)
            return res

    @api.multi
    def write(self, values):
        if values.get('analysis_request_id',None):
            analysis_request = values.get('analysis_request_id')[0]
            ar_invoice_delete = self.env["olims.analysis_request"].search([('ar_invoice_id', '=', self.id), ('id', 'not in', analysis_request[2] ) ])
            ar_invoice_delete.write({'ar_invoice_id':False})
            ar_object = self.env["olims.analysis_request"].search([('id', 'in', analysis_request[2])])
            for ar_record in ar_object:
                if not ar_record.InvoiceExclude:
                    profile_service_ids_list = []
                    amount_subtotal = 0.00
                    amount_vat = 0.00
                    amount_total = 0.00
                    s_amount_subtotal = 0.00
                    s_amount_vat = 0.00
                    s_amount_total = 0.00
                    profiles_price = {}
                    profiles_VAT = {}

                    for profile_record in ar_record.AnalysisProfile:
                        for service in profile_record.Service:
                            profile_service_ids_list.append(service.Services.id)

                    for ar_service in ar_record.Analyses:
                        for rec in ar_record.AnalysisProfile:
                            if ar_service.Services.id in profile_service_ids_list and rec.UseAnalysisProfilePrice:
                                profiles_price[rec.id] = rec.AnalysisProfilePrice
                                profiles_VAT[rec.id] = rec.AnalysisProfileVAT

                            else:
                                s_amount_subtotal = ar_service.Services.Price - (ar_service.Services.Price * ar_record.Client.M_Discount /100)
                                s_amount_vat = s_amount_subtotal * ar_service.Services.VAT / 100
                                s_amount_total += s_amount_subtotal + s_amount_vat

                    for profile, profile_price in profiles_price.iteritems():
                        amount_subtotal += profile_price - (profile_price * ar_record.Client.M_Discount /100)
                        amount_vat = amount_subtotal * profiles_VAT[profile] / 100
                        amount_total += (profile_price - (profile_price * ar_record.Client.M_Discount /100)) + amount_vat

                    ar_record.write({"Total": (amount_total + s_amount_total)})
                else:
                    ar_record.write({"Discount": 0.0, "Subtotal": 0.0, "VAT": 0.0, "Total":0.0})
            res = super(ARInvoice,self).write(values)
            ar_object.write({'ar_invoice_id': self.id})
            return res
        else:
            res = super(ARInvoice,self).write(values)
            return res

    def workflow_script_closed(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids,{
            'state': 'closed'
        },context)
        return True

    def workflow_script_publish(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids,{
            'state': 'published',
            'published_date': datetime.datetime.now()
        },context)
        return True

    @api.multi
    def action_email_ar_invoice(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        email_receivers = []
        # for email in self.client_id.email:
        #     email_receivers.append(email.name)

        for invoice_email in self.client_id.invoice_email:
            email_receivers.append(invoice_email.name)
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('olims', 'ar_invoice_email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self._context)
        ctx.update({
            'default_model': 'olims.ar_invoice',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'send_email': ",".join(email_receivers)
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
    @api.depends("adjust_percent","adjust_amount","total")
    def update_total_adjusted(self):
        for record in self:
            if record.adjust_percent and record.adjust_amount:
                record.adjusted_total = record.total - (record.total * record.adjust_percent / 100)
                record.adjusted_total = record.adjusted_total + record.adjust_amount
            elif record.adjust_percent and not record.adjust_amount:
                record.adjusted_total = record.total - (record.total * record.adjust_percent / 100)
            elif not record.adjust_percent and record.adjust_amount:
                record.adjusted_total = record.total + record.adjust_amount
            else:
                pass

    def workflow_script_cancelled(self,cr,uid,ids,context=None):
        for record in self.browse(cr,uid,ids,context):
            for ar_obj in record.analysis_request_id:
                ar_obj.write({'ar_invoice_id': False})
        self.write(cr, uid, ids,{
            'state': 'cancelled'
        },context)
        return True

Invoice.initialze(schema)