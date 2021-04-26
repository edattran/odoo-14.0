# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Business Game',
    'version' : '14.0.1.0.0',
    'summary': 'Business Game Software',
    'sequence': 1,
    'description': """Business Game""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/',
    'depends' : ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/start.xml',
        'views/purchase.xml',
        'views/mrp_production.xml'
        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
