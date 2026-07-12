# -*- coding: utf-8 -*-
{
    'name': 'TransitOps Maintenance',
    'version': '1.0',
    'category': 'TransitOps/Operations',
    'summary': 'Vehicle health and maintenance tracking',
    'description': """
TransitOps Maintenance Management
=================================
* Tracks routine service and urgent repairs
* Logs financial costs associated with asset upkeep
* Locks vehicles out of dispatch when actively in repair
    """,
    'author': 'TransitOps',
    'depends': ['base', 'web', 'transitops_auth', 'transitops_dashboard', 'transitops_vehicle'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/maintenance_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transitops_maintenance/static/src/scss/maintenance_registry.scss',
            'transitops_maintenance/static/src/xml/maintenance_registry.xml',
            'transitops_maintenance/static/src/js/maintenance_registry.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
