# -*- coding: utf-8 -*-
{
    'name': 'TransitOps Authentication & RBAC',
    'version': '1.0',
    'category': 'TransitOps/Core',
    'summary': 'Enterprise Authentication and Role-Based Access Control',
    'description': """
TransitOps Authentication Module
================================
* Custom pixel-perfect login screen
* Role-Based Access Control (RBAC) definitions
* Rate limiting and brute-force protection (Account lockout)
* Session security enhancements
    """,
    'author': 'TransitOps',
    'depends': ['base', 'web'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/login_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'transitops_auth/static/src/scss/login.scss',
            'transitops_auth/static/src/js/login.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
