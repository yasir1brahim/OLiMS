from openerp import fields

class DateTimeField(fields.Datetime):
#    type = 'datetime' will auto inherit from the base class of Datetime
        
    def _setup_regular_base(self, model):
        super(DateTimeField, self)._setup_regular_base(model)
        
    pass