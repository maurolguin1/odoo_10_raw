# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, exceptions
from odoo.addons import decimal_precision as dp
from odoo.fields import Date as fDate
from datetime import timedelta as td




class BaseArchive(models.AbstractModel):
    _name = 'base.archive'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = 'base.archive'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'


    manager_remarks = fields.Text('Manager Remarks')
    publisher_id = fields.Many2one('res.partner',
                                   string='Publisher',
                                   # optional parameters
                                   ondelete='set null',
                                   context={},
                                   domain=[],
                                   )
    publisher_city = fields.Char('Publisher City', related='publisher_id.city')
    name = fields.Char(string='Title', required=True)
    isbn = fields.Char('ISBN')
    short_name = fields.Char(
        string='Short Title',
        size=100, # For Char only
        translate=False # Also for text files
    )
    author_ids = fields.Many2many(comodel_name="res.partner",
                                  string="Authors")
    notes = fields.Text(string="Internal Notes")

    # Selection field with state or workflow
    state = fields.Selection(
        [('draft', 'Unavailable'),
         ('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
         'State' # status bar field
         )
    # description = fields.HTML(string="Description",   # HTML field is deprecated since version 10.0
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

    # Referenced Field
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Referenced Documents'
    )

    # Database constrains
    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book Title must be unique.'
         )]

    @api.constrains('date_release')
    def _check_release(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError(
                    'Release must be in the past.'
                )

    # Implementing computed field date_release
    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release - today))
            book.age = delta.days

    # Implementing write on the computed field
    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = td(days=book.age_days) - today
            book.date_release = fDate.to_string(d)

    # Implementing search on the computed field
    def _search_age(self, operator, value):
        today = fDate.to_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]

    # Referencable model
    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object, x.name) for x in models]

    # Using method name_get(), vide pag. 89
    # Refactored p.144 pb.121
    @api.model
    def name_get(self):
        result = []
        for book in self:
            authors = book.author_ids.mapped('name')
            name = u'%s (%s)' % (book.title, u', '.join(authors))
            result.append((book.id, name))
        return result

    # p. 144 pb. 121
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += [
                '|', '|',
                ('name', operator, name),
                ('isbn', operator, name),
                ('author_ids.name', operator, name)
            ]
        return super(LibraryBook, self)._name_search(
            name='', args=args, operator='ilike', limit=limit, name_get_uid=name_get_uid
        )


    # Method for Selection field state p.119
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        # returned_book_ids is a list of book ids to return
        books = self.env['library.book']
        # books.browse(returned_book_ids).change_state('available')
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = book.new_state
            else:
                continue

    @api.model
    def get_all_libraly_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

    # p. 141 pb.118
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if not self.user_has_groups(
            'library.group_library_manager'):
            if 'manager_remarks' in values:
                raise exceptions.UserError(
                    'You are not allowed to modify '
                    'manager_remarks')
        return super(LibraryBook, self).create(values)

    # p. 141 pb.118
    @api.multi
    def write(self, vals):
        if not self.user_has_groups(
            'library.group_library_manager'):
            if 'manager_remarks' in vals:
                raise exceptions.UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )
        return super(LibraryBook, self).write(vals)

    # got an error
    # @api.model
    # def fields_get(self,
    #                allfields=None,
    #                write_access=True,
    #                attributes=None):
    #     fields = super(LibraryBook, self).fields_get(
    #         allfields=allfields,
    #         write_access=write_access,
    #         attributes=attributes)
    #     if not self.user_has_groups(
    #         'library.group_library_manager'):
    #         if 'manager_remarks' in fields:
    #             fields['manager_remarks']['readonly'] = True



class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean('Is a company')
    parent_id = fields.Many2one('res.partner', 'Related Company')
    chield_ids = fields.One2many('res.partner', 'parent_id', 'Contacts')

    book_ids = fields.Many2many('library.book',
                               string='Authored Books',
                                # relation='library_book_res_partner_rel' # optional
                                )
    authored_book_ids = fields.Many2many(
        'library.book', string='Authored Books'
    )
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books'
    )

    # computed field for count_books
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)

    # @api.model
    # def create(self, record):
    #     today_str = fields.Date.context_today()
    #
    #     # dict for first contact
    #     val1 = {
    #         'name': u'Eric Idle',
    #         'email': u'eric.idle@example.com',
    #         'date': today_str
    #     }
    #
    #     # dict for the second contact
    #     val2 = {
    #         'name': u'John Cleese',
    #         'email': u'john@example.com',
    #         'date': today_str
    #     }
    #
    #     # dict for the fields for Company
    #     partner_val = {
    #         'name': u'Flying Circus',
    #         'email': u'm.python@example.com',
    #         'date': today_str,
    #         'is_company': True,
    #         'child_ids': [(0, 0, val1),
    #                       (0, 0, val2)]
    #     }
    #
    #     # calling the create method
    #     record = self.env['res.partner'].create(partner_val)
    #     return record

    @api.model
    def add_contacts(self, partner, contacts):
        partner.ensure_one()
        if contacts:
            partner.date = fields.Date.context_today()
            partner.child_ids |= contacts

    @api.model
    def find_partners_and_contacts(self, name):
        partner = self.env['res.partner']
        domain = [
            '|',
            '&',
            ('is_company', '=', True),
            ('name', 'like', name),
            '&',
            ('is_company', '=', False),
            ('parent_id.name', 'like', name)
        ]
        return partner.search(domain)

    @api.model
    def partners_with_email(self, partners):
        def predicate(partner):
            if partner.email:
                return True
            return False

        return partners.filter(lambda p: p.mail)

    @api.model
    def get_email_addresses(self, partner):
        partner.ensure_one()
        return partner.mapped('child_ids.email')

    @api.model
    def get_companies(self, partners):
        return partners.mapped('parent_id')


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()

class LibraryBookLoan(models.Model):
    _name = 'library.book.loan'

    book_id = fields.Many2one('library.book', 'Book', required=True)
    member_id = fields.Many2one('library.member', 'Borrower', required=True)
    state = fields.Selection(
        [('ongoing',  'Ongoing',
        'done', 'Done')],
        'State',
        default='ongoing',
        required=True)

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.multi
    def update_phone_number(self, new_number):
        self.ensure_one()
        company_as_superuser = self.sudo() # using sudo() p.149, pb.126
        company_as_superuser.phone = new_number

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def stock_in_location(self, location):
        product_in_loc = self.with_context(location=location.id, active_test=False ) # getting product.product recordset with a context modified p.152, pb.129
        all_products = product_in_loc.search([]) # searching all products
        stock_levels = [] # creating an empty array
        for product in all_products:
            if product.qty_available:
                stock_levels.append((product.name, product.qty_available))
        return stock_levels
