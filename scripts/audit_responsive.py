#!/usr/bin/env python3
"""
Auditoría responsive y de usabilidad táctil con Playwright.

Abre cada preview de componente en varios viewports, mide desbordamientos
horizontales no intencionales y verifica que todos los controles interactivos
(al menos 44×44 px, conforme WCAG 2.5.5).

Requiere Playwright instalado:
    source venv/bin/activate
    pip install -r requirements-dev.txt
    playwright install chromium

Uso:
    python3 scripts/audit_responsive.py
    python3 scripts/audit_responsive.py --base-url http://localhost:8000
    python3 scripts/audit_responsive.py --viewports 320x568,375x667,768x1024
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, cast

from playwright.sync_api import sync_playwright

from audit_components import list_previewable_components

# WCAG 2.5.5 recomienda 44×44 px para targets táctiles.
# Usamos el valor como estándar de la auditoría.
TOUCH_TARGET_SIZE = 44

# Viewports de referencia: móvil pequeño, móvil estándar, tablet vertical.
DEFAULT_VIEWPORTS: List[Tuple[int, int]] = [
    (320, 568),
    (375, 667),
    (768, 1024),
]


@dataclass
class ViewportResult:
    viewport_width: int
    viewport_height: int
    body_scroll_width: int
    overflows: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    small_controls: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
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
            r.body_scroll_width > r.viewport_width or r.overflows or r.small_controls
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


def audit_viewport(url: str, viewport_width: int, viewport_height: int) -> ViewportResult:
    """Abre la URL en un viewport y recolecta métricas de layout y usabilidad."""
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

        data = page.evaluate(f"""
            () => {{
                const footer = document.querySelector('footer');
                const footerRect = footer ? footer.getBoundingClientRect() : null;
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
                const smallControls = [];
                const selectors = 'a, button, input, select, textarea, summary';
                document.querySelectorAll(selectors).forEach(el => {{
                    const r = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    const isInteractive = style.pointerEvents !== 'none' && style.display !== 'none' && style.visibility !== 'hidden';
                    // Ignoramos elementos ocultos o no interactivos visualmente.
                    if (isInteractive && r.width > 0 && r.height > 0 && (r.width < {TOUCH_TARGET_SIZE} || r.height < {TOUCH_TARGET_SIZE})) {{
                        smallControls.push({{
                            tag: el.tagName,
                            text: el.textContent.trim().substring(0, 25) || el.getAttribute('aria-label') || '',
                            width: Math.round(r.width),
                            height: Math.round(r.height)
                        }});
                    }}
                }});
                return {{
                    viewportWidth: window.innerWidth,
                    viewportHeight: window.innerHeight,
                    bodyScrollWidth: document.body.scrollWidth,
                    overflows,
                    smallControls,
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
    parser = argparse.ArgumentParser(description="Auditoría responsive y táctil con Playwright")
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
    print("Auditoría responsive y táctil con Playwright")
    print(f"Umbral táctil: {TOUCH_TARGET_SIZE}×{TOUCH_TARGET_SIZE}px | Viewports: {len(viewports)}")
    print("=" * 70)

    total_overflows = 0
    total_small_controls = 0
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

        if result.has_failures:
            component_failures += 1
            print(f"   ❌ {component} tiene fallas")

    print("\n" + "=" * 70)
    print("Resumen:")
    print(f"   Componentes auditados: {len(components)}")
    print(f"   Viewports por componente: {len(viewports)}")
    print(f"   Desbordamientos totales: {total_overflows}")
    print(f"   Controles pequeños totales: {total_small_controls}")
    print(f"   Componentes con fallas: {component_failures}")

    if component_failures == 0:
        print("   ✅ Auditoría responsive superada")
        return 0
    print("   ❌ Se detectaron problemas de responsive o usabilidad táctil")
    return 1


if __name__ == "__main__":
    sys.exit(main())
