"""InvoiceBatch is a container for Invoice instances.
"""

from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.date_time_field import DateTimeField
from fields.widget.widget import DateTimeWidget
from openerp.tools.translate import _

schema = (
    DateTimeField('BatchStartDate',
        required=1,
        default_method='current_date',
        widget=DateTimeWidget(
            label=_("Start Date"),
        ),
    ),
    DateTimeField('BatchEndDate',
        required=1,
        default_method='current_date',
        widget=DateTimeWidget(
            label=_("End Date"),
        ),
    ),
)


class InvoiceBatch(models.Model, BaseOLiMSModel):
    _name='olims.invoicebatch'


InvoiceBatch.initialze(schema)
