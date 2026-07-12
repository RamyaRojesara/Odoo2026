# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class TransitOpsMaintenance(models.Model):
    _name = 'transitops.maintenance'
    _description = 'TransitOps Maintenance Management'
    _order = 'date_scheduled asc, create_date desc'

    name = fields.Char(string='Maintenance ID', required=True, copy=False, readonly=True, default=lambda self: 'New')
    
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    
    type = fields.Selection([
        ('routine', 'Routine Service'),
        ('repair', 'Repair'),
        ('urgent', 'Urgent Breakdown')
    ], string='Maintenance Type', required=True, default='routine')
    
    description = fields.Text(string='Work Details')
    cost = fields.Float(string='Maintenance Cost', default=0.0, tracking=True)
    date_scheduled = fields.Date(string='Scheduled Date', required=True, default=fields.Date.context_today)
    
    # State Machine
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='scheduled', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ Auto-generate MNXXXX Sequence """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('transitops.maintenance') or 'New'
        return super(TransitOpsMaintenance, self).create(vals_list)

    def action_start(self):
        """ 
        Business Action: Start Maintenance. 
        Locks the Vehicle state to 'maintenance'. 
        """
        for record in self:
            if record.status != 'scheduled':
                continue
            
            # Concurrency check
            if record.vehicle_id.status == 'in_trip':
                raise exceptions.UserError("Cannot start maintenance. The vehicle is currently on an active trip!")
                
            record.write({'status': 'in_progress'})
            # Block vehicle from dispatch
            record.vehicle_id.write({'status': 'maintenance'})

    def action_complete(self):
        """ 
        Business Action: Complete Maintenance. 
        Releases the Vehicle back to available. 
        """
        for record in self:
            record.write({'status': 'completed'})
            if record.vehicle_id.status == 'maintenance':
                record.vehicle_id.write({'status': 'available'})

    def action_cancel(self):
        """ Business Action: Cancel """
        for record in self:
            record.write({'status': 'cancelled'})
            # Only release if they were actually locked by this record
            if record.vehicle_id.status == 'maintenance':
                record.vehicle_id.write({'status': 'available'})
