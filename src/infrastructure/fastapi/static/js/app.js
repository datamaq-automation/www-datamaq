import { initChatwoot } from './modules/ChatwootManager.js';
import { initCookieManager } from './modules/CookieManager.js';
import { initOffcanvasMenu } from './modules/OffcanvasMenu.js';
import { loadThirdPartyScripts } from './modules/ThirdPartyScriptsManager.js';
import { FormManager } from './modules/FormManager.js';

// Objeto de configuración global
export const APP_CONFIG = {
    apiUrl: window.APP_CONFIG?.contactApiUrl || '',
};

document.addEventListener("DOMContentLoaded", () => {
    // Chatwoot
    initChatwoot(document.getElementById('chatwoot-config'));

    // Cookies
    initCookieManager(
        document.getElementById('cookie-banner'),
        document.getElementById('accept-cookies'),
        document.getElementById('reject-cookies'),
        loadThirdPartyScripts
    );

    // Menu
    initOffcanvasMenu(
        document.getElementById('mainOffcanvas'),
        document.querySelector('[data-action="toggle-offcanvas"]'),
        document.querySelectorAll('[data-action="close-offcanvas"]')
    );

    // Contact Form Manager
    const contactForm = document.querySelector('.c-contact form');
    if (contactForm && APP_CONFIG.apiUrl) {
        new FormManager(contactForm, APP_CONFIG.apiUrl);
    }
});
