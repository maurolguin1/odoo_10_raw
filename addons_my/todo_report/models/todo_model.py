# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class TodoTask(models.Model):
    _inherit = 'todo.task'
    amount_cost = fields.Monetary(
            'Cost',
            currency_field ='currency_id')
    currency_id = fields.Many2one('res.currency')
