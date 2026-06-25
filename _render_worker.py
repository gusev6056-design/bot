#!/usr/bin/env python3
"""
Standalone render worker — запускается как subprocess из card_generator_html.py.
Полностью изолирован от Flask/Gunicorn/greenlet окружения.
Читает HTML из stdin, пишет PNG в stdout.
"""
import sys

def main():
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 1120
    html  = sys.stdin.buffer.read().decode("utf-8", errors="replace")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-dev-shm-usage", "--single-process"]
        )
        try:
            page = browser.new_page(viewport={"width": width, "height": 800})
            page.set_content(html, wait_until="networkidle")
            try:
                page.wait_for_load_state("networkidle", timeout=3000)
            except Exception:
                pass
            body      = page.query_selector("body")
            png_bytes = body.screenshot()
            page.close()
            sys.stdout.buffer.write(png_bytes)
            sys.stdout.buffer.flush()
        finally:
            browser.close()

if __name__ == "__main__":
    main()
