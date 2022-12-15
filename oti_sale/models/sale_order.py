from odoo import models, fields, api


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	project_subject = fields.Char("Objet du projet")
