export const initChatwoot = (configElement) => {
    try {
        if (!configElement) {
            console.warn("[ChatwootManager] Elemento 'chatwoot-config' no encontrado.");
            return;
        }

        const BASE_URL = configElement.dataset.baseUrl;
        const WEBSITE_TOKEN = configElement.dataset.websiteToken;

        console.info("[ChatwootManager] Configuración detectada, inicializando...");
        window.chatwootSettings = {"position":"right","type":"standard","launcherTitle":""};
        (function(d,t) {
            var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
            g.src=BASE_URL+"/packs/js/sdk.js";
            g.async = true;
            s.parentNode.insertBefore(g,s);
            g.onload=function(){
                console.info("[ChatwootManager] SDK cargado correctamente.");
                window.chatwootSDK.run({
                    websiteToken: WEBSITE_TOKEN,
                    baseUrl: BASE_URL
                });
                window.openChatwoot = () => window.$chatwoot?.toggle("open");
                
                // Ocultar WhatsApp FAB si Chatwoot carga
                const whatsappFab = document.getElementById('whatsapp-fab');
                if (whatsappFab) {
                    whatsappFab.classList.add('hidden');
                    console.info("[ChatwootManager] WhatsApp FAB ocultado.");
                }
            };
            g.onerror = () => console.error("[ChatwootManager] Error al cargar SDK.");
        })(document,"script");
    } catch (error) {
        console.error("[ChatwootManager] Error crítico en initChatwoot:", error);
    }
};
