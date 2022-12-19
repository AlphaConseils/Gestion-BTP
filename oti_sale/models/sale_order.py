from odoo import models, fields, api
from odoo.addons.oti_sale.models.tools import amount_to_text_fr
from datetime import datetime


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	project_subject = fields.Char('Objet du projet')
	amount_total_text = fields.Char('Amount total text', compute='compute_amount_to_text')
	sale_attachment_date = fields.Date('Choisissez la période à afficher')
	sale_attachment_widget = fields.Binary(compute='_compute_sale_attachment')
	attachment_note = fields.Html('Note')

	@api.depends('sale_attachment_date', 'order_line.attachment_period_ids')
	def _compute_sale_attachment(self):
		for sale in self:
			sale_attachment_vals = {'title': 'Attachement', 'date_ref': 'sale_attachment_date', 'content': []}
			order_line_vals = []
			for line in sale.order_line:
				if 'virtual' not in str(line.id):
					percent_anterior = sum(
						line.mapped('attachment_period_ids').filtered(lambda l: sale.sale_attachment_date and l.date < sale.sale_attachment_date.replace(day=1)).mapped('percentage'))
					price_anterior = line.price_subtotal * percent_anterior / 100
					percent_current = sum(line.mapped('attachment_period_ids').filtered(
						lambda l: fields.Date.from_string(l.date).month == fields.Date.from_string(
							sale.sale_attachment_date).month and fields.Date.from_string(l.date).year == fields.Date.from_string(
							sale.sale_attachment_date).year).mapped('percentage'))
					price_current = line.price_subtotal * percent_current / 100
					order_line_vals.append({
						'order_line_id': line.id,
						'item': line.item,
						'name': line.name,
						'product_uom': line.product_uom.name,
						'product_qty': line.product_uom_qty,
						'price_unit': line.price_unit,
						'price_subtotal': line.price_subtotal,
						'percent_anterior': percent_anterior,
						'percent_current': percent_current,
						'price_anterior': price_anterior,
						'price_current': price_current,
						'currency_id': sale.company_id.currency_id.id,


					})
			sale_attachment_vals['content'] = order_line_vals
			if sale_attachment_vals['content']:
				sale.sale_attachment_widget = sale_attachment_vals
			else:
				sale.sale_attachment_widget = False

	def update_sale_attachment(self, order_line_id, date_object, percent):
		order_line_id = order_line_id.split('_')
		if len(order_line_id) > 1:
			order_line_id = order_line_id[1]
		if isinstance(order_line_id, list):
			order_line_id = order_line_id[0]
		sale_line = self.env['sale.order.line'].browse(int(order_line_id))
		if sale_line and date_object.get('year', False) and date_object.get('month', False) and date_object.get('day'):
			month = date_object.get('month')
			year = date_object.get('year')
			new_date = str(date_object['year']) + '-' + str(date_object['month']) + '-' + str(date_object['day'])
			sale_id = sale_line.order_id
			sale_id.write({'sale_attachment_date': new_date})
			attachment_exists = sale_line.mapped('attachment_period_ids').filtered(
				lambda l: fields.Date.from_string(l.date).month == month and fields.Date.from_string(l.date).year == year)
			if attachment_exists:
				attachment_exists[0].write({'percentage': percent, 'date': new_date, })
			else:
				self.env['sale.attachment.period'].create({'order_line_id': order_line_id, 'percentage': percent, 'date': new_date})
		return True

	def compute_amount_to_text(self):
		for rec in self:
			rec.amount_total_text = amount_to_text_fr(rec.amount_total, rec.currency_id.currency_unit_label)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	item = fields.Char('Item')
	attachment_period_ids = fields.One2many('sale.attachment.period', 'order_line_id', string="Attachment periods")
