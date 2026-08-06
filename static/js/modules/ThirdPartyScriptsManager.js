export const loadThirdPartyScripts = () => {
    try {
        const gaId = window.APP_CONFIG?.gaId;
        const adsId = window.APP_CONFIG?.googleAdsId;
        const clarityId = window.APP_CONFIG?.clarityId;

        const hasGtag = (gaId && gaId !== "None") || (adsId && adsId !== "None");

        // 0. Shim global: dataLayer + gtag siempre disponibles tras el consentimiento
        //    (corrige bug: si solo hay Ads ID sin GA ID, gtag nunca existía)
        window.dataLayer = window.dataLayer || [];
        window.gtag = window.gtag || function(){ dataLayer.push(arguments); };

        // 1. Google Analytics + Google Ads (un único script gtag.js)
        if (hasGtag) {
            try {
                const primaryId = (gaId && gaId !== "None") ? gaId : adsId;
                const script = document.createElement("script");
                script.async = true;
                script.src = "https://www.googletagmanager.com/gtag/js?id=" + primaryId;
                script.onerror = () => console.error("[ThirdPartyManager] Error de red al cargar GTAG.");
                document.head.appendChild(script);

                window.gtag("js", new Date());
                if (gaId && gaId !== "None") window.gtag("config", gaId);
                if (adsId && adsId !== "None") window.gtag("config", adsId); // remarketing
            } catch (e) {
                console.error("[ThirdPartyManager] Fallo crítico al inicializar GTAG:", e);
            }
        }

        // 2. Cargar Microsoft Clarity
        if (clarityId && clarityId !== "None") {
            try {
                (function(c,l,a,r,i,t,y){
                    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                    t.onerror = () => console.error("[ThirdPartyManager] Error de red al cargar Clarity.");
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
