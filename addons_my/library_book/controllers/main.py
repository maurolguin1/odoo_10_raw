# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request


class Main(http.Controller):

    @http.route('/library_book/books', type='http', auth='none')
    def books(self):
        records = request.env['library.book'].sudo().search([])
        result = '<html><body><table><tr><td>'
        result += '</td></tr></table></body></html>'
        return result

    @http.route('/library_book/books/json', type='json', auth='none')
    def books_json(self):
        record = request.env['library.book'].sudo().search([])
        return record.read(['name'])
