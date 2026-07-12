/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class TransitOpsVehicleRegistry extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = useState({
            loading: true,
            vehicles: []
        });

        onWillStart(async () => {
            await this.loadVehicles();
        });
    }

    async loadVehicles() {
        this.state.loading = true;
        // Fetch vehicles from the backend
        this.state.vehicles = await this.orm.searchRead(
            "transitops.vehicle",
            [],
            ["id", "name", "status"]
        );
        this.state.loading = false;
    }

    // Open standard Odoo form to create a new vehicle
    async openCreateForm() {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "transitops.vehicle",
            views: [[false, "form"]],
            target: "current",
        });
    }

    // Open standard Odoo form to edit/view an existing vehicle
    async openVehicleRecord(recordId) {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "transitops.vehicle",
            res_id: recordId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

TransitOpsVehicleRegistry.template = "transitops_vehicle.registry_main";

registry.category("actions").add("transitops_vehicle.registry_main", TransitOpsVehicleRegistry);
