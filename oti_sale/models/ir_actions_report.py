from odoo import models, _


class IrActionsReport(models.Model):
	_inherit = 'ir.actions.report'

	def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
		if report_ref == 'oti_sale.report_sale_attachment_oti':
			return super(IrActionsReport, self.with_context(landscape=True))._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
		return super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
