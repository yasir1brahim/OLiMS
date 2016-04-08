from openerp import fields

from fields_utils import direct_mapper

class BooleanField(fields.Boolean):
#    type = 'bool' will auto inherit from the base class of Boolean
        
    def __bika_2_odoo_attrs_mapping(self):
        direct_mapper(self, 'description', 'help')
        
    def _setup_regular_base(self, model):
        super(BooleanField, self)._setup_regular_base(model)
        self.__bika_2_odoo_attrs_mapping()
        
    pass