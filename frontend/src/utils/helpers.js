
export const getImageUrl = (url) => {
    if (!url || url.trim() === '') return null;
    if (url.startsWith('http')) return url;
    return `http://localhost:8000${url}`;
};

export const formatPrice = (price) => {
    return `${price} ₽`;
};

