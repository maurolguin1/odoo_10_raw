# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import email
import datetime
from odoo import fields, http
from odoo.http import request


class Main(http.Controller):

    @http.route('/library_book/books', type='http', auth='public')
    def books(self):
        records = request.env['library.book'].sudo().search([])
        result = '<html><body><table><tr><td>'
        result += '</td></tr></table></body></html>'
        return request.make_response(result, [
            ('Last-modified', email.utils.formatdate(
                fields.Datetime.from_string(
                request.env['library.book'].sudo().search([],
                order='write_date desc', limit=1).write_date -
                datetime.datetime(1970, 1, 1)).total_seconds(),
                usegmt=True))])

    @http.route('/library_book/books/json', type='json', auth='public')
    def books_json(self):
        record = request.env['library.book'].sudo().search([])
        return record.read(['name'])

    @http.route('/hello', auth='public')
    def hello_world(self):
        return '<h1>Hello World!</h1>'
