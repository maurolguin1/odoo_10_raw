# -*- coding: utf-8 -*-
# © Jovan Moura 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Report Training',
    'description': 'Sale Report Training',
    'author': 'Jay Vora',
    'depends': [
	    'sale', 'website_quote'
    ],
	'data': [
		'views/report_view.xml',
		'report/report_saleorder.xml'
	],
    'installable': True,
}
