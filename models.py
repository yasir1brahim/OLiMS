# -*- coding: utf-8 -*-

from openerp import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Very Low'),
    ('2', 'Low'),
    ('3', 'Medium'),
    ('4', 'High'),
    ('5', 'Very High'),
    ]

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
    _order = "name asc"

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
            'views': [[False, 'tree']],
            'domain' : [('id', 'in', ids_list)]
            }
        else:
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[False, 'tree']],
            }

    @api.multi
    def disaplay_ordered_database(self):
        data = self.read()[0]
        ids_list = []
        kanban_view = self.env.ref('labpal.database_kanban_view', False)
        if data['order_by'] and data['sort_by']:
            sortBy = data['order_by'] + " " + data['sort_by']
            database_res = self.env['labpal.database'].search([], order=sortBy)
            for ids in database_res:
                ids_list.append(ids.id)
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[kanban_view.id, 'kanban']],
            'domain' : [('id', 'in', ids_list)],
            'view_mode': 'kanban',
            'view_id': kanban_view.id,
            'flags': {'action_buttons': True},
            }
        elif data['order_by']:
            sortBy = data['order_by'] + " " + 'desc'
            database_res = self.env['labpal.database'].search([], order=sortBy)
            for ids in database_res:
                ids_list.append(ids.id)
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'labpal.database',
            'views': [[kanban_view.id, 'kanban']],
            'domain' : [('id', 'in', ids_list)],
            'view_mode': 'kanban',
            'view_id': kanban_view.id,
            'flags': {'action_buttons': True},
            }
        else:
            return {
            'type': "ir.actions.act_window",
            'res_model': "labpal.database",
            'views': [[kanban_view.id, "tree"]],
            'view_mode': 'tree',
            'view_id': kanban_view.id,
            'target' : "current"
            }