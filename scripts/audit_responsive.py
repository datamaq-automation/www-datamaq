#!/usr/bin/env python3
"""
Auditoría responsive y de usabilidad táctil con Playwright.

Abre cada preview de componente en un viewport móvil, ejecuta el mismo tipo de
mediciones que hace static/js/preview-telemetry.js, y reporta desbordamientos
horizontales y enlaces con área táctil inferior a 32px.

Requiere Playwright instalado:
    source venv/bin/activate
    pip install playwright
    playwright install chromium

Uso:
    python3 scripts/audit_responsive.py
    python3 scripts/audit_responsive.py --base-url http://localhost:8000 --viewport 390x844
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, cast

from playwright.sync_api import sync_playwright

from audit_components import list_previewable_components


@dataclass
class AuditResult:
    component: str
    viewport_width: int
    viewport_height: int
    body_scroll_width: int
    overflows: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    small_links: List[Dict[str, Any]] = cast(List[Dict[str, Any]], field(default_factory=list))
    footer_present: bool = False
    footer_height: Optional[int] = None


def audit_page(url: str, viewport_width: int, viewport_height: int) -> AuditResult:
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

        data = page.evaluate("""
            () => {
                const footer = document.querySelector('footer');
                const footerRect = footer ? footer.getBoundingClientRect() : null;
                const overflows = [];
                document.querySelectorAll('*').forEach(el => {
                    if (el.scrollWidth > el.clientWidth && el.clientWidth > 0) {
                        const style = window.getComputedStyle(el);
                        const parentStyle = el.parentElement ? window.getComputedStyle(el.parentElement) : null;
                        const isIntentionalScroll = style.overflowX === 'auto' || style.overflowX === 'scroll' ||
                            (parentStyle && (parentStyle.overflowX === 'auto' || parentStyle.overflowX === 'scroll'));
                        if (!isIntentionalScroll) {
                            overflows.push({
                                tag: el.tagName,
                                class: el.className || '',
                                scrollWidth: el.scrollWidth,
                                clientWidth: el.clientWidth,
                                text: el.textContent.trim().substring(0, 30)
                            });
                        }
                    }
                });
                const smallLinks = [];
                document.querySelectorAll('a').forEach(a => {
                    const r = a.getBoundingClientRect();
                    if (r.height > 0 && r.height < 32) {
                        smallLinks.push({
                            text: a.textContent.trim().substring(0, 25),
                            width: Math.round(r.width),
                            height: Math.round(r.height)
                        });
                    }
                });
                return {
                    viewportWidth: window.innerWidth,
                    viewportHeight: window.innerHeight,
                    bodyScrollWidth: document.body.scrollWidth,
                    overflows,
                    smallLinks,
                    footerPresent: !!footer,
                    footerHeight: footerRect ? Math.round(footerRect.height) : null
                };
            }
        """)

        browser.close()

        return AuditResult(
            component=url.split("/")[-1],
            viewport_width=data["viewportWidth"],
            viewport_height=data["viewportHeight"],
            body_scroll_width=data["bodyScrollWidth"],
            overflows=data["overflows"],
            small_links=data["smallLinks"],
            footer_present=data["footerPresent"],
            footer_height=data["footerHeight"],
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría responsive con Playwright")
    parser.add_argument("--base-url", default="http://localhost:8000", help="URL base del servidor")
    parser.add_argument(
        "--viewport",
        default="375x667",
        help="Viewport móvil en formato WIDTHxHEIGHT (default: 375x667)",
    )
    args = parser.parse_args()

    try:
        viewport_width, viewport_height = map(int, args.viewport.split("x"))
    except ValueError:
        print("❌ El parámetro --viewport debe tener el formato WIDTHxHEIGHT, ej: 375x667")
        return 1

    components = list_previewable_components()
    if not components:
        print("⚠️ No se encontraron componentes previewables.")
        return 0

    print("=" * 70)
    print(f"Auditoría responsive con Playwright - {viewport_width}x{viewport_height}")
    print("=" * 70)

    total_overflows = 0
    total_small_links = 0
    failures = 0

    for component in components:
        url = f"{args.base_url.rstrip('/')}/dev/preview/{component}"
        print(f"\n🔍 {component}")
        try:
            result = audit_page(url, viewport_width, viewport_height)
        except Exception as exc:  # noqa: BLE001
            print(f"   ❌ Error al cargar {url}: {exc}")
            failures += 1
            continue

        scroll_ok = result.body_scroll_width <= result.viewport_width
        print(f"   viewport: {result.viewport_width}x{result.viewport_height}")
        print(f"   body scrollWidth: {result.body_scroll_width}px {'✅' if scroll_ok else '❌'}")

        if result.footer_present:
            print(f"   footer height: {result.footer_height}px")

        if result.overflows:
            total_overflows += len(result.overflows)
            print(f"   ❌ Desbordamientos horizontales ({len(result.overflows)}):")
            for ov in result.overflows:
                print(f"      - <{ov['tag']}> {ov['class']}: {ov['scrollWidth']}px > {ov['clientWidth']}px")
        else:
            print("   ✅ Sin desbordamientos horizontales")

        if result.small_links:
            total_small_links += len(result.small_links)
            print(f"   ❌ Enlaces con touch target < 32px ({len(result.small_links)}):")
            for link in result.small_links:
                print(f"      - \"{link['text']}\": {link['width']}x{link['height']}px")
        else:
            print("   ✅ Todos los enlaces cumplen touch target ≥ 32px")

        if not scroll_ok or result.overflows or result.small_links:
            failures += 1

    print("\n" + "=" * 70)
    print("Resumen:")
    print(f"   Componentes auditados: {len(components)}")
    print(f"   Desbordamientos totales: {total_overflows}")
    print(f"   Enlaces pequeños totales: {total_small_links}")
    print(f"   Componentes con fallas: {failures}")

    if failures == 0:
        print("   ✅ Auditoría responsive superada")
        return 0
    print("   ❌ Se detectaron problemas de responsive o usabilidad táctil")
    return 1


if __name__ == "__main__":
    sys.exit(main())
