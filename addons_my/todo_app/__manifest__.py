# -*- coding: utf-8 -*-
# © Jovan Moura 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'To-Do Application',
    'description': 'Manage your personal To-Do tasks.',
    'author': 'Daniel Reis',
    'depends': [
	    'base'
    ],
	'data':     [
		'views/todo_menu.xml',
		'views/todo_view.xml',
		'security/ir.model.access.csv',
		'security/todo_access_rules.xml'

	],
    'images': ['static/description/icon.png'],
	'application': True,
    'installable': True,
}
