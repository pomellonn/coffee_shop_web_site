import { useEffect, useState } from "react";
import { getAllProducts } from "../../services/productService";
import { createProduct, deleteProduct, updateProduct } from "../../services/adminService";

const ProductsAdmin = () => {
  const [products, setProducts] = useState([]);
  const [newProductName, setNewProductName] = useState("");
  const [newProductPrice, setNewProductPrice] = useState("");
  const [newProductDescription, setNewProductDescription] = useState("");
  const [newProductType, setNewProductType] = useState("coffee");
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editPrice, setEditPrice] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editType, setEditType] = useState("coffee");
  
  const productTypes = [
    { value: "coffee", label: "Кофе" },
    { value: "non_coffee", label: "Не кофе" },
    { value: "bakery", label: "Выпечка" }
  ];

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const data = await getAllProducts();
      setProducts(data);
    } catch (e) {
      console.error("Ошибка получения продуктов", e);
    }
  };

  const handleAddProduct = async () => {
    if (!newProductName || !newProductPrice || !newProductDescription) return;
    setLoading(true);
    try {
      const newProd = await createProduct({
        name: newProductName,
        description: newProductDescription,
        image_url: "",
        product_type: newProductType,
        price: Number(newProductPrice)
      });
      setProducts(prev => [...prev, newProd]);
      setNewProductName("");
      setNewProductPrice("");
      setNewProductDescription("");
      setNewProductType("coffee");
    } catch (e) {
      console.error("Ошибка добавления продукта", e);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm("Удалить продукт?")) return;
    setLoading(true);
    try {
      await deleteProduct(productId);
      setProducts(prev => prev.filter(p => p.product_id !== productId));
    } catch (e) {
      console.error("Ошибка удаления продукта", e);
    } finally {
      setLoading(false);
    }
  };
  
  const startEdit = (p) => {
    setEditingId(p.product_id);
    setEditName(p.name);
    setEditPrice(p.price);
    setEditDescription(p.description || "");
    setEditType(p.product_type || "coffee");
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditName("");
    setEditPrice("");
    setEditDescription("");
    setEditType("coffee");
  };

  const saveEdit = async (id) => {
    setLoading(true);
    try {
      const updated = await updateProduct(id, {
        name: editName,
        price: Number(editPrice),
        description: editDescription,
        product_type: editType
      });

      setProducts(prev =>
        prev.map(p => (p.product_id === id ? updated : p))
      );
      cancelEdit();
    } catch (e) {
      console.error("Ошибка обновления продукта", e);
    } finally {
      setLoading(false);
    }
  };

  const getTypeLabel = (type) => {
    const found = productTypes.find(t => t.value === type);
    return found ? found.label : type;
  };

  return (
    <div className="min-h-screen">
       <div className="px-10"> 
        {/* Header */}
        <h1 className="text-3xl font-light text-gray-900 mb-12">Продукция кофеен</h1>

        {/* Add Product Form */}
        <div className="mb-14">
          <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">Добавить продукт</h2>
          <div className="space-y-3">
            <div className="flex gap-3">
              <input
                type="text"
                placeholder="Название"
                className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                value={newProductName}
                onChange={(e) => setNewProductName(e.target.value)}
              />
              <input
                type="number"
                placeholder="Цена"
                className="w-32 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors"
                value={newProductPrice}
                onChange={(e) => setNewProductPrice(e.target.value)}
              />
              <select
                className="px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors bg-white"
                value={newProductType}
                onChange={(e) => setNewProductType(e.target.value)}
              >
                {productTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex gap-3">
              <textarea
                placeholder="Описание"
                className="flex-1 px-4 py-3 border-b border-gray-300 focus:border-gray-900 outline-none transition-colors resize-none"
                rows="1"
                value={newProductDescription}
                onChange={(e) => setNewProductDescription(e.target.value)}
              />
              <button
                className="px-6 py-3 bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                onClick={handleAddProduct}
                disabled={loading || !newProductName || !newProductPrice || !newProductDescription}
              >
                {loading ? "..." : "Добавить"}
              </button>
            </div>
          </div>
        </div>

        {/* Table Header */}
        <div className="flex items-center justify-between py-3 border-b border-gray-300 mb-1">
          <div className="flex items-center gap-8">
            <span className="text-xs text-gray-500 uppercase tracking-wide w-8">ID</span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-48">Название</span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-32">Тип</span>
            <span className="text-xs text-gray-500 uppercase tracking-wide flex-1">Описание</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs text-gray-500 uppercase tracking-wide w-24 text-right">Цена</span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-32 text-center">Действия</span>
          </div>
        </div>
        
        {/* Products List */}
        <div className="space-y-1">
          {products.length > 0 ? (
            products.map(p => (
              <div
                key={p.product_id}
                className="flex items-center justify-between py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors"
              >
                {editingId === p.product_id ? (
                  <>
                    <div className="flex gap-4 flex-1">
                      <span className="text-sm text-gray-400 w-8">{p.product_id}</span>
                      <input
                        className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 w-48"
                        value={editName}
                        onChange={e => setEditName(e.target.value)}
                      />
                      <select
                        className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 w-32 bg-white"
                        value={editType}
                        onChange={e => setEditType(e.target.value)}
                      >
                        {productTypes.map(type => (
                          <option key={type.value} value={type.value}>
                            {type.label}
                          </option>
                        ))}
                      </select>
                      <textarea
                        className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 flex-1 resize-none"
                        rows="2"
                        value={editDescription}
                        onChange={e => setEditDescription(e.target.value)}
                      />
                    </div>
                    <div className="flex items-center gap-4">
                      <input
                        type="number"
                        className="border-b border-gray-300 focus:border-gray-900 outline-none px-2 py-1 w-24 text-right"
                        value={editPrice}
                        onChange={e => setEditPrice(e.target.value)}
                      />
                      <div className="flex gap-3 w-32 justify-center">
                        <button
                          onClick={() => saveEdit(p.product_id)}
                          className="text-gray-400 hover:text-green-600 text-sm transition-colors"
                        >
                          Сохранить
                        </button>
                        <button
                          onClick={cancelEdit}
                          className="text-gray-400 hover:text-red-600 text-sm transition-colors"
                        >
                          Отмена
                        </button>
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-8">
                      <span className="text-sm text-gray-400 w-8">{p.product_id}</span>
                      <span className="text-gray-900 w-48">{p.name}</span>
                      <span className="text-sm text-gray-600 w-20">{getTypeLabel(p.product_type)}</span>
                      <span className="text-sm text-gray-600 w-100 flex-1 ">{p.description}</span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-gray-900 font-medium w-24 text-right">{p.price} руб.</span>
                      <div className="flex gap-3 w-32 justify-center">
                        <button
                          onClick={() => startEdit(p)}
                          className="text-sm text-gray-400 hover:text-blue-600 transition-colors"
                        >
                          Изменить
                        </button>
                        <button
                          className="text-sm text-gray-400 hover:text-red-600 transition-colors"
                          onClick={() => handleDeleteProduct(p.product_id)}
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
              Нет продуктов
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductsAdmin;