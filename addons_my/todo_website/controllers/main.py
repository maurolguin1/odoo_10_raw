# -*- coding: utf-8 -*-
# © 2016 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import http

class Todo(http.Controller):
    @http.route('helloworld', auth='public')
    def hello_world(self):
        return('<h1>Hello World!<h1>')