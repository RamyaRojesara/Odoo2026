# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime

class ResUsers(models.Model):
    _inherit = 'res.users'

    failed_login_attempts = fields.Integer(string="Failed Login Attempts", default=0, copy=False)
    is_locked = fields.Boolean(string="Account Locked", default=False, copy=False)
    locked_until = fields.Datetime(string="Locked Until", copy=False)

    @api.model
    def check_credentials(self, password, env):
        # Override to implement lockout logic
        user = self.sudo().search([('id', '=', self.env.uid)])
        if user:
            if user.is_locked:
                if user.locked_until and user.locked_until > fields.Datetime.now():
                    raise exceptions.AccessDenied("Account is temporarily locked due to multiple failed login attempts. Please contact the administrator.")
                else:
                    # Lockout period expired
                    user.sudo().write({'is_locked': False, 'failed_login_attempts': 0, 'locked_until': False})

        try:
            super(ResUsers, self).check_credentials(password, env)
            # If successful, reset attempts
            if user:
                user.sudo().write({'failed_login_attempts': 0})
        except exceptions.AccessDenied as e:
            if user:
                attempts = user.failed_login_attempts + 1
                vals = {'failed_login_attempts': attempts}
                if attempts >= 5:
                    vals['is_locked'] = True
                    # Lock for 15 minutes
                    vals['locked_until'] = fields.Datetime.now() + fields.Datetime.timedelta(minutes=15)
                user.sudo().write(vals)
            raise e
