{
	'name': "OTI Sale",

	'summary': """ OTI Sale management""",

	'description': """

	""",

	'author': "Alpha conseils",
	'website': "https://www.alphamada.com/",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
	# for the full list
	'category': 'Uncategorized',
	'version': '0.1',

	# any module necessary for this one to work correctly
	'depends': ['base', 'sale', 'account', 'stock'],

	# always loaded
	'data': [
		'security/ir.model.access.csv',
		'security/oti_groups.xml',
		'report/layout.xml',
		'report/sale_order_template.xml',
		'report/sale_attachment_template.xml',
		'report/sale_order_report.xml',
		'views/sale_order_views.xml',
		'views/stock_warehouse_views.xml',
		'views/product_product_views.xml',

	],
	'assets': {
		'web.assets_backend': [
			'oti_sale/static/src/css/sale_attachment.css',
			'oti_sale/static/src/components/**/*',
		],
		'web.report_assets_common': [
			'oti_sale/static/src/css/sale_attachment.css',
		],

	},
	'installable': True,
	'application': False,
	'auto_install': False,
	'license': 'LGPL-3',
}
