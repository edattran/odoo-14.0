# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Management',
    'version' : '14.0.1.0.0',
    'summary': 'Hospital Management Software',
    'sequence': 10,
    'description': """Hospital Management Software""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/',
    'depends' : [],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
