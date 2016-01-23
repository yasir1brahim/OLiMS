from openerp.tools.translate import _
from fields.string_field import StringField

from fields.file_field import FileField
from fields.widget.widget import StringWidget, FileWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (
             FileField('ReportFile',
            widget = FileWidget(
            label=_("Report"),
        ),
    ),
    StringField('ReportType',
        widget = StringWidget(
            label=_("Report Type"),
            description=_("Report type"),
        ),
    ),

    fields.Many2one(string='Client',
                   comodel_name='olims.client',
                    ),

)


class Report(models.Model, BaseOLiMSModel):
    _name ='olims.report'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def current_date(self):
        """ return current date """
        return DateTime()


Report.initialze(schema)