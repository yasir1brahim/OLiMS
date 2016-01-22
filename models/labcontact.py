"""The lab staff
"""
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.file_field import FileField
from fields.widget.widget import StringWidget, FileWidget
from openerp import fields, models, api

from dependencies.dependency import DisplayList
from dependencies.dependency import safe_unicode
from lims import PMF, bikaMessageFactory as _

PUBLICATION_PREFS = (
    ('email', _('Email')),
    ('pdf', _('PDF')))
schema =  (
        StringField('Salutation',
        widget = StringWidget(
            label = _("Salutation",
                      "Title"),
            description=_("Greeting title eg. Mr, Mrs, Dr"),
        ),
    ),
    StringField('Firstname',
        required = 1,
        widget = StringWidget(
            label=_("Firstname"),
        ),
    ),
    StringField('Middleinitial',
        required = 0,
        widget = StringWidget(
            label=_("Middle initial"),
        ),
    ),
    StringField('Middlename',
        required = 0,
        widget = StringWidget(
            label=_("Middle name"),
        ),
    ),
    StringField('Surname',
        required = 1,
        widget = StringWidget(
            label=_("Surname"),
        ),
    ),
    
    fields.Char(compute='computeFulname', string='Name'),
    StringField('Username',
        widget = StringWidget(
            visible = False
        ),
    ),
    StringField('EmailAddress',
        schemata = 'Email Telephone Fax',
        searchable = 1,
        widget = StringWidget(
            label=_("Email Address"),
        ),
    ),
    StringField('Phone',
        schemata = 'Email Telephone Fax',
        widget = StringWidget(
            label=_("Phone (business)"),
        ),
    ),
    StringField('Fax',
        schemata = 'Email Telephone Fax',
        widget = StringWidget(
            label=_("Fax (business)"),
        ),
    ),
    StringField('HomePhone',
        schemata = 'Email Telephone Fax',
        widget = StringWidget(
            label=_("Phone (home)"),
        ),
    ),
    StringField('Mobile Phone',
        schemata = 'Email Telephone Fax',
        widget = StringWidget(
            label=_("Phone (mobile)"),
        ),
    ),
    StringField('JobTitle',
        widget = StringWidget(
            label=_("Job title"),
        ),
    ),
           
           
                 # # ~~~~~~~~~~ PhysicalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='physical_country'),
    fields.Many2one(comodel_name='olims.state',string='physical_state', domain="[('Country', '=', physical_country)]"),
    fields.Many2one(comodel_name='olims.district',string='physical_district', domain="[('State', '=', physical_state)]"),
    fields.Char(string='physical_city'),
    fields.Char(string='physical_postalcode'),
    fields.Char(string='physical_address'),
    fields.Selection([('postal', 'Postal Address')],string='physical_copy_from'),
          
        # # ~~~~~~~~~~ PostalAddress behavior in Odoo is as selection field ~~~~~~~~~~~
    fields.Many2one(comodel_name='olims.country',string='postal_country'),
    fields.Many2one(comodel_name='olims.state',string='postal_state', domain="[('Country', '=', postal_country)]"),
    fields.Many2one(comodel_name='olims.district',string='postal_district', domain="[('State', '=', postal_state)]"),
    fields.Char(string='postal_city'),
    fields.Char(string='postal_postalcode'),
    fields.Char(string='postal_address'),
    fields.Selection([('physical', 'Physical Address')],string='postal_copy_from'),
    
    fields.Selection(string='PublicationPreference',
                   selection=PUBLICATION_PREFS,
                   default = 'email',
   ),
    
    FileField('Signature',
              help="Upload a scanned signature to be used on printed analysis results reports."+
               "Ideal size is 250 pixels wide by 150 high",
               widget = FileWidget(
               label = _("Signature"),
        ),
    ),
    
    fields.Many2one(string='Department',
                       comodel_name='olims.department',
        ),

    fields.Many2one(comodel_name='res.users',string='user',domain="[('id', '=', '-1')]"),
)

class LabContact(models.Model, BaseOLiMSModel): #Person
    _name = 'olims.lab_contact'
    _rec_name = 'Name'

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)
    
    def computeFulname(self):
        """ return Person's Fullname """
        for record in self:
        
            fn = record.getFirstname()
            mi = record.getMiddleinitial()
            md = record.getMiddlename()
            sn = record.getSurname()
            fullname = ''
             
            if fn or sn:
                if mi and md:
                    fullname = '%s %s %s %s' % (record.getFirstname(),
                                            record.getMiddleinitial(),
                                            record.getMiddlename(),
                                            record.getSurname())
                elif mi:
                    fullname = '%s %s %s' % (record.getFirstname(),
                                            record.getMiddleinitial(),
                                            record.getSurname())
                elif md:
                    fullname = '%s %s %s' % (record.getFirstname(),
                                            record.getMiddlename(),
                                            record.getSurname())
                else:
                    fullname = '%s %s' % (record.getFirstname(), record.getSurname())
            record.Name = fullname.strip()
    

    def Title(self):
        """ Return the contact's Fullname as title """
        return safe_unicode(self.getname()).encode('utf-8')

    def hasUser(self):
        """ check if contact has user """
        return self.portal_membership.getMemberById(
            self.getUsername()) is not None

    def getDepartments(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [('','')] + [(o.UID, o.Title) for o in
                               bsc(portal_type='Department',
                                   inactive_state = 'active')]
        o = self.getDepartment()
        if o and o.UID() not in [i[0] for i in items]:
            items.append((o.UID(), o.Title()))
        items.sort(lambda x,y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    @api.onchange('physical_copy_from')
    def _onchange_physical(self):
        # set auto-changing field
        if self.physical_copy_from:
            setattr(self, 'physical_country', getattr(self,self.physical_copy_from+'_country'))
            setattr(self, 'physical_state', getattr(self,self.physical_copy_from+'_state'))
            setattr(self, 'physical_district', getattr(self,self.physical_copy_from+'_district'))
            setattr(self, 'physical_city', getattr(self,self.physical_copy_from+'_city'))
            setattr(self, 'physical_postalcode', getattr(self,self.physical_copy_from+'_postalcode'))
            setattr(self, 'physical_address', getattr(self,self.physical_copy_from+'_address'))

    @api.onchange('postal_copy_from')
    def _onchange_postal(self):
        # set auto-changing field
        if self.postal_copy_from:
            setattr(self, 'postal_country', getattr(self,self.postal_copy_from+'_country'))
            setattr(self, 'postal_state', getattr(self,self.postal_copy_from+'_state'))
            setattr(self, 'postal_district', getattr(self,self.postal_copy_from+'_district'))
            setattr(self, 'postal_city', getattr(self,self.postal_copy_from+'_city'))
            setattr(self, 'postal_postalcode', getattr(self,self.postal_copy_from+'_postalcode'))
            setattr(self, 'postal_address', getattr(self,self.postal_copy_from+'_address'))


LabContact.initialze(schema)