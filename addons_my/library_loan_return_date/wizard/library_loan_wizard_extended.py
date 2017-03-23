# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from odoo import fields, models, api

class LibraryLoanWizard(models.TransientModel):
    _inherit = 'library.loan.wizard'

    def _prepare_loan(self, book):
        values = super(LibraryLoanWizard, self)._prepare_loan(book)
        loan_duration = self.member_id.loan_duration
        today_str = fields.Date.context_today()
        today = fields.Date.today(today_str)
        expected = today + timedelta(days=loan_duration)
        values.update(
            {
                'expected_return_date': fields.Date.to_string(expected)
            }
        )
        return values