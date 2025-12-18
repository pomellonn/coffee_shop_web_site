import { useState, useEffect } from "react";
import { getAllProducts, getShopMenu, addMenuItem, updateMenuItem, deleteMenuItem } from "../../services/managerService";
// import './styles.css';

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

            // Отправляем на сервер
            console.log("payload", payload);


            const newItem = await addMenuItem(payload);

            // Обновляем локальное состояние меню
            setMenu(prev => [...prev, newItem]);

            // Сбрасываем выбор
            setSelectedProduct("");
        } catch (e) {
            console.error(e.response?.data || e);

            console.log("RAW ERROR", e);
            console.log("RESPONSE", e.response);
            console.log("RESPONSE DATA", e.response?.data);
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
        <div className="container-fluid">
            <h2 className="mb-4">Меню вашей кофейни</h2>

            {/* Добавление продукта */}
            <div className="add-product row mb-4">
                <div className="col-md-6">
                    <select
                        className="form-control"
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
                </div>
                <div className="col-md-3">
                    <button className="btn btn-primary w-100" onClick={handleAdd} disabled={loading}>
                        {loading ? "Добавление..." : "Добавить"}
                    </button>
                </div>
            </div>

            {/* Таблица меню */}
            <table className="table table-bordered">
                <thead>
                    <tr>
                        <th>Продукт</th>
                        <th>Описание</th>
                        <th>Цена</th>
                        <th>Доступность</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    {menu.map(item => (
                        <tr key={item.shop_menu_id}>
                            <td>{item.product.name}</td>
                            <td>{item.product.description}</td>
                            <td>{item.product.price}</td>
                            <td>
                                <input
                                    type="checkbox"
                                    checked={item.is_available}
                                    onChange={() => handleToggleAvailable(item)}
                                />
                            </td>
                            <td>
                                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(item)}>
                                    Удалить
                                </button>
                            </td>
                        </tr>
                    ))}
                    {menu.length === 0 && (
                        <tr>
                            <td colSpan="5" style={{ textAlign: "center" }}>Меню пустое</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default ManagerMenu;