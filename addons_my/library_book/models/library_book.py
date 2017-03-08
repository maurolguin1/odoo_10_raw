# -*- coding: utf-8 -*-
# © 2016 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         result.append(record.id, u"%s (%s)" % (record.name, record.date_release))
    #     return result

    name = fields.Char(string='Title', required=True)
    short_name = fields.Char(
        string='Short Title',
        size=100, # For Char only
        translate=False # Also for text files
    )
    author_ids = fields.Many2many(comodel_name="res.partner", string="Authors")
    notes = fields.Text(string="Internal Notes")
    state = fields.Selection(
         string="State",
         selection=[('draft', 'Not Available'),
                    ('available', 'Available'),
                    ('lost', 'Lost')]
         )
    # description = fields.HTML(
    #     string="Description",
    #     # optional
    #     sanitize=True,
    #     strip_style=False,
    #     translate=False
    # )
    cover = fields.Binary(string="Book Cover")
    out_of_print = fields.Boolean(string="Out of Print?")
    date_release = fields.Date(string="Release Date")
    date_update = fields.Date(string="Last Update")
    page = fields.Integer(
                            string="Number of Pages",
                            default=0,
                            help='Total book page count',
                            groups='base.group_user',
                            copy=True,
                            index=False,
                            readonly=False,
                            required=False,
                            company_dependent=False
                        )
    reader_rating = fields.Float(
        string="Reader Average Rating",
        digits=(14, 4) # Optional precision (total, decimals)
    )

    # Using method name_get(), vide pag. 89
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u'%s (%s)' % (record.name, record.date_released)
            ))
        return result


