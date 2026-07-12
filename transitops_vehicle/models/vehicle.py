# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TransitOpsVehicle(models.Model):
    _name = 'transitops.vehicle'
    _description = 'TransitOps Vehicle Registry'
    _order = 'name asc'

    # Core details
    name = fields.Char(string='Registration Number', required=True, copy=False, index=True)
    make = fields.Char(string='Make', required=True)
    model = fields.Char(string='Model', required=True)
    year = fields.Integer(string='Year')
    capacity_kg = fields.Float(string='Capacity (KG)', required=True, default=0.0)
    
    # State machine
    status = fields.Selection([
        ('available', 'Available'),
        ('in_trip', 'On Trip'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired')
    ], string='Status', default='available', required=True, tracking=True)
    
    active = fields.Boolean(string='Active', default=True)

    # UI/Display helpers
    image_1920 = fields.Image(string="Vehicle Image")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Vehicle Registration Number must be strictly unique! A vehicle with this registration already exists.')
    ]

    def action_retire(self):
        """ Business Action: Retire a vehicle, removing it from active selection """
        for record in self:
            record.write({
                'status': 'retired',
                'active': False
            })

    def action_set_available(self):
        """ Business Action: Manually set a vehicle back to available """
        for record in self:
            record.write({
                'status': 'available'
            })
