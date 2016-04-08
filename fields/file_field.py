from openerp import fields
from fields_utils import direct_mapper

class FileField(fields.Binary):
#    type = 'binary' will auto inherit from the base class of Binary
        
    def __bika_2_odoo_attrs_mapping(self):
        direct_mapper(self, 'description', 'help')
        
    def _setup_regular_base(self, model):
        super(FileField, self)._setup_regular_base(model)
        
        self.__bika_2_odoo_attrs_mapping()
        
    pass