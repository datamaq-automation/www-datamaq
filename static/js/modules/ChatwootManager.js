export const initChatwoot = (configElement) => {
    try {
        if (!configElement) {
            console.warn("[ChatwootManager] Elemento 'chatwoot-config' no encontrado.");
            return;
        }

        const BASE_URL = configElement.dataset.baseUrl;
        const WEBSITE_TOKEN = configElement.dataset.websiteToken;

        console.info("[ChatwootManager] Inicializando gestor de Chatwoot...");
        window.chatwootSettings = {
            position: "right",
            type: "standard",
            launcherTitle: "",
            showLauncher: true // Mostrar el launcher nativo una vez cargado
        };

        const loadChatwootSDK = () => {
            if (window.$chatwoot) {
                window.$chatwoot.toggle("open");
                return;
            }

            configElement.classList.add('is-loading');

            (function(d,t) {
                var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
                g.src=BASE_URL+"/packs/js/sdk.js";
                g.async = true;
                s.parentNode.insertBefore(g,s);
                
                g.onload = function() {
                    console.info("[ChatwootManager] SDK descargado, registrando widget...");
                    window.chatwootSDK.run({
                        websiteToken: WEBSITE_TOKEN,
                        baseUrl: BASE_URL
                    });
                    window.openChatwoot = () => window.$chatwoot?.toggle("open");
                };
                g.onerror = () => {
                    console.error("[ChatwootManager] Error de red al descargar SDK.");
                    configElement.classList.remove('is-loading');
                };
            })(document,"script");
        };

        // Escuchar cuando el chat esté completamente listo
        window.addEventListener("chatwoot:ready", function () {
            console.info("[ChatwootManager] Chatwoot listo. Ocultando botones estáticos.");
            
            // Guardar estado en sessionStorage para cargarlo automáticamente en páginas subsecuentes
            sessionStorage.setItem('chatwoot_active', 'true');
            
            // Ocultar botón estático y su spinner
            configElement.classList.remove('is-loading');
            configElement.style.setProperty('display', 'none', 'important');
            
            // Abrir la ventana de chat inmediatamente tras la primera interacción del usuario
            window.$chatwoot.toggle("open");
        });

        // Si ya interactuó con el chat en esta sesión de navegación, cargarlo automáticamente
        if (sessionStorage.getItem('chatwoot_active') === 'true') {
            console.info("[ChatwootManager] Sesión previa activa. Autocargando Chatwoot...");
            loadChatwootSDK();
        } else {
            // De lo contrario, esperar al clic del usuario (Lazy loading)
            configElement.addEventListener('click', (e) => {
                e.preventDefault();
                loadChatwootSDK();
            });
        }

    } catch (error) {
        console.error("[ChatwootManager] Error crítico en initChatwoot:", error);
    }
};
