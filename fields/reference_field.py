from openerp import fields

from fields_utils import boolean_value_based_mapper

class ReferenceField(fields.Reference):
    """ type = 'reference' will auto inherit from the base class of Reference """
        
    def __bika_2_odoo_attrs_mapping(self):
        boolean_value_based_mapper(self, 'required', 1, 'required', True, False)

        
    def _setup_regular_base(self, model):
        super(ReferenceField, self)._setup_regular_base(model)
        
        self.__bika_2_odoo_attrs_mapping()
        
    pass