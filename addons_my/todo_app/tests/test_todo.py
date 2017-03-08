# -*- coding: utf-8 -*-
# © 2016 Jovani Moura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestTodo(TransactionCase):

	def setUp(self, *args, **kwargs):
		result = super(TestTodo, self).SetUp(*args, **kwargs)
		user_demo = self.env.ref('base.user_demo')
		self.env = self.env(user=user_demo)
		return result

	def test_create(self):
		"Create a simple Todo"
		Todo = self.env['todo.task']
		task = Todo.create({'name': 'Test Task'})
		self.assertEquals(task.is_done, False)

		# Test Toggle Done
		task.do_toggle_done()
		self.assertTrue(task.is_done)
		# Test Clear done
		Todo.do_clear_done()
		self.assertFalse(task.active)


	def test_record_rule(self):
		"Test per user record rules"
		Todo = self.env['todo.task']
		task = Todo.sudo().create({'name': 'Admin Task'})
		with self.assertRaises(AccessError):
			Todo.browse([task.id]).name
