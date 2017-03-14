# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.fields import Date as fDate


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'


    publisher_id = fields.Many2one('res.partner',
                                   string='Publisher',
                                   # optional parameters
                                   ondelete='set null',
                                   context={},
                                   domain=[],
                                   )
    name = fields.Char(string='Title', required=True)
    short_name = fields.Char(
        string='Short Title',
        size=100, # For Char only
        translate=False # Also for text files
    )
    author_ids = fields.Many2many(comodel_name="res.partner",
                                  string="Authors")
    notes = fields.Text(string="Internal Notes")
    state = fields.Selection(
         string="State",
         selection=[('draft', 'Not Available'),
                    ('available', 'Available'),
                    ('lost', 'Lost')]
         )
    # description = fields.HTML(string="Description",
    #                             # optional
    #                             # sanitize=True,
    #                             # strip_style=False,
    #                             # translate=False
    #                         )
    cover = fields.Binary(string="Book Cover")
    out_of_print = fields.Boolean(string="Out of Print?")
    date_release = fields.Date(string="Release Date")
    date_update = fields.Datetime(string="Last Update")
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
    active = fields.Boolean('Active',
                            default=True, # making default value for this field
                            domain=[('active', '=', False)])
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price',
                                   currency_field='currency_id' # optional
                                   )

    # Computed field
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False,
    )


    # Database constrains
    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book Title must be unique.'
         )
    ]

    @api.constrains('date_release')
    def _check_release(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError(
                    'Release must be in the past.'
                )

    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release - today))
            book.age = delta.days

    # Using method name_get(), vide pag. 89D
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, u'%s (%s)' % (record.name, record.date_released)
            ))
        return result


class ResPartner(models.Model):
    _inherit = 'res.partner'

    book_ids = fields.Many2many('library.book',
                               string='Authored Books',
                                # relation='library_book_res_partner_rel' # optional
                                )
