# -*- coding: utf-8 -*-
{
    'name': 'TransitOps Dashboard',
    'version': '1.0',
    'category': 'TransitOps/Core',
    'summary': 'Enterprise Dashboard for Fleet Managers',
    'description': """
TransitOps Dashboard Module
===========================
* Modern OWL Client Action
* Real-time KPI aggregation
* Chart.js visualizations
    """,
    'author': 'TransitOps',
    'depends': ['base', 'web', 'transitops_auth'],
    'data': [
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transitops_dashboard/static/src/scss/dashboard.scss',
            'transitops_dashboard/static/src/js/dashboard.js',
            'transitops_dashboard/static/src/xml/dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
