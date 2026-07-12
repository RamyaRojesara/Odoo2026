# -*- coding: utf-8 -*-
from odoo import models, api

class TransitOpsDashboard(models.AbstractModel):
    _name = 'transitops.dashboard'
    _description = 'TransitOps Dashboard API'

    @api.model
    def get_dashboard_data(self):
        """
        Returns structured JSON data matching the exact layout of the design reference.
        """
        return {
            'kpis': {
                'active_vehicles': {'value': 53, 'trend': '+12%', 'icon': 'car'},
                'available': {'value': 42, 'trend': '+5%', 'icon': 'check-circle'},
                'in_maintenance': {'value': '05', 'trend': '-2', 'icon': 'wrench'},
                'active_trips': {'value': 18, 'trend': '..', 'icon': 'route'},
                'pending_trips': {'value': '09', 'icon': 'clock'},
                'drivers_on_duty': {'value': 26, 'icon': 'id-card'},
                'utilization': {'value': '81%'}
            },
            'recent_trips': [
                {'id': 'TR001', 'vehicle': 'VAN-05', 'driver': 'Alex M.', 'driver_initial': 'A', 'status': 'On Trip', 'status_class': 'primary', 'eta': '45 min'},
                {'id': 'TR002', 'vehicle': 'BUS-12', 'driver': 'Sarah K.', 'driver_initial': 'S', 'status': 'Completed', 'status_class': 'success', 'eta': '10:42 AM'},
                {'id': 'TR003', 'vehicle': 'TRK-02', 'driver': 'John D.', 'driver_initial': 'J', 'status': 'Dispatched', 'status_class': 'info', 'eta': '1 hr 15 min'},
                {'id': 'TR004', 'vehicle': 'VAN-08', 'driver': 'Mike T.', 'driver_initial': 'M', 'status': 'Maintenance', 'status_class': 'warning', 'eta': 'Est. Tomorrow'},
                {'id': 'TR005', 'vehicle': 'VAN-11', 'driver': 'Elena R.', 'driver_initial': 'E', 'status': 'On Trip', 'status_class': 'primary', 'eta': '12 min'}
            ],
            'fleet_status': [
                {'label': 'Available', 'value': 65, 'color': '#4ade80'},
                {'label': 'On Trip', 'value': 25, 'color': '#60a5fa'},
                {'label': 'Maintenance', 'value': 8, 'color': '#f97316'},
                {'label': 'Retired', 'value': 2, 'color': '#4b5563'}
            ],
            'maintenance_schedule': [
                {'title': 'Oil Change', 'vehicle': 'VAN-08', 'desc': '150mi overdue', 'status': 'Urgent', 'icon': 'oil-can'},
                {'title': 'Tire Rotation', 'vehicle': 'TRK-02', 'desc': 'Due in 2 days', 'status': '', 'icon': 'truck'}
            ],
            'recent_activity': [
                {'title': 'Vehicle Assigned', 'desc': 'VAN-05 assigned to Driver Alex M.', 'time': '10 MIN AGO', 'color': '#60a5fa'},
                {'title': 'Trip Completed', 'desc': 'TR002 completed successfully.', 'time': '25 MIN AGO', 'color': '#4ade80'},
                {'title': 'Maintenance Alert', 'desc': 'Engine diagnostic code 0x4F on VAN-08.', 'time': '1 HR AGO', 'color': '#f97316'}
            ],
            'fuel_chart': {
                'labels': ['500', '1000', '1250L', '1500', '1680L', '2000'],
                'data': [10, 20, 15, 30, 25, 35]
            }
        }
