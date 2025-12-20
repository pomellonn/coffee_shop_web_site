/**
 * Calculate total price for cart item including options
 * @param {Object} item - Cart item with unit_price, quantity, and selected_options
 * @returns {number} Total price
 */
export const calculateItemTotal = (item) => {
    const optionsPrice = (item.selected_options || []).reduce(
        (sum, opt) => sum + (opt.extra_price || 0), 0
    );
    return (item.unit_price + optionsPrice) * item.quantity;
};

/**
 * Calculate total price for all items in cart
 * @param {Array} cartItems - Array of cart items
 * @returns {number} Total price
 */
export const calculateCartTotal = (cartItems) => {
    return cartItems.reduce((total, item) => total + calculateItemTotal(item), 0);
};

/**
 * Calculate total with options for product modal
 * @param {number} basePrice - Base product price
 * @param {Array} attributes - Product attributes
 * @param {Object} selectedOptions - Selected option IDs by attribute type
 * @param {number} quantity - Quantity
 * @returns {number} Total price
 */
export const calculateProductTotal = (basePrice, attributes, selectedOptions, quantity) => {
    let total = basePrice;
    
    if (attributes && Array.isArray(attributes)) {
        attributes.forEach(attr => {
            const selectedOptionId = selectedOptions[attr.attribute_type_id];
            const option = attr.options?.find(opt => opt.option_id === selectedOptionId);
            if (option) {
                total += option.extra_price;
            }
        });
    }
    
    return total * quantity;
};
