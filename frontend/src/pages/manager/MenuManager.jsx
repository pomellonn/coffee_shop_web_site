import { useState, useEffect } from "react";
import { getAllProducts } from "../../services/productService";
import { getShopMenu, addMenuItem, updateMenuItem, deleteMenuItem } from "../../services/managerService";

const ManagerMenu = () => {
    const [allProducts, setAllProducts] = useState([]);
    const [menu, setMenu] = useState([]);
    const [selectedProduct, setSelectedProduct] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            const products = await getAllProducts();
            const myMenu = await getShopMenu();
            setAllProducts(products);
            setMenu(myMenu);
        };
        fetchData();
    }, []);

    const handleAdd = async () => {
        if (!selectedProduct) {
            alert("Выберите продукт для добавления");
            return;
        }

        setLoading(true);
        try {
            const productId = Number(selectedProduct);
            if (!Number.isInteger(productId) || productId <= 0) {
                alert("Некорректный product_id");
                return;
            }

            const payload = {
                product_id: productId,
                is_available: true,
            };

            const newItem = await addMenuItem(payload);
            setMenu(prev => [...prev, newItem]);
            setSelectedProduct("");
        } catch (e) {
            alert("Ошибка добавления продукта в меню");
        } finally {
            setLoading(false);
        }
    };

    const handleToggleAvailable = async (item) => {
        setLoading(true);
        try {
            const updated = await updateMenuItem(item.shop_menu_id, { is_available: !item.is_available });
            setMenu(prev => prev.map(m => m.shop_menu_id === updated.shop_menu_id ? updated : m));
        } catch (e) {
            alert("Ошибка обновления статуса доступности");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (item) => {
        if (!window.confirm("Удалить продукт из меню?")) return;

        setLoading(true);
        try {
            await deleteMenuItem(item.shop_menu_id);
            setMenu(prev => prev.filter(m => m.shop_menu_id !== item.shop_menu_id));
        } catch (e) {
            alert("Ошибка удаления продукта");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen">
            <div className="px-10">
                {/* Заголовок */}
                <h1 className="text-3xl font-light text-gray-900 mb-12">
                    Меню вашей кофейни
                </h1>

                {/* Форма добавления продукта */}
                <div className="mb-14">
                    <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
                        Добавить продукт
                    </h2>
                    <div className="flex gap-3">
                        <select
                            className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors bg-white"
                            value={selectedProduct}
                            onChange={(e) => setSelectedProduct(e.target.value)}
                        >
                            <option value="">Выберите продукт</option>
                            {allProducts.map(p => (
                                <option key={p.product_id} value={p.product_id}>
                                    {p.name} ({p.product_type}, {p.price} руб.)
                                </option>
                            ))}
                        </select>

                        <button
                            className="px-6 py-3 bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                            onClick={handleAdd}
                            disabled={loading || !selectedProduct}
                        >
                            {loading ? "..." : "Добавить"}
                        </button>
                    </div>
                </div>

                {/* Заголовки таблицы */}
                <div className="flex items-center py-3 border-b border-gray-300 mb-1">
                    <span className="text-xs text-gray-500 uppercase tracking-wide w-1/5">
                        Продукт
                    </span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide w-2/5">
                        Описание
                    </span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide w-1/5 text-center">
                        Цена
                    </span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide w-1/5 text-center">
                        Доступность
                    </span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide w-1/5 text-center">
                        Действия
                    </span>
                </div>

                {/* Список меню */}
                <div className="space-y-1">
                    {menu.length > 0 ? (
                        menu.map(item => (
                            <div
                                key={item.shop_menu_id}
                                className="flex items-center py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors"
                            >
                                <span className="text-gray-900 text-sm w-1/5">
                                    {item.product.name}
                                </span>
                                <span className="text-gray-600 text-sm w-2/5">
                                    {item.product.description || "—"}
                                </span>
                                <span className="text-gray-900 text-sm w-1/5 text-center">
                                    {item.product.price} руб.
                                </span>
                                <div className="w-1/5 flex justify-center">
                                    <input
                                        type="checkbox"
                                        checked={item.is_available}
                                        onChange={() => handleToggleAvailable(item)}
                                        className="w-5 h-5 cursor-pointer accent-gray-900"
                                    />
                                </div>
                                <div className="w-1/5 flex justify-center">
                                    <button
                                        className="text-sm text-gray-400 hover:text-red-600 transition-colors"
                                        onClick={() => handleDelete(item)}
                                        disabled={loading}
                                    >
                                        Удалить
                                    </button>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="py-16 text-center text-gray-400 text-sm">
                            Меню пустое
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ManagerMenu;