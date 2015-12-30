from openerp import api, fields, models, _


class OlimsCommonReport(models.TransientModel):
    _name = "olims.common_report"
    _description = "OLiMS Common Report"

    date_from = fields.Datetime(string='From')
    date_to = fields.Datetime(string='to')
    
    def _build_contexts(self, data):
        result = {}
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        return result

    def _print_report(self, data):
        raise (_('Error!'), _('Not implemented.'))

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        self._print_report(data)
        return self._print_report(data)