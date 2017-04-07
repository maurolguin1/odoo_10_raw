# -*- coding: utf-8 -*-
# © 2016 Outtech - http://www.outtech.com.br/
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'My Library',
    'description': """Library to rent and consult books""",
    'category': 'Manufacturing',
    'author': 'Jôvani Moura',
    'maintainer': 'Jôvani',
    'website': 'http://www.jovanimoura.com.br',
    'version': '10.0.1.0.0',
    'depends': [
        'base',
        'decimal_precision'
    ],
    'data': [
        'views/library_book_view.xml',
        'views/library_loan_wizard_view.xml',
        'views/partner_test_view.xml',
        # 'data/res_partner.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'license': 'AGPL-3'
}
