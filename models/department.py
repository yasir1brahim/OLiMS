"""Department - the department in the laboratory.
"""
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import *
# from dependencies.dependency import HoldingReference
# from lims.content.bikaschema import BikaSchema
# from dependencies.dependency import ClassSecurityInfo
# from lims.utils import t
# from dependencies.dependency import implements

import logging

from openerp import fields, models,osv

_logger = logging.getLogger(__name__)

import sys
from lims import bikaMessageFactory as _
from dependencies.dependency import getToolByName
from lims.config import PROJECTNAME
# from dependencies.fields import StringField, TextField, ReferenceField
from fields.string_field import StringField
from fields.reference_field import ReferenceField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, TextAreaWidget, ReferenceWidget
from base_olims_model import BaseOLiMSModel

# schema = BikaSchema.copy() + Schema(
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
#         vocabulary = 'getContacts',
#         vocabulary_display_path_bound = sys.maxint,
#         allowed_types = ('LabContact',),
# #         referenceClass = HoldingReference,
#         relationship = 'DepartmentLabContact',
#         widget = ReferenceWidget(
#             checkbox_bound = 0,
#             label=_("Manager"),
#             description = _(
#                 "Select a manager from the available personnel configured under the "
#                 "'lab contacts' setup item. Departmental managers are referenced on "
#                 "analysis results reports containing analyses by their department."),
#         ),
    ),

#    fields.Char(compute='getManager_fulname', string='ManagerName'),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('ManagerName',
#         expression = "context.getManager() and context.getManager().getFullname() or ''",
#         widget = ComputedWidget(
#             visible = False,
#         ),
#     ),

    fields.Char('ManagerPhone',
        compute = "ComputeManagerData",
#         widget = ComputedWidget(
#             visible = False,
#         ),
    ),
    fields.Char('ManagerEmail',
        compute = "ComputeManagerData",
#         widget = ComputedWidget(
#             visible = False,
#         ),
    ),
)#)

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# schema['description'].widget.visible = True
# schema['description'].schemata = 'default'


class Department(models.Model, BaseOLiMSModel):
    _name = 'olims.department'
    _rec_name = 'Department'
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
#     security = ClassSecurityInfo()
#     displayContentsTab = False
#     schema = schema

    def ComputeManagerData(self):
        for record in self:
            record.ManagerPhone = record.Manager.Phone
            record.ManagerEmail = record.Manager.EmailAddress
            
    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)
        
    def getManager_fulname(self):
        for record in self:
            record.ManagerName = record.getManager()  

Department.initialze(schema)
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# registerType(Department, PROJECTNAME)
