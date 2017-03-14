# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class BookCategory(models.Model):
    _name = 'library.book.category'

    name = fields.Char('Category')

    # Adding hierarchy to a Model
    parent_id = fields.Many2one('library.book.category',
                                string='Parent Category',
                                ondelete='restrict',
                                index=True
                                )
    child_ids = fields.One2many('library.book.category',
                                'parent_id',
                                string='Child Category'
                                )
    _parent_store = True
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive categories.'
            )