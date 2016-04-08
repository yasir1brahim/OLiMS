from openerp import fields
from fields_utils import direct_mapper, boolean_value_based_mapper

class FixedPointField(fields.Float):
#    type = 'float' will auto inherit from the base class of Float
        
    def __bika_2_odoo_attrs_mapping(self):
        
#         string_to_float_mapper(self, 'default')
        direct_mapper(self, 'description', 'help')
        boolean_value_based_mapper(self, 'required', 1, 'required', True, False)
        
        
    def _setup_regular_base(self, model):
        super(FixedPointField, self)._setup_regular_base(model)
        self.__bika_2_odoo_attrs_mapping()
        
    pass