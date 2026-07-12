/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class TransitOpsDriverRegistry extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = useState({
            loading: true,
            drivers: [],
            kpis: {
                total: 0,
                available: 0,
                on_trip: 0,
                expiring: 0
            }
        });

        onWillStart(async () => {
            await this.loadDrivers();
        });
    }

    async loadDrivers() {
        this.state.loading = true;
        // Call the custom RPC method we added to the model
        const data = await this.orm.call(
            "transitops.driver",
            "get_driver_registry_data",
            []
        );
        this.state.kpis = data.kpis;
        this.state.drivers = data.drivers;
        this.state.loading = false;
    }

    async openCreateForm() {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "transitops.driver",
            views: [[false, "form"]],
            target: "current",
        });
    }

    async openDriverRecord(recordId) {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "transitops.driver",
            res_id: recordId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

TransitOpsDriverRegistry.template = "transitops_driver.registry_main";

registry.category("actions").add("transitops_driver.registry_main", TransitOpsDriverRegistry);
