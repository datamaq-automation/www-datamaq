export const loadThirdPartyScripts = () => {
    console.debug("[ThirdPartyManager] Iniciando loadThirdPartyScripts...");
    try {
        const gaId = window.APP_CONFIG?.gaId;
        const clarityId = window.APP_CONFIG?.clarityId;
        
        // 1. Cargar Google Analytics
        if (gaId && gaId !== "None") {
            try {
                console.info("[ThirdPartyManager] Cargando GTAG:", gaId);
                const script = document.createElement("script");
                script.async = true;
                script.src = "https://www.googletagmanager.com/gtag/js?id=" + gaId;
                
                script.onerror = () => console.error("[ThirdPartyManager] Error de red al cargar GTAG.");
                script.onload = () => console.debug("[ThirdPartyManager] Script GTAG cargado.");
                
                document.head.appendChild(script);
                
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag("js", new Date());
                gtag("config", gaId);
            } catch (e) {
                console.error("[ThirdPartyManager] Fallo crítico al inicializar GTAG:", e);
            }
        }

        // 2. Cargar Microsoft Clarity
        if (clarityId && clarityId !== "None") {
            try {
                console.info("[ThirdPartyManager] Cargando Clarity:", clarityId);
                (function(c,l,a,r,i,t,y){
                    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                    t.onerror = () => console.error("[ThirdPartyManager] Error de red al cargar Clarity.");
                    t.onload = () => console.debug("[ThirdPartyManager] Script Clarity cargado.");
                    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
                })(window, document, "clarity", "script", clarityId);
            } catch (e) {
                console.error("[ThirdPartyManager] Fallo crítico al inicializar Clarity:", e);
            }
        }
    } catch (e) {
        console.error("[ThirdPartyManager] Error inesperado en el flujo de carga:", e);
    }
};
