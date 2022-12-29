from odoo import models, fields, _


class ProductProduct(models.Model):
	_inherit = 'product.product'

	warehouse = fields.Char('Emplacement de stock', store=False, search='_search_by_warehouse')

	def _search_by_warehouse(self, operator, value):
		if (operator == '!=' and value is True) or (operator == '=' and value is False):
			domain_operator = 'not in'
		else:
			domain_operator = 'in'
		if not isinstance(value, list):
			value = [value]
		warehouse = self.env['stock.warehouse'].search(['|', ('name', domain_operator, value), ('code', domain_operator, value)])
		products = self.env['product.product'].with_context(warehouse=warehouse.ids).search([('qty_available', '>', 0)])
		return [('id', domain_operator, products and products.ids or [])]
