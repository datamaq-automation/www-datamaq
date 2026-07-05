(function() {
    setTimeout(() => {
        console.clear();
        reportResponsive();
    }, 1000);

    window.addEventListener('resize', () => {
        console.clear();
        reportResponsive();
    });

    function reportResponsive() {
        const footer = document.querySelector('footer');
        const rect = footer ? footer.getBoundingClientRect() : null;
        const style = footer ? window.getComputedStyle(footer) : null;
        
        const overflows = [];
        // Buscar desbordamientos horizontales en todo el documento
        document.querySelectorAll('*').forEach(el => {
            if (el.scrollWidth > el.clientWidth && el.clientWidth > 0) {
                overflows.push({
                    etiqueta: el.tagName,
                    clase: el.className || 'Sin clase',
                    ancho_contenido_px: el.scrollWidth,
                    ancho_visible_px: el.clientWidth,
                    extracto: el.textContent.trim().substring(0, 30)
                });
            }
        });

        // Auditar la usabilidad de clicks en enlaces en toda la página
        const links = Array.from(document.querySelectorAll('a'));
        const touchTargets = links.map(a => {
            const r = a.getBoundingClientRect();
            return {
                label: a.textContent.trim().substring(0, 15),
                alto_px: Math.round(r.height),
                ancho_px: Math.round(r.width)
            };
        });
        const targetIssues = touchTargets.filter(t => t.alto_px > 0 && t.alto_px < 32);

        const groups = footer ? Array.from(footer.querySelectorAll('.c-home-footer__nav-group')).map((el, i) => {
            const elRect = el.getBoundingClientRect();
            const container = el.querySelector('.c-home-footer__links-container');
            const containerRect = container ? container.getBoundingClientRect() : null;
            return {
                nombre: el.querySelector('.c-home-footer__nav-title')?.textContent || 'Sin título',
                ancho_grupo_px: Math.round(elRect.width),
                ancho_links_container_px: containerRect ? Math.round(containerRect.width) : 'N/A',
                columnas_internas_links: container ? window.getComputedStyle(container).gridTemplateColumns : 'N/A'
            };
        }) : [];

        const info = {
            ruta_actual: window.location.pathname,
            ancho_viewport_px: window.innerWidth,
            alto_viewport_px: window.innerHeight,
            ancho_scroll_body_px: document.body.scrollWidth,
            elementos_con_desbordamiento_horizontal: overflows,
            medidas_footer: rect ? {
                ancho_px: Math.round(rect.width),
                alto_px: Math.round(rect.height)
            } : 'No renderizado',
            UX_enlaces: {
                total_enlaces_pagina: links.length,
                enlaces_con_area_pequena: targetIssues.length,
                listado_alertas_click: targetIssues.slice(0, 5)
            }
        };

        console.log("%c📱 TELEMETRÍA RESPONSIVE E INFORME UI/UX:", "color: #ff9f43; font-weight: bold; font-size: 14px;");
        console.log(JSON.stringify(info, null, 2));
        console.log("%c💡 Ajustá la pantalla en tu celular o emulador. Copiame este reporte completo cuando se vea mal.", "color: #2ec4b6; font-style: italic;");
    }
})();
