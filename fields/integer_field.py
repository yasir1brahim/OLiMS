from openerp import fields
import logging

class IntegerField(fields.Integer):
#    type = 'integer' will auto inherit from the base class of Integer
        
    def _setup_regular_base(self, model):
        super(IntegerField, self)._setup_regular_base(model)
        
    pass