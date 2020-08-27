# -*- coding: utf-8 -*-
{
    'name': "surgi_expense_trust",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing sale_managementor apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_expense','product','event','sale','hr','oh_employee_creation_from_user'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/trust.xml',
        'views/product.xml',
        'views/to_approve_expenses.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
        'views/work_locations.xml',
        'views/hr_employee.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
