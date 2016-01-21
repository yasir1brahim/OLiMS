from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.boolean_field import BooleanField
from fields.reference_field import ReferenceField
from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.widget.widget import DecimalWidget, BooleanWidget, TextAreaWidget, ReferenceWidget
from lims import bikaMessageFactory as _
BULK_DISCOUNT_OPTION =(
                           ('yes', _('Yes')),
                           ('no', _('NO')),
                           )

PRICELIST_TYPES = (
    ('AnalysisService', _('Analysis Services')),
    ('LabProduct', _('Lab Products')),
)
schema = (StringField('Title',
              required=1,        
        ),
    fields.Selection(string='Type',
           selection=PRICELIST_TYPES,
           default='AnalysisService',
           required=True,
    ),


    fields.Selection(string='BulkDiscount',
        selection=BULK_DISCOUNT_OPTION
    ),
    FixedPointField('BulkPrice',
        widget=DecimalWidget(
            label=_("Discount %"),
            description=_("Enter discount percentage value"),
        ),
    ),
    BooleanField('Descriptions',
        default=False,
        widget=BooleanWidget(
            label=_("Include descriptions"),
            description=_("Select if the descriptions should be included"),
        ),
    ),
    DateTimeField('ExpirationDate'),
    DateTimeField('EffectiveDate'),
)

def apply_discount(price=None, discount=None):
    return float(price) - (float(price) * float(discount)) / 100


def get_vat_amount(price, vat_perc):
    return float(price) * float(vat_perc) / 100


class Pricelist(models.Model, BaseOLiMSModel):
    _name= 'olims.price_list'
    _rec_name = 'Title'

Pricelist.initialze(schema)

def ObjectModifiedEventHandler(instance, event):
    """ Various types need automation on edit.
    """
    if not hasattr(instance, 'portal_type'):
        return

    if instance.portal_type == 'Pricelist':
        """ Create price list line items
        """
        # Remove existing line items
        instance.pricelist_lineitems = []
        for p in instance.portal_catalog(portal_type=instance.getType(),
                                         inactive_state="active"):
            obj = p.getObject()
            itemDescription = None
            itemAccredited = False
            if instance.getType() == "LabProduct":
                print_detail = ""
                if obj.getVolume():
                    print_detail = print_detail + str(obj.getVolume())
                if obj.getUnit():
                    print_detail = print_detail + str(obj.getUnit())
                if obj.getVolume() or obj.getUnit():
                    print_detail = " (" + print_detail + ")"
                    itemTitle = obj.Title() + print_detail
                else:
                    itemTitle = obj.Title()
                cat = None
                if obj.getPrice():
                    price = float(obj.getPrice())
                    totalprice = float(obj.getTotalPrice())
                    vat = totalprice - price
                else:
                    price = 0
                    totalprice = 0
                    vat = 0
            elif instance.getType() == "AnalysisService":
                #
                if str(obj.getUnit()):
                    print_detail = " (" + str(obj.getUnit()) + ")"
                    itemTitle = obj.Title() + print_detail
                else:
                    itemTitle = obj.Title()
                itemAccredited = obj.getAccredited()
                #
                cat = obj.getCategoryTitle()
                if instance.getBulkDiscount():
                        price = float(obj.getBulkPrice())
                        vat = get_vat_amount(price, obj.getVAT())
                        totalprice = price + vat
                else:
                    if instance.getBulkPrice():
                        discount = instance.getBulkPrice()
                        price = float(obj.getPrice())
                        price = apply_discount(price, discount)
                        vat = get_vat_amount(price, obj.getVAT())
                        totalprice = price + vat
                    elif obj.getPrice():
                        price = float(obj.getPrice())
                        vat = get_vat_amount(price, obj.getVAT())
                        totalprice = price + vat
                    else:
                        totalprice = 0
                        price = 0
                        vat = 0

            if instance.getDescriptions():
                itemDescription = obj.Description()

            li = PricelistLineItem()
            li['title'] = itemTitle
            li['ItemDescription'] = itemDescription
            li['CategoryTitle'] = cat
            li['Accredited'] = itemAccredited
            li['Subtotal'] = "%0.2f" % price
            li['VATAmount'] = "%0.2f" % vat
            li['Total'] = "%0.2f" % totalprice
            instance.pricelist_lineitems.append(li)
