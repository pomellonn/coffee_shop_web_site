import { useState } from "react";
import { getOneShopAnalytics } from "../../services/managerService";
import './styles.css'
import {
    Bar,
    Pie,
    Chart
} from "react-chartjs-2";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Tooltip,
    Legend,
    LineElement,
    PointElement,
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    ArcElement,
    Tooltip,
    Legend
);

const AnalyticsManager = () => {
    const [dateFrom, setDateFrom] = useState("");
    const [dateTo, setDateTo] = useState("");
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(false);
    const COLORS = [
        "rgba(54, 162, 235, 0.6)",
        "rgba(255, 99, 132, 0.6)",
        "rgba(255, 206, 86, 0.6)",
        "rgba(75, 192, 192, 0.6)",
        "rgba(153, 102, 255, 0.6)",
        "rgba(255, 159, 64, 0.6)",
    ];

    const loadAnalytics = async () => {
        if (!dateFrom || !dateTo) {
            alert("Выберите диапазон дат");
            return;
        }

        setLoading(true);
        try {
            const data = await getOneShopAnalytics(dateFrom, dateTo);
            setAnalytics(data);
        } catch (e) {
            alert("Ошибка загрузки аналитики");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container-fluid">
            <h2 className="mb-4">Аналитика кофейни</h2>

            {/* Filters */}
            <div className="row mb-3">
                <div className="col-md-3">
                    <label>From</label>
                    <input
                        type="date"
                        className="form-control"
                        value={dateFrom}
                        onChange={(e) => setDateFrom(e.target.value)}
                    />
                </div>

                <div className="col-md-3">
                    <label>To</label>
                    <input
                        type="date"
                        className="form-control"
                        value={dateTo}
                        onChange={(e) => setDateTo(e.target.value)}
                    />
                </div>

                <div className="col-md-3 d-flex align-items-end">
                    <button
                        className="btn btn-primary w-100"
                        onClick={loadAnalytics}
                        disabled={loading}
                    >
                        {loading ? "Загрузка..." : "Показать"}
                    </button>
                </div>
            </div>

            {analytics && (
                <>
                    {/* Monthly summary */}
                    <div className="row mb-4">
                        <div className="col-md-6">
                            <div className="card">
                                <div className="card-header">Аналитика по месяцам</div>
                                <div className="card-body">
                                    <table className="table table-bordered">
                                        <thead>
                                            <tr>
                                                <th>Месяц</th>
                                                <th>Заказы</th>
                                                <th>Выручка</th>
                                                <th>Средний чек</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {analytics.monthly_summary.map((m) => (
                                                <tr key={m.month}>
                                                    <td>{m.month}</td>
                                                    <td>{m.orders_count}</td>
                                                    <td>{m.revenue.toFixed(2)}</td>
                                                    <td>{m.avg_check.toFixed(2)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <div className="col-md-6">
                            <div className="card mb-3">
                                <div className="card-header">Заказы по месяцам</div>
                                <div className="card-body">
                                    <Bar
                                        data={{
                                            labels: analytics.monthly_summary.map((m) => m.month),
                                            datasets: [
                                                {
                                                    label: "Количество заказов",
                                                    data: analytics.monthly_summary.map(
                                                        (m) => m.orders_count
                                                    ),
                                                    backgroundColor: "rgba(54, 162, 235, 0.6)",
                                                },
                                            ],
                                        }}
                                    />
                                </div>
                            </div>

                            <div className="col-md-6">
                                <div className="card">
                                    <div className="card-header">
                                        Выручка по месяцам
                                    </div>
                                    <div className="card-body">
                                        <Chart
                                            type="bar"
                                            data={{
                                                labels: analytics.monthly_summary.map((m) => m.month),
                                                datasets: [
                                                    {
                                                        type: "bar",
                                                        label: "Выручка (столбцы)",
                                                        data: analytics.monthly_summary.map(
                                                            (m) => m.revenue
                                                        ),
                                                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                                                    },
                                                    {
                                                        type: "line",
                                                        label: "Выручка (линия)",
                                                        data: analytics.monthly_summary.map(
                                                            (m) => m.revenue
                                                        ),
                                                        borderColor: "rgba(255, 99, 132, 1)",
                                                        backgroundColor: "rgba(255, 99, 132, 0.3)",
                                                        tension: 0.3,
                                                        pointRadius: 4,
                                                        pointHoverRadius: 6,
                                                        fill: false,
                                                    },
                                                ],
                                            }}
                                            options={{
                                                responsive: true,
                                                plugins: {
                                                    legend: {
                                                        position: "top",
                                                    },
                                                    tooltip: {
                                                        mode: "index",
                                                        intersect: false,
                                                    },
                                                },
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Product ranking */}
                    <div className="row mb-4">
                        <div className="col-md-6">
                            <div className="card">
                                <div className="card-header">Рейтинг продуктов</div>
                                <div className="card-body">
                                    <table className="table table-bordered">
                                        <thead>
                                            <tr>
                                                <th>Продукт</th>
                                                <th>Продано</th>
                                                <th>Выручка</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {analytics.product_ranking.map((p) => (
                                                <tr key={p.product}>
                                                    <td>{p.product}</td>
                                                    <td>{p.total_sold}</td>
                                                    <td>{p.revenue.toFixed(2)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <div className="col-md-6">
                            <Bar
                                data={{
                                    labels: analytics.product_ranking.map((p) => p.product),
                                    datasets: [
                                        {
                                            label: "Продано",
                                            data: analytics.product_ranking.map((p) => p.total_sold),
                                            backgroundColor: COLORS,
                                        },
                                        {
                                            label: "Выручка",
                                            data: analytics.product_ranking.map((p) => p.revenue),
                                            backgroundColor: "rgba(54, 162, 235, 0.6)",
                                            
                                        },
                                    ],
                                }}
                            />
                        </div>
                    </div>

                    {/* Time period */}
                    <div className="row mb-4">
                        <div className="col-md-4">
                            <div className="card">
                                <div className="card-header">Продажи по времени суток</div>
                                <div className="card-body">
            <Pie
    data={{
        labels: analytics.time_period_sales.map((t) => t.period),
        datasets: [
            {
                data: analytics.time_period_sales.map((t) => t.orders),
                backgroundColor: COLORS.slice(
                    0,
                    analytics.time_period_sales.length
                ),
                borderColor: "#fff",
                borderWidth: 1,
            },
        ],
    }}
/>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default AnalyticsManager;