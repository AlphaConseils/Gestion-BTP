from odoo import models, fields, api
from odoo.addons.oti_sale.models.tools import amount_to_text_fr


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	project_subject = fields.Char("Objet du projet")
	amount_total_text = fields.Char('Amount total text', compute='compute_amount_to_text')

	def compute_amount_to_text(self):
		for rec in self:
			rec.amount_total_text = amount_to_text_fr(rec.amount_total, rec.currency_id.currency_unit_label)


class SakeOrderLine(models.Model):
	_inherit = 'sale.order.line'

	item = fields.Char('Item')
