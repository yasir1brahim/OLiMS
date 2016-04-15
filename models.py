# -*- coding: utf-8 -*-

import datetime
import base64
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.osv import osv
import sys
import psycopg2
from openerp.report import report_sxw
import logging
import re
import time
import os
import webbrowser
from os.path import expanduser
import subprocess
import unicodedata
from HTMLParser import HTMLParser
#import Tkinter as tk
#import tkFileDialog as filedialog
import shutil
import tempfile
import StringIO
import csv
from openerp import http
from openerp.http import request
import openerp
from openerp import SUPERUSER_ID
import json
import gzip
import zipfile
from zipfile import ZipFile
import zlib



#from openerp.http import request


AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Very Low'),
    ('2', 'Low'),
    ('3', 'Medium'),
    ('4', 'High'),
    ('5', 'Very High'),
    ]


class Labpal_Mail(models.Model):

    _name = 'labpal.mail'
    email_From = fields.Char('Description')


class MLStripper(HTMLParser):
    print "MLSSS"
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class Experiment(models.Model):

    _name = 'labpal.experiment'
    _inherit = 'mail.thread'
    
    # _inherit = 'mail.compose.message'
    #_inherit = 'mail.compose.message'

    tag_ids = fields.Many2many('labpal.tag',
                              'experiment_tag_rel',
                              'experiment_id', 'tag_id',
                              string='Tags',
                              domain="[('id', '=', '-1')]")
    exp_date = fields.Date('Date')
    status_visibility = fields.Selection(string='Visibility',selection=[
    	('everyone','Everyone with an account'),
    	('team','Only the team'),
    	('me','Only me'),
    	])
    exp_title = fields.Char('Title')
    description = fields.Text()
    attachment_ids = fields.Many2many(
        'ir.attachment', 'experiment_attachment_rel',
        'experiment_id', 'attachment_id',
        string='Attachments',
        help='Attachments are linked to a document through model / res_id and to the Experiment'
             'through this field.')
    exp_status = fields.Many2one(string='Status', comodel_name='labpal.status')
    database_ids = fields.Many2many('labpal.database', 'experiment_database_rel',
                                    string='Database')
    template_id = fields.Many2one('labpal.template',
                                  string='Template')





    @api.multi
    def csv_http(self):


        data ={
           "model": 'labpal.experiment',
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
            "ids":self.id,
            "domain":[],
            "context":{"lang":"en_US",
                       "tz":False,
                       "uid":1,
                       "params":{
                                 "action":79,
                                 "page":0,
#                                  "limit":80,
                                 "view_type":"list",
                                 "model": 'labpal.experiment',
                                 "_push_me":False
                                 }
                       },
            "import_compat":True
            }

        print "GENERATING CSV"
    
        d = json.dumps(data)
        print "d ====", d 
        # print  '/web/export/csv?data=' + json.dumps(data) + '&token=' + str(None)
        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/export/csv?data=' + json.dumps(data) + '&token=' + str(None),
             # 'url': '/web/application/zip?data=' + json.dumps(data) + '&token=' + str(None),
             'target': 'self'
        }
  

    @api.multi
    def get_csv_db(self):

        pass

    @api.multi
    def get_pdf_exp(self):
        
        #fetch the qweb-pdf file

        return self.env['report'].get_action(self, 'labpal.pdf_template')

    @api.multi    
    def get_pdf_db(self):
        #self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'labpal.pdf_db_template')    

    @api.model
    def _get_default_status(self):
        res = self.env['labpal.status'].search([('default_status','=',True)])
        if res:
            return res[0] 
        else:
            False
    _defaults = {
     'exp_status':_get_default_status,
     }

    @api.multi
    def file_compression_old(self):

        file_csv_location = tempfile.gettempdir()
        source = os.path.join(file_csv_location, 'TESTING/')

        # shutil.make_archive('destination','zip','source')

        


    @api.multi
    def file_compression(self):

        data ={
           "model": 'labpal.experiment',
           "fields":[
                       {"name":"id","label":"External ID"},
                       # {"name":"attachment_ids/id","label":"Attachments"},
                       # {"name":"create_uid/id","label":"Created by"},
                       # {"name":"create_date","label":"Created on"},
                       # {"name":"database_ids/id","label":"Database"},
                       # {"name":"exp_date","label":"Date"},
                       # {"name":"description","label":"Description"},
                       # {"name":"write_uid/id","label":"Last Updated by"},
                       # {"name":"write_date","label":"Last Updated on"},
                       # {"name":"exp_status/id","label":"Status"},
                       # {"name":"tag_ids/id","label":"Tags"},
                       # {"name":"template_id/id","label":"Template"},
                       {"name":"exp_title","label":"Title"},
                       # {"name":"status_visibility","label":"Visibility"}
                       ],
            "ids":self.id,
            "domain":[],
            "context":{"lang":"en_US",
                       "tz":False,
                       "uid":1,
                       "params":{
                                 "action":79,
                                 "page":0,
#                                  "limit":80,
                                 "view_type":"list",
                                 "model": 'labpal.experiment',
                                 "_push_me":False
                                 }
                       },
            "import_compat":True
            }

        #getting experiment csv 
        csv_file = StringIO.StringIO()
        # data = data['fields'][0:]

        content = json.dumps(data)
        print "content === ", content

        writer = csv.writer(csv_file)
        writer.writerows(content)

        #compressing the StringIO csv object

        # zip_archive = zipfile.ZipFile(csv_file,'w')
        # zip_archive.writestr('labpal_test.csv',csv_file.getvalue())
        # zip_archive.close()

        #compressing the qweb-pdf file

        file = self.env['report'].get_action(self, 'labpal.pdf_template')
        # zip_archive_pdf = zipfile.ZipFile(file,'w')
        # zip_archive_pdf.write()

        zip = zipfile.ZipFile('THE_FOLDER_.zip','a')
        zip.writestr('odoo.csv',csv_file.getvalue())
        # zip.write('/home/developer06/Desktop/Test_LP.pdf')

        ir_actions_report = self.pool.get('ir.actions.report.xml')

        report_obj = self.env['report']

        report_in = report_obj._get_report_from_name('labpal.pdf_template')

        print "GET REPORT ==== ", report_in

        datas = {}
        matching_reports = ir_actions_report.search(
            self.env.cr,self.env.uid, [('name', '=', 'Download as a pdf file')])
        matching_reports = matching_reports[1]
        print "matching_reports", matching_reports
    
        if matching_reports:
            report = ir_actions_report.browse(self.env.cr, self.env.uid, matching_reports)

            print "report_to ==== ", report
            report_service = 'report.' + report.report_name
            # service = netsvc.LocalService(report_service)
            result, format = openerp.report.render_report(self.env.cr, self.env.uid,[1],'labpal.pdf_template',datas,{})
            result = base64.b64encode(result)
            file_name = "odooo.pdf"

            print "result ==== ", result

        # attachment_id = attachment_obj.create(cr, uid,
        #             {
        #                 'name': file_name,
        #                 'datas': result,
        #                 'datas_fname': file_name,
        #                 'res_model': self._name,
        #                 'res_id': record.id,
        #                 'type': 'binary'
        #             }, context=context)

        zip.write(file)


        zip.close()


        #getting experiment pdf
        # with open('/home/developer06/Desktop/LABPAL_TEST.zip','w+') as f:
        #     f.write(csv_file.getvalue())

        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/export/csv?data=' + json.dumps(data) + '&token=' + str(None),
             'target': 'self'
        }

        

        



    @api.multi
    def get_zip_test(self):


        file_csv = tempfile.gettempdir()

        query_desc = "SELECT description FROM labpal_experiment where id="+ str(self.id) + ""


        join_q = "SELECT tag_id FROM experiment_tag_rel where experiment_id="+ str(self.id) + ""
        conn = psycopg2.connect("dbname = 'labpal-odoo' user = 'admin' host = 'localhost' password = 'knysys'")
        cur = conn.cursor()

        cur.execute(join_q)
        tagid = cur.fetchone()
        tagid = str(tagid[0])

        query = "select t1.exp_title,t1.exp_date,t2.name,t1.description from labpal_experiment t1,labpal_tag t2 where t1.id="+str(self.id)+" and t2.id ="+ tagid+""

        cur.execute(query_desc)

        result = cur.fetchone()

        result = "'"+result[0]+"'"
        
        s = MLStripper()
        s.feed(result)
        result = s.get_data()

        result = result.replace('/n','')

        update_query = "UPDATE labpal_experiment SET description="+result+" WHERE id="+str(self.id)+""  

        cur.execute(update_query)
        conn.commit()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)


        
        
        with open('test.csv', 'w+') as f:
                cur.copy_expert(outputquery , f)
                #cur.copy_expert(outputquery, f)
        conn.close()
        
        # filename = filedialog.asksaveasfilename()        
        shutil.make_archive('/home/developer06/Desktop','zip','test.csv')

        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/export/csv?data=' + json.dumps('test.csv') + '&token=' + str(None),
             'target': 'self'
        }

        

    
    @api.multi
    def test_form(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''


        print "IN test FORM"
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('labpal', 'labpal_send_report_mail_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'labpal.experiment',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        print "ENVIRONMENT",self.env['labpal.experiment']
        print "SELF", self.id
        #print "SELF", self.env['labpal.experiment'].message_get_reply_to([self.id])
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class Status(models.Model):

    _name = 'labpal.status'

    name = fields.Char('Status')
    color = fields.Char(
        string="Color",
        help="Choose your color",
        size=7
    )
    default_status = fields.Boolean('Default Status')
    
class Databases(models.Model):
    _name = 'labpal.database'
    _inherit = 'labpal.experiment'

    _defaults = {'rating': lambda *a: AVAILABLE_PRIORITIES[0][0],
                 }
    rating = fields.Selection(AVAILABLE_PRIORITIES, 'Rating', select=True)
    name = fields.Char('Databases')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'database_attachment_rel',
        'database_id', 'attachment_id',
        string='Attachments',
        help='Attachments are linked to a document through model / res_id and to the Database'
             'through this field.')
    tag_ids = fields.Many2many('labpal.tag',
                              'database_tag_rel',
                              'database_id', 'tag_id',
                              string='Tags',
                              domain="[('id', '=', '-1')]")
    types_of_item_id = fields.Many2one('labpal.types_of_item',
                                         string='Types of Items')

    @api.onchange('types_of_item_id')
    def _onchange_itemtype(self):
        for record in self:
            template = self.env['labpal.types_of_item'].search([('id', '=', record.types_of_item_id.id)])
            form_view = self.env.ref('labpal.database_formedit_view', False)
            if template:
                record.description = template.template

class Tags(models.Model):
    _name = 'labpal.tag'
    _rec_name = 'name'
    name = fields.Char('Tags')

class Templates(models.Model):
    _name = 'labpal.template'
    
    name = fields.Char('Name')
    template  = fields.Text()

class TypesofItems(models.Model):
    _name = 'labpal.types_of_item'

    name = fields.Char('Name')
    template  = fields.Text()
    color = fields.Char(
        string="Color",
        help="Choose your color",
        size=7
    )

class ToDoList(models.Model):
    _name = 'labpal.todolist'
    name = fields.Char('Name')

class FilterDatabase(models.TransientModel):
    _name = 'labpal.filter_database'

    types_of_item_ids = fields.Many2one('labpal.types_of_item',
                                         string='Filter Items')
    order_by = fields.Selection(
                                (
                                 ('types_of_item_id', 'Category'),
                                 ('exp_date', 'Date'),
                                 ('rating', 'Rating'),
                                 ('name','Title')
                                 ),
                                string="Order By",
#                                 default="orderby",
                                select=True)
    sort_by = fields.Selection(
                                (
                                 ('desc', 'DESC'),
                                 ('asc', 'ASC'),
                                 ),
                                string="Sort By",
#                                 default="sortby",
                                select=True
                                )
    status_id = fields.Many2one('labpal.status',
        string='Filter status')

    @api.multi
    def disaplay_filtered_database(self):
        data = self.read()[0]
        ids_list = []
        if data['types_of_item_ids']:
            database_res = self.env['labpal.database'].search([('types_of_item_id',
                                                            '=', data['types_of_item_ids'][0])])
            for ids in database_res:
                ids_list.append(ids.id)
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            'domain' : [('id', 'in', ids_list)]
            }
        else:
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            }
    @api.multi
    def disaplay_filtered_experiment(self):
        data = self.read()[0]
        ids_list = []
        if data['status_id']:
            experiment_res = self.env['labpal.experiment'].search([('exp_status',
                                                            '=', data['status_id'][0])])
            for ids in experiment_res:
                ids_list.append(ids.id)
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.experiment',
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            'domain' : [('id', 'in', ids_list)]
            }
        else:
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.experiment',
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            }

    @api.multi
    def disaplay_ordered_database(self):
        data = self.read()[0]
        ids_list = []
        # kanban_view = self.env.ref('labpal.database_kanban_view', False)
        if data['order_by'] and data['sort_by']:
            sortBy = data['order_by'] + " " + data['sort_by']
            database_res = self.env['labpal.database'].search([], order=sortBy)
            for ids in database_res:
                ids_list.append(ids.id)
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            'domain' : [('id', 'in', ids_list)],
            # 'view_mode': 'kanban',
            # 'view_id': kanban_view.id,
            # 'flags': {'action_buttons': True},
            }
        elif data['order_by']:
            sortBy = data['order_by'] + " " + 'desc'
            database_res = self.env['labpal.database'].search([], order=sortBy)
            for ids in database_res:
                ids_list.append(ids.id)
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            'domain' : [('id', 'in', [ids_list])],
            # 'view_mode': 'kanban',
            # 'view_id': kanban_view.id,
            # 'flags': {'action_buttons': True},
            }
        else:
            return {
            'type': "ir.actions.act_window",
            'res_model': "labpal.database",
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            # 'view_mode': 'tree',
            # 'view_id': kanban_view.id,
            # 'target' : "current"
            }
    @api.multi
    def disaplay_ordered_experiment(self):
        return {
            'type': "ir.actions.act_window",
            'res_model': "labpal.experiment",
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
            }

class SerachModel(models.TransientModel):
    _name = "labpal.serach_model"

    @api.multi
    def _selection_values(self):
        list_of_name = [('experiment','Experiments'),('database','Database')]
        items_types_object = self.env['labpal.types_of_item'].search([])
        for name in items_types_object:
            list_of_name.append((name.name,name.name))
        return list_of_name

    @api.multi
    def _selection_values_createdby(self):
        list_create_uids = [(self.env.uid , 'Yourself')]
        created_by_object = self.env['res.users'].search([('id', '!=', self.env.uid)])
        if created_by_object:
            for name_and_id in created_by_object:
                list_create_uids.append((name_and_id.id,name_and_id.name))
        return list_create_uids

    @api.onchange('search_by_created_uid')
    def _change_search_in_all_value(self):
        for record in self:
            record.search_in_all = False

    search_type = fields.Selection(_selection_values, 'Search in',
        default='experiment',
        required=True)
    tags_id = fields.Many2one('labpal.tag',
                              string='With the tag')
    search_by_created_uid = fields.Selection(_selection_values_createdby, 'Search only in experiments owned by:'
        ,required=True)
    search_in_all = fields.Boolean(string="search in everyone experiments")
    start_date = fields.Date('Where date is between')
    end_date = fields.Date('and')
    contain_title = fields.Char('And title contains')
    status_id = fields.Many2one(string='And status is', comodel_name='labpal.status')
    body_contains = fields.Char('And body contains')
    ratting = fields.Selection((
        ('unrate', 'Unrated'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ),string="And rating is")
    space_mean = fields.Selection(
        (
            ('or', 'or'),
            ('and', 'and')
        ),
        string="Space Means")

    @api.model
    def _get_default_user_id(self):
        return self.env.uid

    _defaults = {
     'search_by_created_uid':_get_default_user_id,
     }

    @api.multi
    def search_data(self):
        data = self.read()[0]
        ids_list = []
        model = ''
        if data['search_type'] and data['search_by_created_uid'] \
        and data['start_date'] == False \
        and data['end_date'] == False \
        and data['status_id'] == False \
        and data['ratting'] == False \
        and data['contain_title'] == False \
        and data['body_contains'] == False:
            if data['search_type'] == 'experiment':
                if data['search_in_all']:
                    experiment_object = self.env['labpal.experiment'].search([])
                elif data['search_by_created_uid']:
                    u_id = int(data['search_by_created_uid'])
                    experiment_object = self.env['labpal.experiment'].search([('create_uid', '=', u_id)])
                model = 'labpal.experiment'
                for obj_id in experiment_object:
                    ids_list.append(obj_id.id)
            elif data['search_type'] == 'database':
                if data['search_in_all']:
                    database_object = self.env['labpal.database'].search([])
                elif data['search_by_created_uid']:
                    database_object = self.env['labpal.database'].search([('create_uid', \
                        '=', int(data['search_by_created_uid']))])
                model = 'labpal.database'
                for obj_id in database_object:
                    ids_list.append(obj_id.id)
            else:
                if data['search_in_all']:
                    database_object = self.env['labpal.database'].search([('types_of_item_id.name', \
                        '=', data['search_type'])])
                elif data['search_by_created_uid']:
                    database_object = self.env['labpal.database'].search([('types_of_item_id.name', \
                        '=', data['search_type']), \
                    ('create_uid', '=', int(data['search_by_created_uid']))])
                model = 'labpal.database'
                for obj_id in database_object:
                    ids_list.append(obj_id.id)
        elif data['search_type'] and data['status_id'] == False \
        and data['ratting'] == False and data['contain_title'] == False \
        and data['body_contains'] == False:
            if data['search_type'] == 'experiment':
                if data['start_date'] and data['end_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),])
                elif data['start_date'] and data['end_date'] == False:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', start_date)])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('exp_date', '=', start_date)])
                elif data['start_date'] == False and data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', end_date)])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([('exp_date', '=', end_date)])
                model = 'labpal.experiment'
                for exp_obj in experiment_object:
                    ids_list.append(exp_obj.id)
            elif data['search_type'] == 'database':
                if data['start_date'] and data['end_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),])
                elif data['start_date'] and data['end_date'] == False:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', start_date)])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', start_date)])
                elif data['start_date'] == False and data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', end_date)])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', end_date)])
                model = 'labpal.database'
                for db_obj in database_object:
                    ids_list.append(db_obj.id)
            else:
                if data['start_date'] and data['end_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('types_of_item_id.name', '=', data['search_type'])])
                elif data['start_date'] and data['end_date'] == False:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', start_date),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', start_date),
                            ('types_of_item_id.name', '=', data['search_type'])])
                elif data['start_date'] == False and data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', end_date),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', end_date),
                            ('types_of_item_id.name', '=', data['search_type'])])
                model = 'labpal.database'
                for db_obj in database_object:
                    ids_list.append(db_obj.id)

        elif data['search_type'] == 'experiment' and data['status_id'] \
        and data['contain_title'] == False and data['body_contains'] == False:
            StatusId = int(data['status_id'][0])
            if data['start_date'] and data['end_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('exp_status', '=', StatusId)])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('exp_status', '=', StatusId)])
            elif data['start_date'] and data['end_date'] == False:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', start_date),
                            ('exp_status', '=', StatusId)])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([('exp_date', '=', start_date),
                            ('exp_status', '=', StatusId)])
            elif data['start_date'] == False and data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', end_date),
                            ('exp_status', '=', StatusId)])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([('exp_date', '=', end_date),
                            ('exp_status', '=', StatusId)])
            elif data['start_date'] == False and data['end_date'] == False:
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_status', '=', StatusId)])
                    elif data['search_in_all']:
                        experiment_object = self.env['labpal.experiment'].search([
                            ('exp_status', '=', StatusId)])
            model = 'labpal.experiment'
            for exp_obj in experiment_object:
                    ids_list.append(exp_obj.id)
        elif data['search_type'] == 'database' and data['ratting'] \
        and data['contain_title'] == False \
        and data['body_contains'] == False:
            if data['start_date'] and data['end_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('rating', '=', data['ratting'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('rating', '=', data['ratting'])])
            elif data['start_date'] and data['end_date'] == False:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', start_date),
                            ('rating', '=', data['ratting'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', start_date),
                            ('rating', '=', data['ratting'])])
            elif data['start_date'] == False and data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', end_date),
                            ('rating', '=', data['ratting'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', end_date),
                            ('rating', '=', data['ratting'])])
            elif data['start_date'] == False and data['end_date'] == False:
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('rating', '=', data['ratting'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([
                            ('rating', '=', data['ratting'])])
            model = "labpal.database"
            for db_obj in database_object:
                    ids_list.append(db_obj.id)
        elif data['search_type'] not in ['experiment','database'] \
        and data['ratting'] and data['contain_title'] == False \
        and data['body_contains'] == False:
            if data['start_date'] and data['end_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '>=', start_date),
                            ('exp_date', '<=', end_date),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
            elif data['start_date'] and data['end_date'] == False:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', start_date),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', start_date),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
            elif data['start_date'] == False and data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('exp_date', '=', end_date),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('exp_date', '=', end_date),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
            elif data['start_date'] == False and data['end_date'] == False:
                    if data['search_by_created_uid'] and data['search_in_all'] == False:
                        database_object = self.env['labpal.database'].search([
                            ('create_uid', '=', int(data['search_by_created_uid'])),
                            ('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['search_in_all']:
                        database_object = self.env['labpal.database'].search([('rating', '=', data['ratting']),
                            ('types_of_item_id.name', '=', data['search_type'])])
            model = "labpal.database"
            for db_obj in database_object:
                    ids_list.append(db_obj.id)
        elif data['contain_title'] and data['body_contains']:
            if data['search_type'] == 'experiment' and data['status_id']:
                StatusId = int(data['status_id'][0])
                if data['space_mean'] == 'or':
                    titles = str(data['contain_title']).split()
                    templates_text = str(data['body_contains']).split()
                    if data['end_date'] and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                    elif data['end_date'] and data['start_date'] == False:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', end_date),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_date', '=', end_date),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', start_date),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_date', '=', start_date),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_status', '=', StatusId)])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                elif data['space_mean'] in ['and', False]:
                    if data['end_date'] and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('exp_status', '=', StatusId)])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('exp_status', '=', StatusId)])
                    elif data['end_date'] == False and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),
                                    ('exp_status', '=', StatusId)])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('exp_status', '=', StatusId)])
                    elif data['end_date'] and data['start_date'] == False:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),
                                    ('exp_status', '=', StatusId)])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('exp_status', '=', StatusId)])
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_status', '=', StatusId)])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_status', '=', StatusId)])
                    else:
                        pass
                    for exp_obj in experiment_object:
                        ids_list.append(exp_obj.id)
                model = "labpal.experiment"
                ids_set = set(ids_list)
                ids_list = list(ids_set)
            elif data['search_type'] == 'experiment' and data['status_id'] == False:
                if data['space_mean'] == 'or':
                    titles = str(data['contain_title']).split()
                    templates_text = str(data['body_contains']).split()
                    if data['end_date'] and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                    elif data['end_date'] and data['start_date'] == False:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', end_date),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_date', '=', end_date),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', start_date),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('exp_date', '=', start_date),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for item_text in templates_text:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('description', 'ilike', item_text),])
                                    for exp_obj in experiment_object:
                                        ids_list.append(exp_obj.id)
                elif data['space_mean'] == 'and':
                    if data['end_date'] and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ])
                    elif data['end_date'] == False and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ])
                    elif data['end_date'] and data['start_date'] == False:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ])
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', '=', data['contain_title']),
                                    ('description', '=', data['body_contains']),
                                    ])
                    else:
                        pass
                    for exp_obj in experiment_object:
                        ids_list.append(exp_obj.id)
                else:
                    if data['end_date'] and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ])
                    elif data['end_date'] == False and data['start_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ])
                    elif data['end_date'] and data['start_date'] == False:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ])
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ])
                        elif data['search_in_all']:
                            experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ])
                    else:
                        pass
                    for exp_obj in experiment_object:
                        ids_list.append(exp_obj.id)
                model = "labpal.experiment"
                ids_set = set(ids_list)
                ids_list = list(ids_set)
            elif data['search_type'] == 'database':
                if data['space_mean'] == 'or':
                    titles = str(data['contain_title']).split()
                    templates_text = str(data['body_contains']).split()
                    if data['start_date'] and data['end_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    elif data['start_date'] and data['end_date'] == False:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date']:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    else:
                        pass
                elif data['space_mean'] in ['and', False]:
                    if data['start_date'] and data['end_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),])
                    elif data['start_date'] and data['end_date'] == False:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '=', start_date),])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),])
                    elif data['start_date'] == False and data['end_date']:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),])
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('rating', '=', data['ratting']),])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),])
                    else:
                        pass
                    for db_obj in database_object:
                        ids_list.append(db_obj.id)
                model = 'labpal.database'
                ids_set = set(ids_list)
                ids_list = list(ids_set)
            else:
                if data['space_mean'] == 'or':
                    titles = str(data['contain_title']).split()
                    templates_text = str(data['body_contains']).split()
                    if data['start_date'] and data['end_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    elif data['start_date'] and data['end_date'] == False:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', start_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date']:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('exp_date', '=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                for body_text in templates_text:
                                    if data['ratting']:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('description', 'ilike', body_text),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                    for db_obj in database_object:
                                        ids_list.append(db_obj.id)
                    else:
                        pass
                elif data['space_mean'] in ['and', False]:
                    if data['start_date'] and data['end_date']:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] and data['end_date'] == False:
                        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike',  data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] == False and data['end_date']:
                        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('rating', '=', data['ratting']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                database_object = self.env['labpal.database'].search([
                                    ('name', 'ilike', data['contain_title']),
                                    ('description', 'ilike', data['body_contains']),
                                    ('types_of_item_id.name', '=', data['search_type'])])
                    else:
                        pass
                    for db_obj in database_object:
                        ids_list.append(db_obj.id)
                model = 'labpal.database'
                ids_set = set(ids_list)
                ids_list = list(ids_set)
        elif data['contain_title'] and data['body_contains'] == False:
            if data['search_type'] == 'experiment':
                if data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['start_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['space_mean'] == 'or':
                    titles = str(data['contain_title']).split()
                    if data['end_date'] and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                    elif data['end_date'] and data['start_date'] == False:
                        # end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_date', '=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_date', '=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date']:
                        # start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', start_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', start_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_date', '=', start_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_date', '=', start_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('exp_title', 'ilike', title),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                elif data['space_mean'] in ['and', False]:
                    if data['end_date'] and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),])
                    elif data['end_date'] and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_date', '=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_date', '=', end_date),])
                    elif data['end_date'] == False and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_date', '=', start_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_date', '=', start_date),])
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('exp_title', 'ilike', data['contain_title']),])
                    for exp_obj in experiment_object:
                        ids_list.append(exp_obj.id)
                model = 'labpal.experiment'
                ids_set = set(ids_list)
                ids_list = list(ids_set)
            elif data['search_type'] != 'experiment':
                if data['start_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['space_mean'] == 'or':
                    titles = str(data['contain_title']).split()
                    if data['start_date'] and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    elif data['start_date'] and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', start_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('exp_date', '=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('name', 'ilike', title),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for title in titles:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('name', 'ilike', title),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    else:
                        pass
                elif data['space_mean'] in ['and', False]:
                    if data['start_date'] and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', start_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] == False and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('exp_date', '=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('name', 'ilike', data['contain_title']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('name', 'ilike', data['contain_title']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    else:
                        pass
                    for db_obj in database_object:
                        ids_list.append(db_obj.id)
                model = 'labpal.database'
                ids_set = set(ids_list)
                ids_list = list(ids_set)
        elif data['contain_title'] == False and data['body_contains']:
            if data['search_type'] == 'experiment':
                if data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['start_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['space_mean'] == 'or':
                    description = str(data['body_contains']).split()
                    if data['end_date'] and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                    elif data['end_date'] and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_date', '=', end_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_date', '=', end_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', start_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_date', '=', start_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_date', '=', start_date),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_date', '=', start_date),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('create_uid', '=', int(data['search_by_created_uid'])),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['status_id']:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),
                                        ('exp_status', '=', int(data['status_id'][0]))])
                                else:
                                    experiment_object = self.env['labpal.experiment'].search([
                                        ('description', 'ilike', text),])
                                for exp_obj in experiment_object:
                                    ids_list.append(exp_obj.id)
                elif data['space_mean'] in ['and', False]:
                    if data['end_date'] and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '>=', start_date),
                                    ('exp_date', '<=', end_date),])
                    elif data['end_date'] and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', end_date),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', end_date),])
                    elif data['end_date'] == False and data['start_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_date', '=', start_date),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_date', '=', start_date),])
                    elif data['end_date'] == False and data['start_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('create_uid', '=', int(data['search_by_created_uid'])),])
                        elif data['search_in_all']:
                            if data['status_id']:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),
                                    ('exp_status', '=', int(data['status_id'][0]))])
                            else:
                                experiment_object = self.env['labpal.experiment'].search([
                                    ('description', 'ilike', data['body_contains']),])
                    for exp_obj in experiment_object:
                        ids_list.append(exp_obj.id)
                model = 'labpal.experiment'
                ids_set = set(ids_list)
                ids_list = list(ids_set)
            elif data['search_type'] != 'experiment':
                if data['start_date']:
                    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['end_date']:
                    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d')
                if data['space_mean'] == 'or':
                    description = str(data['body_contains']).split()
                    if data['start_date'] and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '>=', start_date),
                                            ('exp_date', '<=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    elif data['start_date'] and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', start_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('exp_date', '=', end_date),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('create_uid', '=', int(data['search_by_created_uid'])),
                                            ('description', 'ilike', text),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                        elif data['search_in_all']:
                            for text in description:
                                if data['ratting']:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('rating', '=', data['ratting']),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('rating', '=', data['ratting']),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                else:
                                    if data['search_type'] == 'database':
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),])
                                    else:
                                        database_object = self.env['labpal.database'].search([
                                            ('description', 'ilike', text),
                                            ('types_of_item_id.name', '=', data['search_type'])])
                                for db_obj in database_object:
                                    ids_list.append(db_obj.id)
                    else:
                        pass
                elif data['space_mean'] in ['and', False]:
                    if data['start_date'] and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '>=', start_date),
                                        ('exp_date', '<=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', start_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] == False and data['end_date']:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('exp_date', '=', end_date),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    elif data['start_date'] == False and data['end_date'] == False:
                        if data['search_by_created_uid'] and data['search_in_all'] == False:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('create_uid', '=', int(data['search_by_created_uid'])),
                                        ('description', 'ilike', data['body_contains']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                        elif data['search_in_all']:
                            if data['ratting']:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('rating', '=', data['ratting']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('rating', '=', data['ratting']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                            else:
                                if data['search_type'] == 'database':
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),])
                                else:
                                    database_object = self.env['labpal.database'].search([
                                        ('description', 'ilike', data['body_contains']),
                                        ('types_of_item_id.name', '=', data['search_type'])])
                    else:
                        pass
                    for db_obj in database_object:
                        ids_list.append(db_obj.id)
                model = 'labpal.database'
                ids_set = set(ids_list)
                ids_list = list(ids_set)
        else:
            pass
        if model and len(ids_list) > 0:
            return{
                'views': [[False, 'kanban'],[False, "form"],[False, 'tree']],
                'res_model': model,
                'type': 'ir.actions.act_window',
                'domain': [['id', 'in', ids_list]],
            }
        else:
            return{
                'views': [[False, "form"]],
                'res_model': 'labpal.serach_model',
                'type': 'ir.actions.act_window',
                'target' : 'inline'
            }

class MailComposer(models.TransientModel):
    """ Generic message composition wizard. You may inherit from this wizard
        at model and view levels to provide specific features.

        The behavior of the wizard depends on the composition_mode field:
        - 'comment': post on a record. The wizard is pre-populated via ``get_record_data``
        - 'mass_mail': wizard in mass mailing mode where the mail details can
            contain template placeholders that will be merged with actual data
            before being sent to each recipient.
    """
    _name = 'mail.compose.message'
    _inherit = ['mail.compose.message','labpal.experiment']
    _description = 'Email composition wizard'
    _log_access = True
    _batch_size = 500

    @api.multi
    def experiment_email(self):
    

        print "MAIL COMPOSE"

        email_obj = self.pool.get('mail.template')

        print "email_obj = ", email_obj


        template_id = self.pool.get('mail.template').search(self.env.cr, self.env.uid, 
            [('name', '=', 'Labpal Email Template')], context=self.env.context)[0]

        template_num = email_obj.search(self.env.cr,self.env.uid,[('name','=','Labpal Email Template')])
        print "template_num = ", template_num[0]
        print "template_id = ", template_id

        email = email_obj.browse(self.env.cr, self.env.uid, template_num[0])

        print "email = ", email 

        attachment_obj = self.pool.get('ir.attachment')

        print " attachment_obj = ", attachment_obj
        ir_actions_report = self.pool.get('ir.actions.report.xml')

        print "ir_actions_report = ",ir_actions_report

        datas = {}
        matching_reports = ir_actions_report.search(
            self.env.cr, self.env.uid, [('name', '=', 'Download as a pdf file')])
        matching_reports = matching_reports[0]
        print "matching_reports", matching_reports
    
        if matching_reports:
            report = ir_actions_report.browse(self.env.cr, self.env.uid, matching_reports)
            report_service = 'report.' + report.report_name
            print "report var = ", report
            rep = 'report.'+ report.report_file
            print "Report", rep




            # result, format = openerp.report.render_report(cr, uid,[''],report.report_name,datas,{})
            #result, format = openerp.report.render_report(cr, uid,report.report_name, datas, context)
            # result, format = openerp.report.render_report(self.env.cr,self.env.uid,,port.report_name, {}, {})
            if not report.attachment:
                file_name = "Labpal Experiment Report.pdf"
               
                # attachment_id = attachment_obj.create(self.env.cr, self.env.uid,
                #                                       {
                #                                           'name': file_name,
                #                                           'datas': base64.b64encode(result),
                #                                           'datas_fname': file_name,
                #                                           'type': 'binary'
                #                                       }, context=self.env.context)
                # print "attachment = ", attachment_id
                print "email.email_from = ", email.email_from
                print "email.email_to = " , email.email_to
                print "email.subject = " , email.subject
                print "body_html = ", email.body_html 

                print "uid = ", self.env.uid
                print "cr = " , self.env.cr
                email_obj.write(self.env.cr, self.env.uid, template_num[0], {'email_from':email.email_from,
                                                   'email_to':email.email_to,
                                                   'subject':email.subject,
                                                   'body_html':email.body_html,
                                                   #'attachment_ids': [(6, 0, [attachment_id])],
                                                   })
                # #print "STATUS",email_obj.send_mail(cr, uid,template_num[0], ['']) 
                #req_id = self.pool.get('res.users').search(cr, '', [('login' , '=', email.email_to)])
                #print "req_id = ", req_id
                email_obj.send_mail(self.env.cr, self.env.uid,template_num[0], 1, True, {})
                #email_obj.send_mail(cr, uid, template_id, False, True, context=context)
                #print "Email Response",email_obj.send_mail(cr, uid,['5'], history_id)

        return True


