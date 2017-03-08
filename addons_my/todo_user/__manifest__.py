# -*- coding: utf-8 -*-
# © 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Multiuser  To-Do',
    'description': 'Extending To-Do app to multiuser.',
    'author': 'Daniel Reis',
    'depends': ['todo_app', 'mail'],
	'data': [
		'views/todo_task.xml',
		'security/todo_access_rules.xml'
	],
	'demo': [
		'data/todo.task.csv',
		'data/todo_data.xml',
	],
}
