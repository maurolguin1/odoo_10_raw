	# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task', 'mail.thread']

    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')
    name = fields.Char(help="What needs to be done?")
    state = fields.Many2one('todo.task', 'State')

    @api.multi
    def do_clear_done(self):
        domain = [('is_done', '=', True),
                  '|', ('user_id', '=', self.env.uid),
                       ('user_id', '=', False)]
        dones = self.search(domain)
        dones.write({'active': False})
        return True

    @api.multi
    def do_toggle_done(self):
        for task in self:
            if task.user_id != self.env.user:
                raise ValidationError(
                    'Only the responsible can do this!')
        return super(TodoTask, self).do_toggle_done()

    @api.model
    def create(self, vals):
        # Code before create: can use the `vals` dict
        new_record = super(TodoTask, self).create(vals)
        # Code after create: can use the  `new_record` created
        return new_record

    @api.multi
    def write(self, vals):
        # Code before write: can use `self`, with the old values
        super(TodoTask, self).write(vals)
        # Code after write: can use `self`, with the update values
        return True