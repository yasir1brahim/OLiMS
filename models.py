# -*- coding: utf-8 -*-

import datetime
from HTMLParser import HTMLParser
from StringIO import StringIO
import base64
import csv
import datetime
import logging
from openerp import http
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
import psycopg2
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from HTMLParser import HTMLParser
import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import tempfile
from StringIO import StringIO
import csv
from openerp import http
from openerp.http import request

import tkFileDialog as filedialog
from wizard.export_experiment import generate_csv 


#from openerp.http import request


AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Very Low'),
    ('2', 'Low'),
    ('3', 'Medium'),
    ('4', 'High'),
    ('5', 'Very High'),
    ]

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class Experiment(models.Model):

    _name = 'labpal.experiment'

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
        return generate_csv(self, self.ids, self._name)

    @api.multi
    def get_csv(self):

        print "IN GET CSV"

        

        print "DATA"

        query_desc="SELECT description FROM labpal_experiment where id="+ str(self.id) + ""


        join_q = "SELECT tag_id FROM experiment_tag_rel where experiment_id="+ str(self.id) + ""
        conn = psycopg2.connect("dbname = 'labpal' user = 'dev' host = 'localhost' password = 'labpal9'")
        cur = conn.cursor()

        cur.execute(join_q)
        tagid = cur.fetchone()
        tagid = str(tagid[0])

        query = "select t1.exp_title,t1.exp_date,t2.name,t1.description from labpal_experiment t1,labpal_tag t2 where t1.id="+str(self.id)+" and t2.id ="+ tagid+""

        cur.execute(query_desc)

        result = cur.fetchone()
    
        #result=[result[0] for result in cur.fetchall()]
        result = "'"+result[0]+"'"

        #p = re.compile(r'<.*?>')
    
        s = MLStripper()
        s.feed(result)
        result = s.get_data()

        result = result.replace('/n','')
    

        update_query = "UPDATE labpal_experiment SET description="+result+" WHERE id="+str(self.id)+""

        cur.execute(update_query)
        conn.commit()

        
        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
            
        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["1","a","b","c"])

        conn.close()

    @api.multi
    def get_csv_db(self):
        filename = expanduser("~")
        filename = os.path.join('labpaldb.csv')

        query_desc = "SELECT description FROM labpal_database where id="+ str(self.id) + ""
        join_q = "SELECT tag_id FROM database_tag_rel where database_id="+ str(self.id) + ""

        conn = psycopg2.connect("dbname = 'labpal' user = 'dev' host = 'localhost' password = 'labpal9'")
        cur = conn.cursor()

        cur.execute(join_q)
        tagid = cur.fetchone()
        tagid = str(tagid[0])

        query = "select t1.name,t1.exp_date,t2.name,t1.description from labpal_database t1,labpal_tag t2 where t1.id="+str(self.id)+" and t2.id ="+ tagid+""



        cur.execute(query_desc)

        result = cur.fetchone()
        result = "'"+result[0]+"'"
        print result
        s = MLStripper()
        s.feed(result)
        result = s.get_data()
        result = result.replace('/n','')
        
        #result = str(result)
        
        print result

        update_query = "UPDATE labpal_database SET description="+result+" WHERE id="+str(self.id)+""  

        #print update_query

        cur.execute(update_query)
        conn.commit()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open(filename, 'w+') as f:
                cur.copy_expert(outputquery , f)
        conn.close()
        webbrowser.open(filename)
        return True

    @api.multi
    def get_pdf(self):
        file = self.env['report'].get_action(self, 'labpal.pdf_template')
        return self.env['report'].get_action(self, 'labpal.pdf_template')

    @api.multi    
    def get_pdf_db(self):
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
    def get_zip():
        file = self.env['report'].get_action(self, 'labpal.pdf_template')


    @api.multi
    def get_zip_test(self):


        file_csv = tempfile.gettempdir()

        query_desc = "SELECT description FROM labpal_experiment where id="+ str(self.id) + ""


        join_q = "SELECT tag_id FROM experiment_tag_rel where experiment_id="+ str(self.id) + ""
        conn = psycopg2.connect("dbname = 'labpal' user = 'dev' host = 'localhost' password = 'labpal9'")
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
        
        filename = filedialog.asksaveasfilename()        
        shutil.make_archive(filename,'zip','test.csv')

        #shutil.move(file_csv, filename)
        
        webbrowser.open(filename)


    @api.multi
    def send_email():
        pass


    @api.onchange('template_id')
    def _onchange_template(self):
        for record in self:
            template = self.env['labpal.template'].search([('id', '=', record.template_id.id)])
            if template:
                record.description = template.template
    
    
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100





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

class Preferences(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = "labpal.preferences"

    create_key_value = fields.Char('Create',default="Ctrl + N")
    edit_key_value = fields.Char('Edit',default="Ctrl + E")
    save_key_value = fields.Char('Save',default="Ctrl + S")
    cancel_key_value = fields.Char('Cancel',default="Ctrl + Z")


