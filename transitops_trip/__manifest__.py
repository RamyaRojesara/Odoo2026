# -*- coding: utf-8 -*-
{
    'name': 'TransitOps Trip & Dispatch',
    'version': '1.0',
    'category': 'TransitOps/Operations',
    'summary': 'Core dispatching engine with cross-module state locking',
    'description': """
TransitOps Trip & Dispatch Management
=====================================
* Orchestrates Vehicles and Drivers
* Enforces strict dispatch compliance rules
* Capacity warning UI feedback
* State machine integration (locks assets on dispatch, releases on complete)
    """,
    'author': 'TransitOps',
    'depends': ['base', 'web', 'transitops_auth', 'transitops_dashboard', 'transitops_vehicle', 'transitops_driver'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/trip_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
