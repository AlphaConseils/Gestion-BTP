from odoo import models, _


class IrActionsReport(models.Model):
	_inherit = 'ir.actions.report'

	def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
		report_sudo = self._get_report(report_ref)
		if report_ref in ['oti_sale.report_sale_attachment_oti', 'oti_sale.action_report_attachment']:
			return super(IrActionsReport, report_sudo.with_context(landscape=True))._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
		return super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
