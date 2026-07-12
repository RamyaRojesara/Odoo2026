# -*- coding: utf-8 -*-
{
    'name': 'TransitOps Driver Management',
    'version': '1.0',
    'category': 'TransitOps/Core',
    'summary': 'Enterprise Driver Profiles and License Compliance',
    'description': """
TransitOps Driver Management
============================
* Strict compliance monitoring (License Expiration)
* State tracking (Available, In Trip, Suspended)
* Safety Officer and Dispatcher RBAC enforcement
* UI optimized for quick compliance checks (Ribbons, Badges)
    """,
    'author': 'TransitOps',
    'depends': ['base', 'web', 'transitops_auth', 'transitops_dashboard'],
    'data': [
        'security/ir.model.access.csv',
        'views/driver_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transitops_driver/static/src/scss/driver_registry.scss',
            'transitops_driver/static/src/xml/driver_registry.xml',
            'transitops_driver/static/src/js/driver_registry.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
