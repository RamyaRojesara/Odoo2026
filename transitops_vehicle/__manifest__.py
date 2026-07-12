# -*- coding: utf-8 -*-
{
    'name': 'TransitOps Vehicle Registry',
    'version': '1.0',
    'category': 'TransitOps/Core',
    'summary': 'Enterprise Vehicle Ledger and State Management',
    'description': """
TransitOps Vehicle Registry
===========================
* Strict database constraints for unique registration
* Vehicle state machine (Available, In Trip, Maintenance, Retired)
* Kanban, List, and Form views optimized for UI/UX
    """,
    'author': 'TransitOps',
    'depends': ['base', 'web', 'transitops_auth', 'transitops_dashboard'],
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transitops_vehicle/static/src/scss/vehicle_registry.scss',
            'transitops_vehicle/static/src/xml/vehicle_registry.xml',
            'transitops_vehicle/static/src/js/vehicle_registry.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
