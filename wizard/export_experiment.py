from cStringIO import StringIO
import csv
import json
import logging
from openerp import fields
from openerp.osv import osv
from openerp.tools.translate import _


_logger = logging.getLogger(__name__)

def generate_csv(self, ids, model, token=None, domain=[]):

    data ={
           "model": model,
           "fields":[
                       {"name":"id","label":"External ID"},
                       {"name":"attachment_ids/id","label":"Attachments"},
                       {"name":"create_uid/id","label":"Created by"},
                       {"name":"create_date","label":"Created on"},
                       {"name":"database_ids/id","label":"Database"},
                       {"name":"exp_date","label":"Date"},
                       {"name":"description","label":"Description"},
                       {"name":"write_uid/id","label":"Last Updated by"},
                       {"name":"write_date","label":"Last Updated on"},
                       {"name":"exp_status/id","label":"Status"},
                       {"name":"tag_ids/id","label":"Tags"},
                       {"name":"template_id/id","label":"Template"},
                       {"name":"exp_title","label":"Title"},
                       {"name":"status_visibility","label":"Visibility"}
                       ],
            "ids":ids,
            "domain":domain,
            "context":{"lang":"en_US",
                       "tz":False,
                       "uid":1,
                       "params":{
                                 "action":79,
                                 "page":0,
#                                  "limit":80,
                                 "view_type":"list",
                                 "model": model,
                                 "_push_me":False
                                 }
                       },
            "import_compat":True
            }
        
    return {
             'type' : 'ir.actions.act_url',
             'url': '/web/export/csv?data=' + json.dumps(data) + '&token=' + str(None),
             'target': 'self'
        }

class experiment_export(osv.osv_memory):
    _name = "labpal.experiment_export"
    _description = "Labpal Export Experiment"

    start_date = fields.Datetime('Start Date', help='Start date for generating report (requested delivery date)')
    end_date = fields.Datetime('End Date', help='End date for generating report (requested delivery date)')
    export_type = fields.Selection([('all', 'All Records'), ('range', 'From Range')], default='all')
 
    @property
    def content_type(self):
        return 'text/csv;charset=utf8'
    
    def from_data(self, fields, rows):
        fp = StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)

        writer.writerow([name.encode('utf-8') for name in fields])

        for data in rows:
            row = []
            for d in data:
                if isinstance(d, unicode):
                    try:
                        d = d.encode('utf-8')
                    except UnicodeError:
                        pass
                if d is False: d = None
                row.append(d)
            writer.writerow(row)
        
        fp.seek(0)
        data = fp.read()
        fp.close()
        return data

    def filename(self, base):
        return base + '.csv'
    
    def export_excel(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['start_date', 'end_date', 'export_type'])[0]

        context = dict(context or {})
        
        if data['export_type'] == 'all':
            ids = False
        else:
            start_date = data['start_date'] 
            end_date = data['end_date'] 
            ids = self.pool.get('labpal.experiment').search(cr, uid, [('create_date', '>=', start_date), ('create_date', '<=', end_date)])
        
        return generate_csv(self, ids, model="labpal.experiment")
