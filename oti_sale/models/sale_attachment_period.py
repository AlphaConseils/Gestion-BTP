from odoo import models, fields


class SaleAttachmentPeriod(models.Model):
	_name = 'sale.attachment.period'

	date = fields.Date('Period')
	order_line_id = fields.Many2one('sale.order.line', string='Order line', ondelete='cascade')
	percentage = fields.Float('Percentage')
