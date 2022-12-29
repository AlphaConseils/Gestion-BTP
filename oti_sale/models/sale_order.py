import base64
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.addons.oti_sale.models.tools import amount_to_text_fr
from datetime import datetime


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	project_subject = fields.Char('Objet du projet')
	amount_total_text = fields.Char('Amount total text', compute='compute_amount_to_text')
	sale_attachment_date = fields.Date('Choisissez la période à afficher')
	sale_attachment_widget = fields.Binary(compute='_compute_sale_attachment')
	attachment_note = fields.Html('Note', related='attachment_parent_id.note', readonly=False)
	attachment_parent_id = fields.Many2one('sale.attachment.period.parent', 'Attachment Main')
	attachment_state = fields.Selection(related='attachment_parent_id.state')
	attachment_sequence = fields.Char(compute='_compute_attachment_char')
	attachment_id = fields.Binary(related='attachment_parent_id.attachment_id')
	attachment_name = fields.Char(related='attachment_parent_id.attachment_name', string='Attachment')

	def _compute_attachment_char(self):
		for rec in self:
			attachments = self.env['sale.attachment.period.parent'].search(
				[('sale_id', '=', rec.id), ('state', '=', 'validated'), ('attachment_id', '!=', False)])
			rec.attachment_sequence = 'Attachement n° %s' % (str((len(attachments) + 1)).zfill(3))

	@api.depends('sale_attachment_date', 'order_line.attachment_period_ids', 'attachment_parent_id')
	def _compute_sale_attachment(self):
		for sale in self:
			sale_attachment_vals = {'title': 'Attachement', 'date_ref': 'sale_attachment_date', 'content': []}
			order_line_vals = []
			for line in sale.order_line:
				if 'virtual' not in str(line.id):
					percent_anterior = sum(
						line.mapped('attachment_period_ids').filtered(
							lambda l: sale.sale_attachment_date and l.date < sale.sale_attachment_date.replace(day=1)).mapped('percentage'))
					price_anterior = line.price_subtotal * percent_anterior / 100
					tax_anterior = line.price_tax * percent_anterior / 100
					percent_current = sum(line.mapped('attachment_period_ids').filtered(
						lambda l: fields.Date.from_string(l.date).month == fields.Date.from_string(
							sale.sale_attachment_date).month and fields.Date.from_string(l.date).year == fields.Date.from_string(
							sale.sale_attachment_date).year).mapped('percentage'))
					price_current = line.price_subtotal * percent_current / 100
					tax_current = line.price_tax * percent_current / 100
					order_line_vals.append({
						'order_line_id': line.id,
						'display_type': line.display_type,
						'item': line.item,
						'name': line.name,
						'product_uom': line.product_uom.name,
						'product_qty': line.product_uom_qty,
						'price_unit': line.price_unit,
						'price_subtotal': line.price_subtotal,
						'price_tax': line.price_tax,
						'price_total': line.price_total,
						'percent_anterior': percent_anterior,
						'percent_current': percent_current,
						'price_anterior': price_anterior,
						'price_current': price_current,
						'tax_anterior': tax_anterior,
						'tax_current': tax_current,
						'currency_id': sale.company_id.currency_id.id,
						'attachment_state': sale.attachment_parent_id and sale.attachment_parent_id.state or '',

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
			date_start = fields.Date.from_string(new_date).replace(day=1)
			date_end = date_start + relativedelta(months=1) - relativedelta(days=1)
			exists = self.env['sale.attachment.period.parent'].search(
				[('date', '>=', date_start), ('date', '<=', date_end), ('sale_id', '=', sale_id.id)], limit=1)
			if not exists:
				vals = {
					'sale_id': sale_id.id,
					'date': sale_id.sale_attachment_date,
					'state': 'draft',
				}
				parent_attachment = self.env['sale.attachment.period.parent'].create(vals)
				sale_id.write({'attachment_parent_id': parent_attachment.id})
		return True

	def compute_amount_to_text(self):
		for rec in self:
			rec.amount_total_text = amount_to_text_fr(rec.amount_untaxed, rec.currency_id.currency_unit_label)

	def action_attachment_report(self):
		return self.env.ref('oti_sale.action_report_attachment').report_action(self.ids)

	@api.onchange('sale_attachment_date')
	def onchange_sale_attachment_date(self):
		if self.sale_attachment_date:
			date_start = self.sale_attachment_date.replace(day=1)
			date_end = date_start + relativedelta(months=1) - relativedelta(days=1)
			parent_attachment_id = self.env['sale.attachment.period.parent'].search(
				[('sale_id', '=', self.ids[0]), ('date', '>=', date_start), ('date', '<=', date_end)], limit=1)
			if parent_attachment_id:
				self.attachment_parent_id = parent_attachment_id.id
			else:
				self.attachment_parent_id = False
		else:
			self.attachment_parent_id = False

	def confirm_attachment(self):
		self.ensure_one()
		if self.attachment_parent_id:
			self.attachment_parent_id.state = 'validated'
		else:
			vals = {
				'sale_id': self.id,
				'note': self.attachment_note,
				'date': self.sale_attachment_date,
				'state': 'validated',
			}
			parent_attachment = self.env['sale.attachment.period.parent'].create(vals)
			self.update({'attachment_parent_id': parent_attachment.id})
		self.attachment_parent_id.write({'attachment_name': self.attachment_sequence})
		pdf, _ = self.env['ir.actions.report'].with_context(landscape=True)._render_qweb_pdf('oti_sale.action_report_attachment', self.ids[0])
		self.attachment_parent_id.write({'attachment_id': base64.b64encode(pdf)})

	def _get_invoiceable_lines(self, final=False):
		res = super()._get_invoiceable_lines(final)
		downpayment_lines = res.filtered(lambda l: l.is_downpayment).ids
		attachment_invoiceable = []
		for line in res:
			sale = line.order_id
			if sale.attachment_parent_id:
				date = sale.attachment_parent_id.date
				date_start = date.replace(day=1)
				date_end = date_start + relativedelta(months=1) - relativedelta(days=1)
				attachment = line.attachment_period_ids.filtered(lambda l: date_start <= l.date <= date_end)
				if attachment and attachment.percentage:
					attachment_invoiceable.append(line.id)
		return self.env['sale.order.line'].browse(downpayment_lines + attachment_invoiceable)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	item = fields.Char('Item')
	attachment_period_ids = fields.One2many('sale.attachment.period', 'order_line_id', string="Attachment periods")
	qty_invoiced_progress = fields.Float('% Avancement', compute='_compute_invoice_progress')

	@api.depends('qty_invoiced')
	def _compute_invoice_progress(self):
		for rec in self:
			if rec.product_uom_qty:
				rec.qty_invoiced_progress = rec.qty_invoiced * 100 / rec.product_uom_qty
			else:
				rec.qty_invoiced_progress = 0

	def _prepare_invoice_line(self, **optional_values):
		res = super()._prepare_invoice_line(**optional_values)
		sale = self.order_id
		if sale.attachment_parent_id:
			date = sale.attachment_parent_id.date
			date_start = date.replace(day=1)
			date_end = date_start + relativedelta(months=1) - relativedelta(days=1)
			attachment = self.attachment_period_ids.filtered(lambda l: date_start <= l.date <= date_end)
			percentage = attachment[0].percentage if attachment else 0
			if percentage:
				res.update({
					'quantity': self.product_uom_qty * percentage / 100,
				})
		return res
