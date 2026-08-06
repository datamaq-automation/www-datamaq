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

    // 3. Tracking WhatsApp FAB (GA4 + Google Ads; no-op sin consentimiento)
    try {
        const whatsappFab = document.querySelector('.c-whatsapp-fab');
        if (whatsappFab) {
            whatsappFab.addEventListener('click', () => {
                if (window.dataLayer && typeof window.dataLayer.push === 'function') {
                    window.dataLayer.push({
                        event: 'whatsapp_click'
                    });
                }

                // Google Ads: conversión de WhatsApp
                if (window.APP_CONFIG?.googleAdsWhatsappConversionId
                    && window.APP_CONFIG.googleAdsWhatsappConversionId !== "None"
                    && typeof window.gtag === 'function') {
                    window.gtag('event', 'conversion', {
                        send_to: window.APP_CONFIG.googleAdsWhatsappConversionId
                    });
                }
            });
        }
    } catch (e) {
        console.error("[App] Fallo crítico al inicializar tracking WhatsApp:", e);
    }
});
