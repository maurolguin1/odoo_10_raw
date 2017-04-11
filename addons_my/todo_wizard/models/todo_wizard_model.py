# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo import exceptions
import logging

logger = logging.getLogger(__name__)


class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    _description = 'To-Do Mass Assignment'


    task_ids = fields.Many2many('todo.task', string='Tasks')
    new_deadline = fields.Date('Deadline to set')
    new_user_id = fields.Many2one('res.users', string='Responsible to Set')


    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise exceptions.ValidationError('No data to update!')
        logger.debug('Mass update on Todo Tasks %s', self.task_ids.ids)
        vals = {}
        if self.new_deadline:
            vals['date_deadline'] = self.new_deadline
        if self.new_user_id:
            vals['new_user_id'] = self.new_user_id
        # Mass write values on all selected tasks
        if vals:
            self.task_ids.write(vals)
        return True


    @api.multi
    def do_count_tasks(self):
        Task = self.env['todo.task']
        count = Task.search_count(['is_done', '=', False])
        raise exceptions.Warning('There are %d  active tasks' % count)

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name, # this model
            'res_id':   self.id, # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def do_populate_tasks(self):
        self.ensure_one()
        Task = self.env['todo.task']
        open_tasks = Task.search(['is_done', '=', False])
        # fill the wizard Task list with all tasks
        all_tasks = self.task_ids
        # reopen wizard form on same wizard record
        return self._reopen_form()