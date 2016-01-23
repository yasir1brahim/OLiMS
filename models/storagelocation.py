from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, TextAreaWidget
from openerp.tools.translate import _

schema =(StringField('Storage Location',
        required=1,
        widget=StringWidget(
            label=_('Address'),
            description=_('Title is required.'),
        ),
    ),
    TextField('Description',
        widget=TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    StringField('Site Title',
        widget=StringWidget(
            label=_("Site Title"),
            description=_("Title of the site"),
        ),
    ),
    StringField('Site Code',
        widget=StringWidget(
            label=_("Site Code"),
            description=_("Code for the site"),
        ),
    ),
    StringField('SiteDescription',
        widget=StringWidget(
            label=_("Site Description"),
            description=_("Description of the site"),
        ),
    ),
    StringField('Location Title',
        widget=StringWidget(
            label=_("Location Title"),
            description=_("Title of location"),
        ),
    ),
    StringField('Location Code',
        widget=StringWidget(
            label=_("Location Code"),
            description=_("Code for the location"),
        ),
    ),
    StringField('LocationDescription',
        widget=StringWidget(
            label=_("Location Description"),
            description=_("Description of the location"),
        ),
    ),
    StringField('LocationType',
        widget=StringWidget(
            label=_("Location Type"),
            description=_("Type of location"),
        ),
    ),
    StringField('Shelf Title',
        widget=StringWidget(
            label=_("Shelf Title"),
            description=_("Title of the shelf"),
        ),
    ),
    StringField('Shelf Code',
        widget=StringWidget(
            label=_("Shelf Code"),
            description=_("Code the the shelf"),
        ),
    ),
    StringField('ShelfDescription',
        widget=StringWidget(
            label=_("Shelf Description"),
            description=_("Description of the shelf"),
        ),
    ),
)


class StorageLocation(models.Model, BaseOLiMSModel):
    _name='olims.storage_location'
    _rec_name = 'Storage Location'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        return safe_unicode(self.getField('title').get(self)).encode('utf-8')


StorageLocation.initialze(schema)