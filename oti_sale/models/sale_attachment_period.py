from odoo import models, fields


class SAleAttachmentPeriodParent(models.Model):
	_name = 'sale.attachment.period.parent'
	_rec_name = 'date'

	name = fields.Char('Nom')
	note = fields.Html('Notes', default="<p></p>")
	sequence = fields.Char('Sequence')
	date = fields.Date('Période')
	state = fields.Selection([('draft', 'Brouillon'), ('validated', 'Validé')], 'Statut', default='draft')
	attachment_id = fields.Binary('Attachment File')
	attachment_name = fields.Char('Attachment')
	sale_id = fields.Many2one('sale.order')


class SaleAttachmentPeriod(models.Model):
	_name = 'sale.attachment.period'

	date = fields.Date('Period')
	order_line_id = fields.Many2one('sale.order.line', string='Order line', ondelete='cascade')
	percentage = fields.Float('Percentage')
