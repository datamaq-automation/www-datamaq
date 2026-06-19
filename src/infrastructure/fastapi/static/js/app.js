import { initChatwoot } from './modules/ChatwootManager.js';
import { initCookieManager } from './modules/CookieManager.js';
import { initOffcanvasMenu } from './modules/OffcanvasMenu.js';
import { loadThirdPartyScripts } from './modules/ThirdPartyScriptsManager.js';

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
});
