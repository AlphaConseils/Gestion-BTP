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
	'depends': ['sale'],

	# always loaded
	'data': [
		'report/sale_order_template.xml',
		'report/sale_order_report.xml',

		'views/sale_order_views.xml',
	],
	# only loaded in demonstration mode
	'demo': [
	],
	'installable': True,
	'application': False,
	'auto_install': False,
	'license': 'LGPL-3',
}
