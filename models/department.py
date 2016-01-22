"""Department - the department in the laboratory.
"""

from openerp import fields, models
from openerp.tools.translate import _
from fields.string_field import StringField
from fields.reference_field import ReferenceField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, TextAreaWidget, ReferenceWidget
from base_olims_model import BaseOLiMSModel

schema = (
    StringField('Department',
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

    fields.Many2one(string='Manager',
           comodel_name='olims.lab_contact',
           required=True,
    ),

    fields.Char('ManagerPhone',
        compute = "ComputeManagerData",
    ),
    fields.Char('ManagerEmail',
        compute = "ComputeManagerData",
    ),
)

class Department(models.Model, BaseOLiMSModel):
    _name = 'olims.department'
    _rec_name = 'Department'

    def ComputeManagerData(self):
        for record in self:
            record.ManagerPhone = record.Manager.Phone
            record.ManagerEmail = record.Manager.EmailAddress
            
        
    def getManager_fulname(self):
        for record in self:
            record.ManagerName = record.getManager()  

Department.initialze(schema)
