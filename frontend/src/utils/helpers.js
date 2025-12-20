
export const getImageUrl = (url) => {
    if (!url || url.trim() === '') return null;
    if (url.startsWith('http')) return url;
    // If the URL is already an absolute path (starts with '/'), return it as-is
    // so the browser will request it using the current page scheme (https://...)
    // and nginx will proxy `/static/` to the backend. This avoids mixed-content
    // errors when the site is served over HTTPS.
    if (url.startsWith('/')) return url;

    // Otherwise assume it's a path relative to `/static/` on the server.
    return `/static${url.startsWith('/') ? '' : '/'}${url}`;
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

