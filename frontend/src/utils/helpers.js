
export const getImageUrl = (url) => {
    if (!url || url.trim() === '') return null;
    if (url.startsWith('http')) return url;
    return `http://localhost:8000${url}`;
};

export const formatPrice = (price) => {
    return `${price} ₽`;
};

// Словарь переводов для названий атрибутов
const attributeTranslations = {
    'milk': 'Молоко',
    'syrup': 'Сироп',
    'roast': 'Обжарка',
    'size': 'Размер'
};

// Функция перевода названий атрибутов
export const translateAttributeName = (name) => {
    const lowerName = name?.toLowerCase();
    return attributeTranslations[lowerName] || name;
};

