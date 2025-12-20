import { useEffect } from 'react';

/**
 * Hook for modal window behavior: close on ESC, lock body scroll
 * @param {Function} onClose - Callback to close modal
 */
export const useModal = (onClose) => {
    useEffect(() => {
        const handleEsc = (e) => {
            if (e.key === 'Escape') onClose();
        };
        
        document.body.style.overflow = 'hidden';
        window.addEventListener('keydown', handleEsc);
        
        return () => {
            window.removeEventListener('keydown', handleEsc);
            document.body.style.overflow = 'unset';
        };
    }, [onClose]);
};
