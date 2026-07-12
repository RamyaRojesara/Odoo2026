/** @odoo-module **/

import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/network/download";

export class TransitOpsDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: true,
            data: {}
        });

        onWillStart(async () => {
            // Load Chart.js dynamically from CDN for visualization
            await loadJS("https://cdn.jsdelivr.net/npm/chart.js");
            
            // Fetch structured data from the Python backend
            this.state.data = await this.orm.call(
                'transitops.dashboard',
                'get_dashboard_data',
                []
            );
            
            this.state.loading = false;
        });

        onMounted(() => {
            if (!this.state.loading) {
                this.renderFuelChart();
            }
        });
    }

    renderFuelChart() {
        const ctx = document.getElementById('fuelChart');
        if (!ctx) return;

        // Create gradient
        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 180);
        gradient.addColorStop(0, 'rgba(96, 165, 250, 0.5)'); // #60a5fa
        gradient.addColorStop(1, 'rgba(96, 165, 250, 0.0)');

        const chartData = this.state.data.fuel_chart;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Fuel Consumption',
                    data: chartData.data,
                    borderColor: '#60a5fa',
                    backgroundColor: gradient,
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#1f2937',
                    pointBorderColor: '#60a5fa',
                    pointRadius: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#374151',
                        titleColor: '#f3f4f6',
                        bodyColor: '#d1d5db'
                    }
                },
                scales: {
                    y: {
                        display: false, // Hide Y axis per design
                        beginAtZero: true
                    },
                    x: {
                        grid: {
                            display: true,
                            color: 'rgba(255,255,255,0.05)',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#6b7280',
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }
}

TransitOpsDashboard.template = "transitops_dashboard.main";

registry.category("actions").add("transitops_dashboard.main", TransitOpsDashboard);
