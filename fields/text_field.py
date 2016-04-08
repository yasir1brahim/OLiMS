from openerp import fields
from fields_utils import boolean_value_based_mapper, direct_mapper

class TextField(fields.Text):
#    type = 'text' will auto inherit from the base class of Text
        
    def __bika_2_odoo_attrs_mapping(self):
        boolean_value_based_mapper(self, 'required', 1, 'required', True, False)
        boolean_value_based_mapper(self, 'searchable', 1, 'search', True, False)
        direct_mapper(self, 'description', 'help')
        
    def _setup_regular_base(self, model):
        super(TextField, self)._setup_regular_base(model)
        
        self.__bika_2_odoo_attrs_mapping()

        
    pass