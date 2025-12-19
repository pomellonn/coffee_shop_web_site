import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import { getTopClientsAnalytics, getClientsStats } from "../../services/adminService";

const ClientsAnalytics = () => {
    const [dateFrom, setDateFrom] = useState("");
    const [dateTo, setDateTo] = useState("");
    const [topClients, setTopClients] = useState([]);
    const [clientsStats, setClientsStats] = useState(null);
    const [loading, setLoading] = useState(false);
    const pieChartRef = useRef(null);
    const pieChartInstance = useRef(null);

    const loadClientsAnalytics = async () => {
        if (!dateFrom || !dateTo) {
            alert("Выберите диапазон дат");
            return;
        }

        setLoading(true);
        try {
            // Топ клиентов
            const clientsData = await getTopClientsAnalytics(dateFrom, dateTo);
            setTopClients(clientsData.top_clients);

            // Статистика новых/постоянных клиентов
            const pieData = await getClientsStats(dateFrom, dateTo);
            setClientsStats(pieData);

            if (pieChartInstance.current) {
                pieChartInstance.current.destroy();
            }

            const ctx = pieChartRef.current.getContext("2d");
            pieChartInstance.current = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: ["Новые клиенты", "Постоянные клиенты"],
                    datasets: [
                        {
                            data: [pieData.one_time, pieData.returning],
                            backgroundColor: [
                                "rgb(114, 153, 72)",
                                "rgb(12, 60, 124)",
                            ],
                            borderWidth: 0,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: "bottom",
                        },
                    },
                },
            });
        } catch (e) {
            console.error("Ошибка загрузки аналитики", e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen">
            <div className="px-10">
                {/* Заголовок */}
                <h1 className="text-3xl font-light text-gray-900 mb-12">
                    Аналитика клиентов
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
                            onClick={loadClientsAnalytics}
                            disabled={loading}
                        >
                            {loading ? "..." : "Показать"}
                        </button>
                    </div>
                </div>

                {topClients.length > 0 && (
                    <>
                        {/* Топ клиентов */}
                        <div className="mb-20">
                            <h2 className="text-2xl font-light text-gray-900 mb-8">
                                Топ клиентов
                            </h2>

                            {/* Заголовки таблицы */}
                            <div className="flex items-center py-3 border-b border-gray-300 mb-1">
                                <span className="text-xs text-gray-500 uppercase tracking-wide w-1/4">
                                    Email
                                </span>
                                <span className="text-xs text-gray-500 uppercase tracking-wide w-1/4 text-center">
                                    Покупки
                                </span>
                                <span className="text-xs text-gray-500 uppercase tracking-wide w-1/4 text-center">
                                    Потрачено
                                </span>
                                <span className="text-xs text-gray-500 uppercase tracking-wide w-1/4 text-center">
                                    Посещенные кофейни
                                </span>
                            </div>

                            {/* Список клиентов */}
                            <div className="space-y-1">
                                {topClients.map((c) => (
                                    <div
                                        key={c.email}
                                        className="flex items-center py-3 border-b border-gray-200 hover:bg-gray-50 transition-colors"
                                    >
                                        <span className="text-gray-900 text-sm w-1/4">{c.email}</span>
                                        <span className="text-gray-900 text-sm w-1/4 text-center">
                                            {c.total_purchases}
                                        </span>
                                        <span className="text-gray-900 text-sm w-1/4 text-center">
                                            {c.spent_money.toFixed(0)} руб.
                                        </span>
                                        <span className="text-gray-900 text-sm w-1/4 text-center">
                                            {c.shops_visited}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Новые vs Постоянные клиенты */}
                        {clientsStats && (
                            <div className="mb-20">
                                <h2 className="text-2xl font-light text-gray-900 mb-8">
                                    Новые vs Постоянные клиенты
                                </h2>

                                <div className="max-w-md border border-gray-200 p-8">
                                    <canvas ref={pieChartRef}></canvas>
                                </div>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default ClientsAnalytics;