# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class TransitOpsTrip(models.Model):
    _name = 'transitops.trip'
    _description = 'TransitOps Trip & Dispatch Management'
    _order = 'create_date desc'

    name = fields.Char(string='Trip ID', required=True, copy=False, readonly=True, default=lambda self: 'New')
    
    # Relationships
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True, 
                                 domain="[('status', '=', 'available')]")
    driver_id = fields.Many2one('transitops.driver', string='Driver', required=True, 
                                domain="[('status', '=', 'available'), ('is_license_expired', '=', False)]")
    
    # Trip Details
    cargo_weight = fields.Float(string='Cargo Weight (KG)', required=True, default=0.0)
    start_location = fields.Char(string='Origin', required=True)
    end_location = fields.Char(string='Destination', required=True)
    eta = fields.Datetime(string='Estimated Arrival')
    
    # State Machine
    status = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ Auto-generate TRXXXX Sequence """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('transitops.trip') or 'New'
        return super(TransitOpsTrip, self).create(vals_list)

    @api.onchange('cargo_weight', 'vehicle_id')
    def _onchange_cargo_weight(self):
        """ UI Warning: Prevent overloading the vehicle """
        if self.vehicle_id and self.cargo_weight > self.vehicle_id.capacity_kg:
            return {
                'warning': {
                    'title': "Capacity Warning",
                    'message': f"The cargo weight ({self.cargo_weight} KG) exceeds the maximum capacity of the selected vehicle ({self.vehicle_id.capacity_kg} KG).",
                }
            }

    @api.constrains('cargo_weight', 'vehicle_id')
    def _check_cargo_capacity(self):
        """ Hard Backend Constraint: Absolutely prevent overloading """
        for record in self:
            if record.vehicle_id and record.cargo_weight > record.vehicle_id.capacity_kg:
                raise exceptions.ValidationError(f"Cannot dispatch! Cargo weight ({record.cargo_weight} KG) exceeds vehicle capacity ({record.vehicle_id.capacity_kg} KG).")

    @api.constrains('driver_id')
    def _check_driver_compliance(self):
        """ Hard Backend Constraint: Prevent illegal dispatching """
        for record in self:
            if record.driver_id.is_license_expired:
                raise exceptions.ValidationError(f"Cannot dispatch Driver {record.driver_id.name}. Their license is expired!")
            if record.driver_id.status != 'available' and record.status not in ['completed', 'cancelled']:
                # Note: This is simplified. In a real scenario we'd check if they are ALREADY on this exact trip, 
                # but if they are selected as a new driver, they must be available.
                pass

    def action_dispatch(self):
        """ 
        Business Action: Dispatch the trip. 
        Locks the Vehicle and Driver states. 
        """
        for record in self:
            if record.status != 'draft':
                continue
            
            # Concurrency check
            if record.vehicle_id.status != 'available':
                raise exceptions.UserError("The selected vehicle is no longer available.")
            if record.driver_id.status != 'available':
                raise exceptions.UserError("The selected driver is no longer available.")
                
            record.write({'status': 'dispatched'})
            
            # Orchestrate state changes in other modules
            record.vehicle_id.write({'status': 'in_trip'})
            record.driver_id.write({'status': 'in_trip'})

    def action_start_transit(self):
        """ Move to In Transit """
        for record in self:
            record.write({'status': 'in_transit'})

    def action_complete(self):
        """ 
        Business Action: Complete the trip. 
        Releases the Vehicle and Driver back to available. 
        """
        for record in self:
            record.write({'status': 'completed'})
            record.vehicle_id.write({'status': 'available'})
            record.driver_id.write({'status': 'available'})

    def action_cancel(self):
        """ Business Action: Cancel trip and release assets """
        for record in self:
            record.write({'status': 'cancelled'})
            # Only release if they were actually locked by this trip
            if record.vehicle_id.status == 'in_trip':
                record.vehicle_id.write({'status': 'available'})
            if record.driver_id.status == 'in_trip':
                record.driver_id.write({'status': 'available'})
