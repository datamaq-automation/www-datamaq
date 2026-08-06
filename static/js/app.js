import { initCookieManager } from './modules/CookieManager.js';
import { loadThirdPartyScripts } from './modules/ThirdPartyScriptsManager.js';
import { FormManager } from './modules/FormManager.js';

// Objeto de configuración global
export const APP_CONFIG = {
    apiUrl: window.APP_CONFIG?.contactApiUrl || '',
};

document.addEventListener("DOMContentLoaded", () => {
    // 1. Cookies
    try {
        initCookieManager(
            document.getElementById('cookie-banner'),
            document.getElementById('accept-cookies'),
            document.getElementById('reject-cookies'),
            loadThirdPartyScripts
        );
    } catch (e) {
        console.error("[App] Fallo crítico al inicializar CookieManager:", e);
    }

    // 2. Contact Form Manager
    try {
        const contactForm = document.querySelector('.c-contact form');
        if (contactForm && APP_CONFIG.apiUrl) {
            new FormManager(contactForm, APP_CONFIG.apiUrl);
        }
    } catch (e) {
        console.error("[App] Fallo crítico al inicializar FormManager:", e);
    }
});
