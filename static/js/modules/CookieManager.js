export const initCookieManager = (bannerElement, acceptBtn, rejectBtn, loadScripts) => {
    try {
        if (!bannerElement || !acceptBtn || !rejectBtn) {
            return;
        }

        const consent = localStorage.getItem('userConsent');
        
        if (consent === 'accepted') {
            loadScripts();
        } else if (consent === null) {
            bannerElement.classList.add('is-visible');
            document.body.classList.add('has-consent-banner');
        }

        acceptBtn.addEventListener('click', () => {
            localStorage.setItem('userConsent', 'accepted');
            bannerElement.classList.remove('is-visible');
            document.body.classList.remove('has-consent-banner');
            loadScripts();
        });

        rejectBtn.addEventListener('click', () => {
            localStorage.setItem('userConsent', 'rejected');
            bannerElement.classList.remove('is-visible');
            document.body.classList.remove('has-consent-banner');
        });
    } catch (error) {
        console.error("[CookieManager] Error accediendo a localStorage:", error);
        // Fallback seguro: cargar scripts
        loadScripts();
    }
};
