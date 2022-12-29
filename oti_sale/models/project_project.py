import json
from odoo import models, fields


class ProjectProject(models.Model):
	_inherit = 'project.project'

	def _get_stat_buttons(self):
		buttons = super()._get_stat_buttons()
		warehouse = self.env['stock.warehouse'].search([('project_id', '=', self.id)])
		if warehouse:
			buttons.append({
				'icon': 'cubes',
				'text': 'Stock',
				'action_type': 'action',
				'action': 'stock.action_product_stock_view',
				'additional_context': json.dumps({
					'active_id': self.id,
					'warehouse': warehouse.id,
					'search_default_warehouse': warehouse.name,
				}),
				'show': True,
				'sequence': 100,
			})
		return buttons
