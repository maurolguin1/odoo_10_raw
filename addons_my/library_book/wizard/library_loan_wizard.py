# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'

    member_id = fields.Many2one('library.member', 'Member')
    book_ids = fields.Many2many('library.book', 'Books')

    @api.multi
    def record_loans(self):
        for wizard in self:
            member = wizard.member_id
            books = wizard.book_ids
            loan = self.env['library.book.loan']
            for book in books:
                loan.create({
                    'member_id': member.id,
                    'book_id': book.id
                })