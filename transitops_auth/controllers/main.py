# -*- coding: utf-8 -*-
import odoo
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db

class TransitOpsAuth(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        
        # Intercept RBAC Role if provided during POST
        if request.httprequest.method == 'POST':
            rbac_role = request.params.get('rbac_role')
            login = request.params.get('login')
            
            # Standard Odoo authentication check happens here
            response = super(TransitOpsAuth, self).web_login(redirect=redirect, **kw)
            
            # If login was successful (session uid exists)
            if request.session.uid:
                user = request.env['res.users'].sudo().browse(request.session.uid)
                
                # Check if the user has the selected RBAC role
                # Note: 'rbac_role' from the form maps to group XML IDs.
                # Example: 'dispatcher' -> 'transitops_auth.group_dispatcher'
                role_group_xml_id = f"transitops_auth.group_{rbac_role}"
                
                try:
                    role_group = request.env.ref(role_group_xml_id)
                    if role_group.id not in user.groups_id.ids and not user.has_group('base.group_system'):
                        # Unauthorized role selection
                        request.session.logout(keep_db=True)
                        values = request.params.copy()
                        values['error'] = "Access Denied: You do not have the required permissions for the selected role."
                        return request.render('web.login', values)
                except ValueError:
                    # Group not found, fail safe
                    request.session.logout(keep_db=True)
                    values = request.params.copy()
                    values['error'] = "Invalid Role Selection."
                    return request.render('web.login', values)
            
            return response

        # GET request, just render standard (which is overridden by our view)
        return super(TransitOpsAuth, self).web_login(redirect=redirect, **kw)
