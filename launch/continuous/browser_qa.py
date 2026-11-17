"""Bounded local browser QA. Starts/stops only owned fixture servers."""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=False)
report = {"checks": [], "pages": [], "external_requests": [], "page_errors": []}

def serve(name, port):
    log = open(OUT / f"{name}-server.txt", "w", encoding="utf-8")
    p = subprocess.Popen(["node", "launch/continuous/cli.js", "demo", "--dir", str(OUT / (name + "-state")), "--port", str(port)], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    url = f"http://127.0.0.1:{port}"
    for _ in range(100):
        if p.poll() is not None:
            raise RuntimeError("server exited; inspect " + name)
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                if r.status == 200:
                    return p, log, url
        except OSError:
            time.sleep(.1)
    p.terminate()
    raise RuntimeError("server not ready")

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel="msedge", headless=True)
    try:
        for name, size, port in [("desktop", {"width": 1365, "height": 1000}, 8791), ("mobile", {"width": 390, "height": 844}, 8792), ("ambiguous", {"width": 390, "height": 844}, 8793)]:
            proc, log, url = serve(name, port)
            context = browser.new_context(viewport=size, reduced_motion="reduce", service_workers="block")
            context.route("**/*", lambda route: route.continue_() if route.request.url.startswith(url + "/") else (report["external_requests"].append(route.request.url), route.abort()))
            page = context.new_page()
            page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
            try:
                page.goto(url)
                page.wait_for_selector('body[data-stage="AVAILABLE"]')
                assert page.locator("img").evaluate("img => img.complete && img.naturalWidth > 0")
                initial = page.request.get(url + "/api/state").json()
                page.screenshot(path=str(OUT / f"{name}-initial.png"), full_page=True)
                page.locator(".faults summary").click()
                page.select_option("#mode", "reject")
                page.locator("#advance").click()
                page.locator('#error').filter(has_text='rejected').wait_for()
                assert page.locator("body").get_attribute("data-stage") == "AVAILABLE"
                page.locator(".controls").screenshot(path=str(OUT / f"{name}-rejected.png"))
                report["checks"].append(name + ": rejection leaves reservation unchanged")
                page.locator(".faults summary").click()
                page.locator("#advance").click()
                page.wait_for_selector('body[data-stage="RESERVED"]')
                if name == "ambiguous":
                    page.locator(".faults summary").click()
                    page.select_option("#mode", "ambiguous")
                    page.locator("#advance").click()
                    page.locator('#advance').filter(has_text='Reconciliation hold').wait_for()
                    assert page.locator("#advance").is_disabled()
                    before = page.request.get(url + "/api/state").json()
                    page.reload()
                    page.locator('#advance').filter(has_text='Reconciliation hold').wait_for()
                    after = page.request.get(url + "/api/state").json()
                    assert before["pending"] == after["pending"]
                    page.locator(".controls").screenshot(path=str(OUT / "ambiguous-held-reloaded.png"))
                    report["checks"].append("ambiguous: durable same-byte hold survives browser reload")
                else:
                    for stage in ["PACKED", "SEALED", "TRANSFERRED", "OPENED", "WITHDRAWN"]:
                        page.locator("#advance").click()
                        page.wait_for_selector(f'body[data-stage="{stage}"]', timeout=60000)
                        current = page.request.get(url + "/api/state").json()
                        assert current["binding"] == initial["binding"]
                        assert all(current["provenance"].values())
                        page.locator(".controls").screenshot(path=str(OUT / f"{name}-{stage.lower()}.png"))
                    assert page.locator("#advance").is_disabled()
                    page.reload()
                    page.wait_for_selector('body[data-stage="WITHDRAWN"]')
                    page.locator(".evidence summary").click()
                    with page.expect_download() as dl:
                        page.get_by_text("Download current evidence JSON", exact=True).click()
                    download = OUT / f"{name}-download.json"
                    dl.value.save_as(download)
                    payload = json.loads(download.read_text())
                    assert payload["stage"] == "WITHDRAWN"
                    assert payload["binding"] == initial["binding"]
                    assert payload == page.request.get(url + "/api/evidence").json()
                    assert len(payload["history"]) == 5
                    report["checks"].append(name + ": all five signed transitions, binding/provenance, reload and exact evidence download")
                    page.screenshot(path=str(OUT / f"{name}-complete-evidence.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                report["checks"].append(name + ": no horizontal overflow; real candidate image decoded")
                report["pages"].append({"name": name, "url": url, "viewport": size})
            finally:
                context.close()
                proc.terminate()
                proc.wait(timeout=15)
                log.close()
    finally:
        browser.close()
assert not report["external_requests"]
assert not report["page_errors"]
report["result"] = "PASS"
(OUT / "report.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
