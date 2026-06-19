export const loadThirdPartyScripts = () => {
    console.debug("Ejecutando loadThirdPartyScripts...");
    const gaId = window.APP_CONFIG?.gaId;
    const clarityId = window.APP_CONFIG?.clarityId;
    
    // 1. Cargar Google Analytics
    if (gaId && gaId !== "None") {
        try {
            console.info("Iniciando carga de Google Analytics: " + gaId);
            const script1 = document.createElement("script");
            script1.async = true;
            script1.src = "https://www.googletagmanager.com/gtag/js?id=" + gaId;
            document.head.appendChild(script1);
            
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag("js", new Date());
            gtag("config", gaId);
        } catch (e) {
            console.error("Fallo crítico al inicializar GTAG:", e);
        }
    }

    // 2. Cargar Microsoft Clarity
    if (clarityId && clarityId !== "None") {
        try {
            console.info("Iniciando carga de Clarity: " + clarityId);
            (function(c,l,a,r,i,t,y){
                c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
            })(window, document, "clarity", "script", clarityId);
        } catch (e) {
            console.error("Fallo crítico al inicializar Clarity:", e);
        }
    }
};
