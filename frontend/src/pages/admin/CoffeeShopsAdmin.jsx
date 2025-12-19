import { useEffect, useState } from "react";
import {
    getAllShops,
    createShop,
    deleteShop,
    updateShop,
    getManagers,
    createUser,
    deleteUser,
    updateUser,
} from "../../services/adminService";

const CoffeeShopsAdmin = () => {
    const [shops, setShops] = useState([]);
    const [managers, setManagers] = useState([]);
    const [newShopName, setNewShopName] = useState("");
    const [newShopAddress, setNewShopAddress] = useState("");
    const [selectedManager, setSelectedManager] = useState("");

    const [newManagerName, setNewManagerName] = useState("");
    const [newManagerEmail, setNewManagerEmail] = useState("");
    const [passw, setPassw] = useState("");
    const [loading, setLoading] = useState(false);

    // Редактирование кофеен
    const [editingShopId, setEditingShopId] = useState(null);
    const [editShopName, setEditShopName] = useState("");
    const [editShopAddress, setEditShopAddress] = useState("");
    const [editShopManager, setEditShopManager] = useState("");

    // Редактирование менеджеров
    const [editingManagerId, setEditingManagerId] = useState(null);
    const [editManagerName, setEditManagerName] = useState("");
    const [editManagerEmail, setEditManagerEmail] = useState("");

    // Пагинация для кофейн
    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 20;

    useEffect(() => {
        fetchShops();
        fetchManagers();
    }, []);

    const fetchShops = async () => {
        try {
            const data = await getAllShops();
            setShops(data);
        } catch (e) {
            console.error("Ошибка получения кофейн", e);
        }
    };

    const fetchManagers = async () => {
        try {
            const data = await getManagers();
            setManagers(data);
        } catch (e) {
            console.error("Ошибка получения менеджеров", e);
        }
    };

    // Добавление кофейни
    const handleAddShop = async () => {
        if (!newShopName || !newShopAddress || !selectedManager) return;
        setLoading(true);
        try {
            const newShop = await createShop({
                name: newShopName,
                address: newShopAddress,
                manager_id: Number(selectedManager),
            });
            setShops(prev => [...prev, newShop]);
            setNewShopName("");
            setNewShopAddress("");
            setSelectedManager("");
        } catch (e) {
            console.error("Ошибка добавления кофейни", e);
        } finally {
            setLoading(false);
        }
    };

    // Удаление кофейни
    const handleDeleteShop = async (shopId) => {
        if (!window.confirm("Удалить кофейню?")) return;
        setLoading(true);
        try {
            await deleteShop(shopId);
            setShops(prev => prev.filter(s => s.shop_id !== shopId));
        } catch (e) {
            console.error("Ошибка удаления кофейни", e);
        } finally {
            setLoading(false);
        }
    };

    // Редактирование кофейни
    const startEditShop = (shop) => {
        setEditingShopId(shop.shop_id);
        setEditShopName(shop.name);
        setEditShopAddress(shop.address);
        setEditShopManager(shop.manager_id || "");
    };

    const cancelEditShop = () => {
        setEditingShopId(null);
        setEditShopName("");
        setEditShopAddress("");
        setEditShopManager("");
    };

    const saveEditShop = async (id) => {
        setLoading(true);
        try {
            const updated = await updateShop(id, {
                name: editShopName,
                address: editShopAddress,
                manager_id: Number(editShopManager),
            });
            setShops(prev => prev.map(s => (s.shop_id === id ? updated : s)));
            cancelEditShop();
        } finally {
            setLoading(false);
        }
    };

    // Добавление нового менеджера
    const handleAddManager = async () => {
        if (!newManagerName || !newManagerEmail || !passw) return;
        setLoading(true);
        try {
            const newM = await createUser({ 
                name: newManagerName, 
                email: newManagerEmail, 
                password: passw, 
                role: "manager" 
            });
            setManagers(prev => [...prev, newM]);
            setNewManagerName("");
            setNewManagerEmail("");
            setPassw("");
        } catch (e) {
            console.error("Ошибка добавления менеджера", e);
        } finally {
            setLoading(false);
        }
    };

    // Удаление manager
    const handleDeleteManager = async (id) => {
        if (!window.confirm("Удалить менеджера?")) return;
        setLoading(true);
        try {
            await deleteUser(id);
            setManagers(prev => prev.filter(s => s.user_id !== id));
        } catch (e) {
            console.error("Ошибка удаления", e);
        } finally {
            setLoading(false);
        }
    };

    // Редактирование менеджера
    const startEditManager = (manager) => {
        setEditingManagerId(manager.user_id);
        setEditManagerName(manager.name);
        setEditManagerEmail(manager.email);
    };

    const cancelEditManager = () => {
        setEditingManagerId(null);
        setEditManagerName("");
        setEditManagerEmail("");
    };

    const saveEditManager = async (id) => {
        setLoading(true);
        try {
            const updated = await updateUser(id, {
                name: editManagerName,
                email: editManagerEmail,
            });
            setManagers(prev => prev.map(m => (m.user_id === id ? updated : m)));
            cancelEditManager();
        } finally {
            setLoading(false);
        }
    };

    // Пагинация кофейн
    const indexOfLast = currentPage * pageSize;
    const indexOfFirst = indexOfLast - pageSize;
    const currentShops = shops.slice(indexOfFirst, indexOfLast);
    const totalPages = Math.ceil(shops.length / pageSize);

    return (
        <div className="min-h-screen">
            <div className="px-10">
                {/* Заголовок кофеен */}
                <h1 className="text-3xl font-light text-gray-900 mb-12">Сеть кофеен FLTR</h1>

                {/* Форма добавления кофейни */}
                <div className="mb-14">
                    <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
                        Добавить кофейню
                    </h2>
                    <div className="flex gap-3">
                        <input
                            type="text"
                            placeholder="Название"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={newShopName}
                            onChange={(e) => setNewShopName(e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Адрес"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={newShopAddress}
                            onChange={(e) => setNewShopAddress(e.target.value)}
                        />
                        <select
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors bg-white"
                            value={selectedManager}
                            onChange={(e) => setSelectedManager(e.target.value)}
                        >
                            <option value="">Выберите менеджера</option>
                            {managers.map(m => (
                                <option key={m.user_id} value={m.user_id}>
                                    {m.name} ({m.email})
                                </option>
                            ))}
                        </select>
                        <button
                            className="px-6 py-3 bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                            onClick={handleAddShop}
                            disabled={loading || !newShopName || !newShopAddress || !selectedManager}
                        >
                            {loading ? "..." : "Добавить"}
                        </button>
                    </div>
                </div>

                {/* Заголовки таблицы кофеен */}
                <div className="flex items-center justify-between py-3 border-b border-gray-300 mb-1">
                    <div className="flex items-center gap-8">
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-8">ID</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">Название</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">Адрес</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-40">Менеджер</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-48 text-center">Действия</span>
                    </div>
                </div>

                {/* Список кофеен */}
                <div className="space-y-1 mb-20">
                    {currentShops.length > 0 ? (
                        currentShops.map(shop => (
                            <div
                                key={shop.shop_id}
                                className="flex items-center justify-between py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors"
                            >
                                {editingShopId === shop.shop_id ? (
                                    <>
                                        <div className="flex gap-4 flex-1">
                                            <span className="text-sm text-gray-400 w-8">{shop.shop_id}</span>
                                            <input
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 flex-1"
                                                value={editShopName}
                                                onChange={e => setEditShopName(e.target.value)}
                                            />
                                            <input
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 flex-1"
                                                value={editShopAddress}
                                                onChange={e => setEditShopAddress(e.target.value)}
                                            />
                                            <select
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 w-40 bg-white"
                                                value={editShopManager}
                                                onChange={e => setEditShopManager(e.target.value)}
                                            >
                                                <option value="">Без менеджера</option>
                                                {managers.map(m => (
                                                    <option key={m.user_id} value={m.user_id}>
                                                        {m.name}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="flex items-center gap-3 w-48 justify-center">
                                            <button
                                                onClick={() => saveEditShop(shop.shop_id)}
                                                className="text-gray-400 hover:text-green-600 text-sm transition-colors"
                                            >
                                                Сохранить
                                            </button>
                                            <button
                                                onClick={cancelEditShop}
                                                className="text-gray-400 hover:text-red-600 text-sm transition-colors"
                                            >
                                                Отмена
                                            </button>
                                        </div>
                                    </>
                                ) : (
                                    <>
                                        <div className="flex items-center gap-8 flex-1">
                                            <span className="text-sm text-gray-400 w-8">{shop.shop_id}</span>
                                            <span className="text-gray-900 flex-1">{shop.name}</span>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <span className="text-gray-600 flex-1">{shop.address}</span>
                                            <span className="text-gray-600 w-40">
                                                {managers.find(m => m.user_id === shop.manager_id)?.name || "—"}
                                            </span>
                                            <div className="flex gap-3 w-48 justify-center">
                                                <button
                                                    onClick={() => startEditShop(shop)}
                                                    className="text-sm text-gray-400 hover:text-blue-600 transition-colors"
                                                >
                                                    Изменить
                                                </button>
                                                <button
                                                    className="text-sm text-gray-400 hover:text-red-600 transition-colors"
                                                    onClick={() => handleDeleteShop(shop.shop_id)}
                                                    disabled={loading}
                                                >
                                                    Удалить
                                                </button>
                                            </div>
                                        </div>
                                    </>
                                )}
                            </div>
                        ))
                    ) : (
                        <div className="py-16 text-center text-gray-400 text-sm">
                            Нет кофеен
                        </div>
                    )}
                </div>

                {/* Пагинация кофеен */}
                {totalPages > 1 && (
                    <div className="flex justify-center mb-20 gap-2">
                        {Array.from({ length: totalPages }, (_, i) => (
                            <button
                                key={i + 1}
                                onClick={() => setCurrentPage(i + 1)}
                                className={`px-3 py-1 text-sm transition-colors ${
                                    currentPage === i + 1
                                        ? "text-gray-900 font-medium border-b-2 border-gray-900"
                                        : "text-gray-400 hover:text-gray-600"
                                }`}
                            >
                                {i + 1}
                            </button>
                        ))}
                    </div>
                )}

                {/* Заголовок менеджеров */}
                <h1 className="text-3xl font-light text-gray-900 mb-12">Менеджеры</h1>

                {/* Форма добавления менеджера */}
                <div className="mb-14">
                    <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
                        Добавить менеджера
                    </h2>
                    <div className="flex gap-3">
                        <input
                            type="text"
                            placeholder="Имя"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={newManagerName}
                            onChange={(e) => setNewManagerName(e.target.value)}
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={newManagerEmail}
                            onChange={(e) => setNewManagerEmail(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Пароль"
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                            value={passw}
                            onChange={(e) => setPassw(e.target.value)}
                        />
                        <button
                            className="px-6 py-3 bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                            onClick={handleAddManager}
                            disabled={loading || !newManagerName || !newManagerEmail || !passw}
                        >
                            {loading ? "..." : "Добавить"}
                        </button>
                    </div>
                </div>

                {/* Заголовки таблицы менеджеров */}
                <div className="flex items-center justify-between py-3 border-b border-gray-300 mb-1">
                    <div className="flex items-center gap-8">
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-8">ID</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">Имя</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">Email</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-40 text-center">Действия</span>
                    </div>
                </div>

                {/* Список менеджеров */}
                <div className="space-y-1">
                    {managers.length > 0 ? (
                        managers.map(m => (
                            <div
                                key={m.user_id}
                                className="flex items-center justify-between py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors"
                            >
                                {editingManagerId === m.user_id ? (
                                    <>
                                        <div className="flex gap-4 flex-1">
                                            <span className="text-sm text-gray-400 w-8">{m.user_id}</span>
                                            <input
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 flex-1"
                                                value={editManagerName}
                                                onChange={e => setEditManagerName(e.target.value)}
                                            />
                                            <input
                                                type="email"
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 flex-1"
                                                value={editManagerEmail}
                                                onChange={e => setEditManagerEmail(e.target.value)}
                                            />
                                        </div>
                                        <div className="flex items-center gap-3 w-40 justify-center">
                                            <button
                                                onClick={() => saveEditManager(m.user_id)}
                                                className="text-gray-400 hover:text-green-600 text-sm transition-colors"
                                            >
                                                Сохранить
                                            </button>
                                            <button
                                                onClick={cancelEditManager}
                                                className="text-gray-400 hover:text-red-600 text-sm transition-colors"
                                            >
                                                Отмена
                                            </button>
                                        </div>
                                    </>
                                ) : (
                                    <>
                                        <div className="flex items-center gap-8 flex-1">
                                            <span className="text-sm text-gray-400 w-8">{m.user_id}</span>
                                            <span className="text-gray-900 flex-1">{m.name}</span>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <span className="text-gray-600 flex-1">{m.email}</span>
                                            <div className="flex gap-3 w-40 justify-center">
                                                <button
                                                    onClick={() => startEditManager(m)}
                                                    className="text-sm text-gray-400 hover:text-blue-600 transition-colors"
                                                >
                                                    Изменить
                                                </button>
                                                <button
                                                    className="text-sm text-gray-400 hover:text-red-600 transition-colors"
                                                    onClick={() => handleDeleteManager(m.user_id)}
                                                    disabled={loading}
                                                >
                                                    Удалить
                                                </button>
                                            </div>
                                        </div>
                                    </>
                                )}
                            </div>
                        ))
                    ) : (
                        <div className="py-16 text-center text-gray-400 text-sm">
                            Нет менеджеров
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CoffeeShopsAdmin;