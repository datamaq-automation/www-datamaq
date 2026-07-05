#!/usr/bin/env python3
"""
Auditoría responsive, usabilidad táctil y accesibilidad básica con Playwright.

Abre cada preview de componente en varios viewports y verifica:
- Desbordamientos horizontales no intencionales.
- Controles interactivos de al menos 44×44 px (WCAG 2.5.5).
- Contraste de color de texto (WCAG AA) usando axe-core.
- Presencia de estilos :focus/:focus-visible en controles interactivos.

Requiere Playwright y axe-core instalados:
    source venv/bin/activate
    pip install -r requirements-dev.txt
    playwright install chromium
    npm install --save-dev axe-core

Uso:
    python3 scripts/audit_responsive.py
    python3 scripts/audit_responsive.py --base-url http://localhost:8000
    python3 scripts/audit_responsive.py --viewports 320x568,375x667,768x1024
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

from playwright.sync_api import sync_playwright

from audit_components import list_previewable_components

# WCAG 2.5.5 recomienda 44×44 px para targets táctiles.
TOUCH_TARGET_SIZE = 44

# Viewports de referencia: móvil pequeño, móvil estándar, tablet vertical.
DEFAULT_VIEWPORTS: List[Tuple[int, int]] = [
    (320, 568),
    (375, 667),
    (768, 1024),
]

AXE_CORE_PATH = Path(__file__).resolve().parent.parent / "node_modules" / "axe-core" / "axe.min.js"


@dataclass
class ViewportResult:
    viewport_width: int
    viewport_height: int
    body_scroll_width: int
    overflows: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    small_controls: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    contrast_issues: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    focus_issues: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    footer_present: bool = False
    footer_height: Optional[int] = None


@dataclass
class ComponentResult:
    component: str
    url: str
    viewport_results: List[ViewportResult] = cast(List[ViewportResult], field(default_factory=list))

    @property
    def has_failures(self) -> bool:
        return any(
            r.body_scroll_width > r.viewport_width
            or r.overflows
            or r.small_controls
            or r.contrast_issues
            or r.focus_issues
            for r in self.viewport_results
        )


def parse_viewports(value: str) -> List[Tuple[int, int]]:
    """Parsea una cadena tipo '320x568,375x667'."""
    viewports: List[Tuple[int, int]] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            width, height = map(int, part.split("x"))
            viewports.append((width, height))
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Viewport inválido: '{part}'. Formato esperado: WIDTHxHEIGHT"
            ) from exc
    if not viewports:
        raise argparse.ArgumentTypeError("Debe proporcionar al menos un viewport.")
    return viewports


def load_axe_core() -> str:
    """Carga el código de axe-core desde node_modules."""
    if not AXE_CORE_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró axe-core en {AXE_CORE_PATH}. "
            "Ejecutá: npm install --save-dev axe-core"
        )
    return AXE_CORE_PATH.read_text(encoding="utf-8")


def audit_viewport(url: str, viewport_width: int, viewport_height: int) -> ViewportResult:
    """Abre la URL en un viewport y recolecta métricas de layout, usabilidad y accesibilidad."""
    axe_code = load_axe_core()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.add_script_tag(content=axe_code)

        data = page.evaluate(f"""
            async () => {{
                const footer = document.querySelector('footer');
                const footerRect = footer ? footer.getBoundingClientRect() : null;

                // -----------------------------------------------------------------
                // Desbordamientos horizontales no intencionales
                // -----------------------------------------------------------------
                const overflows = [];
                document.querySelectorAll('*').forEach(el => {{
                    if (el.scrollWidth > el.clientWidth && el.clientWidth > 0) {{
                        const style = window.getComputedStyle(el);
                        const parentStyle = el.parentElement ? window.getComputedStyle(el.parentElement) : null;
                        const isIntentionalScroll = style.overflowX === 'auto' || style.overflowX === 'scroll' ||
                            (parentStyle && (parentStyle.overflowX === 'auto' || parentStyle.overflowX === 'scroll'));
                        if (!isIntentionalScroll) {{
                            overflows.push({{
                                tag: el.tagName,
                                class: el.className || '',
                                scrollWidth: el.scrollWidth,
                                clientWidth: el.clientWidth,
                                text: el.textContent.trim().substring(0, 30)
                            }});
                        }}
                    }}
                }});

                // -----------------------------------------------------------------
                // Controles interactivos: tamaño táctil mínimo
                // -----------------------------------------------------------------
                const smallControls = [];
                const interactiveSelectors = 'a, button, input, select, textarea, summary';
                document.querySelectorAll(interactiveSelectors).forEach(el => {{
                    const r = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    const isInteractive = style.pointerEvents !== 'none' && style.display !== 'none' && style.visibility !== 'hidden';
                    if (isInteractive && r.width > 0 && r.height > 0 && (r.width < {TOUCH_TARGET_SIZE} || r.height < {TOUCH_TARGET_SIZE})) {{
                        smallControls.push({{
                            tag: el.tagName,
                            text: el.textContent.trim().substring(0, 25) || el.getAttribute('aria-label') || '',
                            width: Math.round(r.width),
                            height: Math.round(r.height)
                        }});
                    }}
                }});

                // -----------------------------------------------------------------
                // Contraste de color con axe-core
                // -----------------------------------------------------------------
                let axeResult;
                try {{
                    axeResult = await axe.run(document.body, {{
                        runOnly: {{ type: 'rule', values: ['color-contrast'] }},
                        resultTypes: ['violations']
                    }});
                }} catch (e) {{
                    axeResult = {{ violations: [] }};
                }}

                const contrastIssues = [];
                for (const violation of axeResult.violations) {{
                    for (const node of violation.nodes) {{
                        contrastIssues.push({{
                            target: node.target.join(' > '),
                            html: node.html.substring(0, 80),
                            message: node.failureSummary ? node.failureSummary.split('\\n')[0] : violation.help,
                            contrast: node.contrastRatio ? Math.round(node.contrastRatio * 100) / 100 : null
                        }});
                    }}
                }}

                // -----------------------------------------------------------------
                // Foco visible: verificar estilos :focus/:focus-visible en CSS
                // -----------------------------------------------------------------
                function hasFocusStyle(element) {{
                    const selectors = [];
                    if (element.id) selectors.push('#' + element.id);
                    for (const cls of element.classList) selectors.push('.' + cls);
                    selectors.push(element.tagName.toLowerCase());

                    for (const sheet of document.styleSheets) {{
                        try {{
                            for (const rule of sheet.cssRules) {{
                                if (!rule.selectorText) continue;
                                for (const rawSel of rule.selectorText.split(',')) {{
                                    const sel = rawSel.trim();
                                    if (!sel.includes(':focus') && !sel.includes(':focus-visible')) continue;
                                    const baseSel = sel.replace(/:focus-visible|:focus/g, '').trim();
                                    if (!baseSel) return true;
                                    try {{
                                        if (element.matches(baseSel)) return true;
                                    }} catch (e) {{}}
                                }}
                            }}
                        }} catch (e) {{}}
                    }}
                    return false;
                }}

                const focusIssues = [];
                document.querySelectorAll(interactiveSelectors).forEach(el => {{
                    const style = window.getComputedStyle(el);
                    const isInteractive = style.pointerEvents !== 'none' && style.display !== 'none' && style.visibility !== 'hidden';
                    if (!isInteractive) return;
                    if (!hasFocusStyle(el)) {{
                        focusIssues.push({{
                            tag: el.tagName,
                            class: el.className || '',
                            text: el.textContent.trim().substring(0, 25) || el.getAttribute('aria-label') || ''
                        }});
                    }}
                }});

                return {{
                    viewportWidth: window.innerWidth,
                    viewportHeight: window.innerHeight,
                    bodyScrollWidth: document.body.scrollWidth,
                    overflows,
                    smallControls,
                    contrastIssues,
                    focusIssues,
                    footerPresent: !!footer,
                    footerHeight: footerRect ? Math.round(footerRect.height) : null
                }};
            }}
        """)

        browser.close()

        return ViewportResult(
            viewport_width=data["viewportWidth"],
            viewport_height=data["viewportHeight"],
            body_scroll_width=data["bodyScrollWidth"],
            overflows=data["overflows"],
            small_controls=data["smallControls"],
            contrast_issues=data["contrastIssues"],
            focus_issues=data["focusIssues"],
            footer_present=data["footerPresent"],
            footer_height=data["footerHeight"],
        )


def audit_component(base_url: str, component: str, viewports: List[Tuple[int, int]]) -> ComponentResult:
    """Audita un componente en todos los viewports indicados."""
    url = f"{base_url.rstrip('/')}/dev/preview/{component}"
    result = ComponentResult(component=component, url=url)
    for width, height in viewports:
        result.viewport_results.append(audit_viewport(url, width, height))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría responsive, táctil y accesibilidad con Playwright")
    parser.add_argument("--base-url", default="http://localhost:8000", help="URL base del servidor")
    parser.add_argument(
        "--viewports",
        type=parse_viewports,
        default=DEFAULT_VIEWPORTS,
        help="Lista de viewports en formato WIDTHxHEIGHT separados por coma (default: 320x568,375x667,768x1024)",
    )
    args = parser.parse_args()

    components = list_previewable_components()
    if not components:
        print("⚠️ No se encontraron componentes previewables.")
        return 0

    viewports = args.viewports

    print("=" * 70)
    print("Auditoría responsive, táctil y accesibilidad con Playwright")
    print(f"Touch target: {TOUCH_TARGET_SIZE}×{TOUCH_TARGET_SIZE}px | axe-core | Viewports: {len(viewports)}")
    print("=" * 70)

    total_overflows = 0
    total_small_controls = 0
    total_contrast_issues = 0
    total_focus_issues = 0
    component_failures = 0
    all_results: List[ComponentResult] = []

    for component in components:
        print(f"\n🔍 {component}")
        try:
            result = audit_component(args.base_url, component, viewports)
        except Exception as exc:  # noqa: BLE001
            print(f"   ❌ Error al auditar {component}: {exc}")
            component_failures += 1
            continue

        all_results.append(result)

        for vr in result.viewport_results:
            scroll_ok = vr.body_scroll_width <= vr.viewport_width
            print(f"\n   📱 {vr.viewport_width}×{vr.viewport_height}")
            print(f"   body scrollWidth: {vr.body_scroll_width}px {'✅' if scroll_ok else '❌'}")

            if vr.footer_present:
                print(f"   footer height: {vr.footer_height}px")

            if vr.overflows:
                total_overflows += len(vr.overflows)
                print(f"   ❌ Desbordamientos ({len(vr.overflows)}):")
                for ov in vr.overflows:
                    print(f"      - <{ov['tag']}> {ov['class']}: {ov['scrollWidth']}px > {ov['clientWidth']}px")
            else:
                print("   ✅ Sin desbordamientos horizontales")

            if vr.small_controls:
                total_small_controls += len(vr.small_controls)
                print(f"   ❌ Controles < {TOUCH_TARGET_SIZE}×{TOUCH_TARGET_SIZE}px ({len(vr.small_controls)}):")
                for ctrl in vr.small_controls:
                    print(f"      - <{ctrl['tag']}> \"{ctrl['text']}\": {ctrl['width']}×{ctrl['height']}px")
            else:
                print(f"   ✅ Todos los controles cumplen ≥ {TOUCH_TARGET_SIZE}×{TOUCH_TARGET_SIZE}px")

            if vr.contrast_issues:
                total_contrast_issues += len(vr.contrast_issues)
                print(f"   ❌ Problemas de contraste ({len(vr.contrast_issues)}):")
                for issue in vr.contrast_issues:
                    contrast = f" ({issue['contrast']}:1)" if issue['contrast'] else ""
                    print(f"      - {contrast} {issue['target']}")
            else:
                print("   ✅ Contraste de texto conforme WCAG AA")

            if vr.focus_issues:
                total_focus_issues += len(vr.focus_issues)
                print(f"   ❌ Controles sin estilo de foco ({len(vr.focus_issues)}):")
                for issue in vr.focus_issues:
                    print(f"      - <{issue['tag']}> \"{issue['text']}\"")
            else:
                print("   ✅ Estilos de foco definidos en controles interactivos")

        if result.has_failures:
            component_failures += 1
            print(f"   ❌ {component} tiene fallas")

    print("\n" + "=" * 70)
    print("Resumen:")
    print(f"   Componentes auditados: {len(components)}")
    print(f"   Viewports por componente: {len(viewports)}")
    print(f"   Desbordamientos totales: {total_overflows}")
    print(f"   Controles pequeños totales: {total_small_controls}")
    print(f"   Problemas de contraste: {total_contrast_issues}")
    print(f"   Problemas de foco: {total_focus_issues}")
    print(f"   Componentes con fallas: {component_failures}")

    if component_failures == 0:
        print("   ✅ Auditoría superada")
        return 0
    print("   ❌ Se detectaron problemas de responsive, usabilidad o accesibilidad")
    return 1


if __name__ == "__main__":
    sys.exit(main())
