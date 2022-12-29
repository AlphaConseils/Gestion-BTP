from odoo import models, fields, _


class StockWarehouse(models.Model):
	_inherit = 'stock.warehouse'

	project_id = fields.Many2one('project.project', 'Chantier')
