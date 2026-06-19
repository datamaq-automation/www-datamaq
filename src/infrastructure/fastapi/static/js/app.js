console.log("[App] El script app.js se está ejecutando...");
import { initChatwoot } from './modules/ChatwootManager.js';
import { initCookieManager } from './modules/CookieManager.js';
import { loadThirdPartyScripts } from './modules/ThirdPartyScriptsManager.js';
import { FormManager } from './modules/FormManager.js';

// Objeto de configuración global
export const APP_CONFIG = {
    apiUrl: window.APP_CONFIG?.contactApiUrl || '',
};

document.addEventListener("DOMContentLoaded", () => {
    console.info("[App] Iniciando orquestación de componentes...");

    // 1. Chatwoot
    try {
        initChatwoot(document.getElementById('chatwoot-config'));
    } catch (e) { console.error("[App] Fallo crítico al inicializar Chatwoot:", e); }

    // 2. Cookies
    try {
        initCookieManager(
            document.getElementById('cookie-banner'),
            document.getElementById('accept-cookies'),
            document.getElementById('reject-cookies'),
            loadThirdPartyScripts
        );
    } catch (e) { console.error("[App] Fallo crítico al inicializar CookieManager:", e); }

    // 3. Contact Form Manager
    try {
        const contactForm = document.querySelector('.c-contact form');
        if (contactForm && APP_CONFIG.apiUrl) {
            new FormManager(contactForm, APP_CONFIG.apiUrl);
            console.info("[App] FormManager inicializado.");
        } else {
            console.warn("[App] FormManager no inicializado: falta formulario o API URL.");
        }
    } catch (e) { console.error("[App] Fallo crítico al inicializar FormManager:", e); }

    console.info("[App] Orquestación de componentes finalizada.");
});
