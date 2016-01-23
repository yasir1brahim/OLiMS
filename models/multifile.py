from openerp.tools.translate import _
from fields.string_field import StringField
from fields.file_field import FileField
from fields.widget.widget import StringWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (
    StringField('DocumentID',
    required=1,
    validators=('uniquefieldvalidator',),
    widget = StringWidget(
        label=_("Document ID"),
        )
    ),
    FileField('File',
    required=1,
    ),

    StringField('DocumentVersion',
    widget = StringWidget(
        label=_("Document Version"),
        )
    ),

    StringField('DocumentLocation',
    widget = StringWidget(
        label=_("Document Location"),
        description=_("Location where the document set is shelved"),
        )
    ),

    StringField('DocumentType',
    required=1,
    widget = StringWidget(
        label=_("Document Type"),
        description=_("Type of document (e.g. user manual, instrument specifications, image, ...)"),
        )
    ),
    fields.Many2one(string='Instrument',
                   comodel_name='olims.instrument',
                   required = False,
    )
)


class Multifile(models.Model, BaseOLiMSModel): #BaseContent
    _name = 'olims.multifile'

Multifile.initialze(schema)