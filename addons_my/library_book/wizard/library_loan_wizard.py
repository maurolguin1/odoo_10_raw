# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'

    member_id = fields.Many2one('library.member', 'Member')
    book_ids = fields.Many2many('library.book', 'Books')

    # refactored in  Wizards and Code reuse p.159 (p.136 in the book).
    @api.multi
    def record_loans(self):
        for wizard in self:
            # member = wizard.member_id # outdated p.138 - p.b.115
            books = wizard.book_ids
            loan = self.env['library.book.loan']
            for book in books:
                values = self._prepare_loan(book)
                loan.create(values)

                # outdated p.138 - p.b.115
                # loan.create({
                #     'member_id': member.id,
                #     'book_id': book.id
                # })

    # p.138 - pb. 115
    @api.multi
    def _prepare_loan(self, book):
        return {
            'member_id': self.member_id.id,
            'book_id': self.book.id
        }

    # refactored in  Wizards and Code reuse p.159 (p.136 in the book).
    @api.multi
    def record_borrows(self):
        # self.ensure_one()
        for wizard in self:
            member = self.member_id
            books = self.book_ids
            member.borrow_books(books)
        member_ids = self.mapped('member_id').ids
        action = {
            'type': 'ir.action.act_window',
            'name': 'Borrower',
            'res_model': 'library.member',
            'domain': [('id', '=', member_ids)],
            'view_mode': 'form,tree'
        }
        return action


    def _default_member(self):
        if self.context.get('active_model' == 'library.member'):
            return self.self.context.get('active_id', False)

