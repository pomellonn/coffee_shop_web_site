import { useState } from "react";
import { getOneShopAnalytics } from "../../services/managerService";

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
        <div className="min-h-screen">
            <div className="px-10">
                {/* Заголовок */}
                <h1 className="text-3xl font-light text-gray-900 mb-12">
                    Аналитика кофейни
                </h1>

                {/* Форма выбора параметров */}
                <div className="mb-14">
                    <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
                        Параметры отчета
                    </h2>
                    <div className="flex gap-3">
                        <input
                            type="date"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={dateFrom}
                            onChange={(e) => setDateFrom(e.target.value)}
                            placeholder="От"
                        />

                        <input
                            type="date"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={dateTo}
                            onChange={(e) => setDateTo(e.target.value)}
                            placeholder="До"
                        />

                        <button
                            className="px-6 py-3 bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                            onClick={loadAnalytics}
                            disabled={loading}
                        >
                            {loading ? "..." : "Показать"}
                        </button>
                    </div>
                </div>

                {analytics && (
                    <>
                        {/* Аналитика по месяцам */}
                        <div className="mb-20">
                            <h2 className="text-2xl font-light text-gray-900 mb-8">
                                Аналитика по месяцам
                            </h2>

                            <div className="grid grid-cols-12 gap-8">
                                {/* Таблица */}
                                <div className="col-span-4">
                                    <div className="flex items-center justify-between py-3 border-b border-gray-300 mb-1">
                                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">
                                            Месяц
                                        </span>
                                        <span className="text-xs text-gray-500 uppercase tracking-wide w-20 text-right">
                                            Заказы
                                        </span>
                                        <span className="text-xs text-gray-500 uppercase tracking-wide w-24 text-right">
                                            Выручка
                                        </span>
                                        <span className="text-xs text-gray-500 uppercase tracking-wide w-24 text-right">
                                            Ср. чек
                                        </span>
                                    </div>

                                    <div className="space-y-1">
                                        {analytics.monthly_summary.map((m) => (
                                            <div
                                                key={m.month}
                                                className="flex items-center justify-between py-3 border-b border-gray-200"
                                            >
                                                <span className="text-gray-900 text-sm flex-1">{m.month}</span>
                                                <span className="text-gray-900 text-sm w-20 text-right">
                                                    {m.orders_count}
                                                </span>
                                                <span className="text-gray-900 text-sm w-24 text-right">
                                                    {m.revenue.toFixed(0)} ₽
                                                </span>
                                                <span className="text-gray-900 text-sm w-24 text-right">
                                                    {m.avg_check.toFixed(0)} ₽
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Графики */}
                                <div className="col-span-8 space-y-8">
                                    {/* График заказов */}
                                    <div className="border border-gray-200 p-6">
                                        <h3 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
                                            Заказы по месяцам
                                        </h3>
                                        <Bar
                                            data={{
                                                labels: analytics.monthly_summary.map((m) => m.month),
                                                datasets: [
                                                    {
                                                        label: "Количество заказов",
                                                        data: analytics.monthly_summary.map(
                                                            (m) => m.orders_count
                                                        ),
                                                        backgroundColor: "rgb(185, 201, 166)",
                                                    },
                                                ],
                                            }}
                                            options={{
                                                responsive: true,
                                                maintainAspectRatio: true,
                                                plugins: {
                                                    legend: {
                                                        display: false,
                                                    },
                                                },
                                            }}
                                        />
                                    </div>

                                    {/* График выручки */}
                                    <div className="border border-gray-200 p-6">
                                        <h3 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
                                            Выручка по месяцам
                                        </h3>
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
                                                        backgroundColor: "rgb(185, 201, 166)",
                                                    },
                                                    {
                                                        type: "line",
                                                        label: "Выручка (линия)",
                                                        data: analytics.monthly_summary.map(
                                                            (m) => m.revenue
                                                        ),
                                                        borderColor: "rgb(182, 166, 201)",
                                                        backgroundColor: "rgba(182, 166, 201, 0.3)",
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

                        {/* Рейтинг продуктов */}
                        <div className="mb-20">
                            <h2 className="text-2xl font-light text-gray-900 mb-8">
                                Рейтинг продуктов
                            </h2>

                            <div className="grid grid-cols-12 gap-8">
                                {/* Таблица */}
                                <div className="col-span-4">
                                    <div className="flex items-center justify-between py-3 border-b border-gray-300 mb-1">
                                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">
                                            Продукт
                                        </span>
                                        <span className="text-xs text-gray-500 uppercase tracking-wide w-24 text-right">
                                            Продано
                                        </span>
                                        <span className="text-xs text-gray-500 uppercase tracking-wide w-28 text-right">
                                            Выручка
                                        </span>
                                    </div>

                                    <div className="space-y-1">
                                        {analytics.product_ranking.map((p) => (
                                            <div
                                                key={p.product}
                                                className="flex items-center justify-between py-3 border-b border-gray-200"
                                            >
                                                <span className="text-gray-900 text-sm flex-1">{p.product}</span>
                                                <span className="text-gray-900 text-sm w-24 text-right">
                                                    {p.total_sold}
                                                </span>
                                                <span className="text-gray-900 text-sm w-28 text-right">
                                                    {p.revenue.toFixed(0)} ₽
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* График */}
                                <div className="col-span-8 border border-gray-200 p-6">
                                    <Bar
                                        data={{
                                            labels: analytics.product_ranking.map((p) => p.product),
                                            datasets: [
                                                {
                                                    label: "Продано",
                                                    data: analytics.product_ranking.map((p) => p.total_sold),
                                                    backgroundColor: "rgb(185, 201, 166)",
                                                },
                                                {
                                                    label: "Выручка",
                                                    data: analytics.product_ranking.map((p) => p.revenue),
                                                    backgroundColor: "rgb(182, 166, 201)",
                                                },
                                            ],
                                        }}
                                        options={{
                                            responsive: true,
                                            maintainAspectRatio: true,
                                            plugins: {
                                                legend: {
                                                    display: true,
                                                    position: "top",
                                                },
                                            },
                                        }}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Продажи по времени суток */}
                        <div className="mb-20">
                            <h2 className="text-2xl font-light text-gray-900 mb-8">
                                Продажи по времени суток
                            </h2>

                            <div className="max-w-md border border-gray-200 p-8">
                                <Pie
                                    data={{
                                        labels: analytics.time_period_sales.map((t) => t.period),
                                        datasets: [
                                            {
                                                data: analytics.time_period_sales.map((t) => t.orders),
                                                backgroundColor: [
                                                    "rgb(114, 153, 72)",
                                                    "rgb(12, 60, 124)",
                                                    "rgb(226, 168, 41)",
                                                ],
                                                borderWidth: 0,
                                            },
                                        ],
                                    }}
                                    options={{
                                        responsive: true,
                                        maintainAspectRatio: true,
                                        plugins: {
                                            legend: {
                                                display: true,
                                                position: "bottom",
                                            },
                                        },
                                    }}
                                />
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default AnalyticsManager;