# -*- coding: utf-8 -*-
# © 2017 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

class ResPartner(models.Model):
    _name = 'res.partner'

    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean('Is a company')
    parent_id = fields.Many2one('res.partner', 'Related Company')
    chield_ids = fields.One2many('res.partner', 'parent_id', 'Contacts')

    @api.model
    def create(self, record):
        today_str = fields.Date.context_today()

        # dict for first contact
        val1 = {
            'name': u'Eric Idle',
            'email': u'eric.idle@example.com',
            'date': today_str
        }

        # dict for the second contact
        val2 = {
            'name': u'John Cleese',
            'email': u'john@example.com',
            'date': today_str
        }

        # dict for the fields for Company
        partner_val = {
            'name': u'Flying Circus',
            'email': u'm.python@example.com',
            'date': today_str,
            'is_company': True,
            'child_ids': [(0, 0, val1),
                          (0, 0, val2)]
        }

        # calling the create method
        record = self.env['res.partner'].create(partner_val)

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