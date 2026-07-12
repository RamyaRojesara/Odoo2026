# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class TransitOpsDriver(models.Model):
    _name = 'transitops.driver'
    _description = 'TransitOps Driver Management'
    _order = 'name asc'

    # Core details
    name = fields.Char(string='Full Name', required=True, index=True)
    user_id = fields.Many2one('res.users', string='Linked User', help="The portal or internal user account for this driver.")
    phone = fields.Char(string='Contact Number')
    
    # Compliance & Licensing
    license_number = fields.Char(string='License Number', required=True, copy=False)
    license_expiry = fields.Date(string='License Expiry Date', required=True)
    
    is_license_expired = fields.Boolean(
        string='License Expired', 
        compute='_compute_is_license_expired', 
        store=True,
        help="Automatically calculated based on the Expiry Date. If True, driver cannot be dispatched."
    )
    
    # State machine
    status = fields.Selection([
        ('available', 'Available'),
        ('in_trip', 'On Trip'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive')
    ], string='Status', default='available', required=True, tracking=True)
    
    active = fields.Boolean(string='Active', default=True)
    image_1920 = fields.Image(string="Driver Photo")
    
    # Refactored UI fields
    employee_id = fields.Char(string='Employee ID', copy=False, help="Unique employee identifier")
    category = fields.Selection([
        ('LMV', 'LMV'),
        ('HMV', 'HMV')
    ], string='Category', default='LMV')
    safety_score = fields.Integer(string='Safety Score', default=100, help="0 to 100")
    
    _sql_constraints = [
        ('license_uniq', 'unique (license_number)', 'The Driving License Number must be unique! A driver with this license already exists in the system.')
    ]

    @api.depends('license_expiry')
    def _compute_is_license_expired(self):
        """ Business Rule: Drivers with expired licenses cannot be dispatched """
        today = date.today()
        for record in self:
            if record.license_expiry:
                record.is_license_expired = record.license_expiry < today
            else:
                record.is_license_expired = True # Failsafe

    def action_suspend(self):
        """ Business Action: Suspend a driver """
        for record in self:
            record.write({
                'status': 'suspended'
            })

    def action_set_available(self):
        """ Business Action: Manually set a driver back to available """
        for record in self:
            # Prevent making them available if license is expired
            if record.is_license_expired:
                # We raise a user error if they try to bypass it via UI
                from odoo.exceptions import ValidationError
                raise ValidationError("Cannot mark driver as available. Their license is expired.")
            record.write({
                'status': 'available'
            })

    @api.model
    def get_driver_registry_data(self):
        """ Payload for the custom OWL Driver Registry UI """
        drivers = self.search_read([], ['id', 'name', 'employee_id', 'category', 'safety_score', 'status'])
        
        total = len(drivers)
        available = len([d for d in drivers if d['status'] == 'available'])
        on_trip = len([d for d in drivers if d['status'] == 'in_trip'])
        
        from datetime import timedelta
        today = date.today()
        thirty_days = today + timedelta(days=30)
        expiring = self.search_count([
            ('license_expiry', '>=', today), 
            ('license_expiry', '<=', thirty_days)
        ])
        
        return {
            'kpis': {
                'total': total,
                'available': available,
                'on_trip': on_trip,
                'expiring': expiring
            },
            'drivers': drivers
        }
