# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class LibraryBookLoan(models.Model):
    _inherit = 'library.book.loan'

    expected_return_date = fields.Date('Due for', required=True)

class LibraryMember(models.Model):
    _inherit = 'library.member'

    loan_duration = fields.Integer('Loan duration',
                                   default=15,
                                   required=True)