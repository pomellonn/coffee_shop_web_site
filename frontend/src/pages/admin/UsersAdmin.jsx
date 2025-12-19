import { useEffect, useState } from "react";
import { getCustomers, deleteUser, updateUser } from "../../services/adminService";

const UsersAdmin = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(false);
    
    // Редактирование клиента
    const [editingCustomerId, setEditingCustomerId] = useState(null);
    const [editCustomerName, setEditCustomerName] = useState("");
    const [editCustomerEmail, setEditCustomerEmail] = useState("");

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        setLoading(true);
        try {
            const data = await getCustomers();
            setCustomers(data);
        } catch (e) {
            console.error("Ошибка получения клиентов", e);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteCustomer = async (id) => {
        if (!window.confirm("Удалить клиента?")) return;
        setLoading(true);
        try {
            await deleteUser(id);
            setCustomers(prev => prev.filter(c => c.user_id !== id));
        } catch (e) {
            console.error("Ошибка удаления клиента", e);
        } finally {
            setLoading(false);
        }
    };

    // Редактирование клиента
    const startEditCustomer = (customer) => {
        setEditingCustomerId(customer.user_id);
        setEditCustomerName(customer.name);
        setEditCustomerEmail(customer.email);
    };

    const cancelEditCustomer = () => {
        setEditingCustomerId(null);
        setEditCustomerName("");
        setEditCustomerEmail("");
    };

    const saveEditCustomer = async (id) => {
        setLoading(true);
        try {
            const updated = await updateUser(id, {
                name: editCustomerName,
                email: editCustomerEmail,
            });
            setCustomers(prev => prev.map(c => (c.user_id === id ? updated : c)));
            cancelEditCustomer();
        } catch (e) {
            console.error("Ошибка обновления клиента", e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen">
            <div className="px-10">
                {/* Заголовок */}
                <h1 className="text-3xl font-light text-gray-900 mb-12">Клиенты</h1>

                {/* Заголовки таблицы */}
                <div className="flex items-center justify-between py-3 border-b border-gray-300 mb-1">
                    <div className="flex items-center gap-8 flex-1">
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-8">ID</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-64">Имя</span>
                        <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">Email</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="text-xs text-gray-500 uppercase tracking-wide w-40 text-center">Действия</span>
                    </div>
                </div>

                {/* Список клиентов */}
                <div className="space-y-1">
                    {customers.length > 0 ? (
                        customers.map(c => (
                            <div
                                key={c.user_id}
                                className="flex items-center justify-between py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors"
                            >
                                {editingCustomerId === c.user_id ? (
                                    <>
                                        <div className="flex gap-4 flex-1">
                                            <span className="text-sm text-gray-400 w-8">{c.user_id}</span>
                                            <input
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 w-64"
                                                value={editCustomerName}
                                                onChange={e => setEditCustomerName(e.target.value)}
                                            />
                                            <input
                                                type="email"
                                                className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 flex-1"
                                                value={editCustomerEmail}
                                                onChange={e => setEditCustomerEmail(e.target.value)}
                                            />
                                        </div>
                                        <div className="flex items-center gap-3 w-40 justify-center">
                                            <button
                                                onClick={() => saveEditCustomer(c.user_id)}
                                                className="text-gray-400 hover:text-green-600 text-sm transition-colors"
                                            >
                                                Сохранить
                                            </button>
                                            <button
                                                onClick={cancelEditCustomer}
                                                className="text-gray-400 hover:text-red-600 text-sm transition-colors"
                                            >
                                                Отмена
                                            </button>
                                        </div>
                                    </>
                                ) : (
                                    <>
                                        <div className="flex items-center gap-8 flex-1">
                                            <span className="text-sm text-gray-400 w-8">{c.user_id}</span>
                                            <span className="text-gray-900 w-64">{c.name}</span>
                                            <span className="text-gray-600 flex-1">{c.email}</span>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <div className="flex gap-3 w-40 justify-center">
                                                <button
                                                    onClick={() => startEditCustomer(c)}
                                                    className="text-sm text-gray-400 hover:text-blue-600 transition-colors"
                                                >
                                                    Изменить
                                                </button>
                                                <button
                                                    className="text-sm text-gray-400 hover:text-red-600 transition-colors"
                                                    onClick={() => handleDeleteCustomer(c.user_id)}
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
                            Нет клиентов
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UsersAdmin;