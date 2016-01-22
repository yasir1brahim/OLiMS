from lims import bikaMessageFactory as _
from fields.string_field import StringField

from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, DecimalWidget, TextAreaWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (StringField('Title',
        required=1,
        widget=StringWidget(
            label=_('Title'),
            description=_('Title is required.'),
        ),
    ),
    TextField('Description',
        widget=TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    StringField('Volume',
        widget = StringWidget(
            label=_("Volume"),
        )
    ),
    StringField('Unit',
        widget = StringWidget(
            label=_("Unit"),
        )
    ),
    FixedPointField('VAT',
        default=14.00,
        default_method = 'getDefaultVAT',
        widget = DecimalWidget(
            label=_("VAT %"),
            description=_("Enter percentage value eg. 14.0"),
        ),
    ),
    FixedPointField('Price',
        required=1,
        widget = DecimalWidget(
            label=_("Price excluding VAT"),
        )
    ),

    fields.Float(string='TotalPrice',
        compute = '_ComputeTotalPrice',
    ),
)

class LabProduct(models.Model, BaseOLiMSModel):
    _name ='olims.lab_product'
    _rec_name = 'Title'


    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)
    
    def _ComputeTotalPrice(self):
        """ compute total price """
        for items in self:
            price = items.getPrice()
            price = (price or 0.00)
            vat = (items.getVAT())
            price = price and price or 0
            vat = vat and vat or 0
            price = price + vat
            items.TotalPrice = price

    def getDefaultVAT(self):
        """ return default VAT from bika_setup """
        try:
            vat = self.bika_setup.getVAT()
            return vat
        except ValueError:
            return "0.00"

    #security.declarePublic('getVATAmount')
    def computeVATAmount(self):
        """ Compute VATAmount
        """
        for record in self:
            try:
                vatamount = record.getTotalPrice() - record.getPrice()
            except:
                vatamount = 0
            record.VATAmount= vatamount


LabProduct.initialze(schema)