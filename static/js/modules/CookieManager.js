export const initCookieManager = (bannerElement, acceptBtn, rejectBtn, loadScripts) => {
    try {
        if (!bannerElement || !acceptBtn || !rejectBtn) {
            console.warn("[CookieManager] Elementos de cookies no encontrados.");
            return;
        }

        const consent = localStorage.getItem('userConsent');
        console.debug("[CookieManager] Estado de consentimiento:", consent);
        
        if (consent === 'accepted') {
            console.info("[CookieManager] Consentimiento ya aceptado.");
            loadScripts();
        } else if (consent === null) {
            console.debug("[CookieManager] Mostrando banner de cookies.");
            bannerElement.classList.add('is-visible');
        }

        acceptBtn.addEventListener('click', () => {
            console.info("[CookieManager] Usuario aceptó cookies.");
            localStorage.setItem('userConsent', 'accepted');
            bannerElement.classList.remove('is-visible');
            loadScripts();
        });

        rejectBtn.addEventListener('click', () => {
            console.info("[CookieManager] Usuario rechazó cookies.");
            localStorage.setItem('userConsent', 'rejected');
            bannerElement.classList.remove('is-visible');
        });
    } catch (error) {
        console.error("[CookieManager] Error accediendo a localStorage:", error);
        // Fallback seguro: cargar scripts
        loadScripts();
    }
};
