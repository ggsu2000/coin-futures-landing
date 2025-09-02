#!/usr/bin/env python3
import os, sys, xml.etree.ElementTree as ET
from datetime import datetime, timezone

BASE_URL = os.environ.get("BASE_URL", "https://xn--v69ap5s3zcl6hspa.com")
ROOT = os.getcwd()

def to_url(path: str) -> str:
    if path.endswith("index.html"):
        rel = "/" + os.path.relpath(os.path.dirname(path), ROOT).replace("\\", "/")
        if rel == "/.":
            return BASE_URL + "/"
        return BASE_URL + rel + "/"
    rel = "/" + os.path.relpath(path, ROOT).replace("\\", "/")
    return BASE_URL + rel

def lastmod(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def collect_html_files():
    htmls = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in (".git", "node_modules", "dist", "build")]
        for f in files:
            if f.endswith(".html"):
                htmls.append(os.path.join(root, f))
    return sorted(htmls)

def build_sitemap(files):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for f in files:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = to_url(f)
        ET.SubElement(url, "lastmod").text = lastmod(f)
        ET.SubElement(url, "changefreq").text = "weekly"
        ET.SubElement(url, "priority").text = "0.8" if not f.endswith("index.html") else "1.0"
    return ET.ElementTree(urlset)

def main():
    files = collect_html_files()
    if not files:
        print("No HTML files found; exiting.")
        sys.exit(0)
    tree = build_sitemap(files)
    out = os.path.join(ROOT, "sitemap.xml")
    tree.write(out, encoding="utf-8", xml_declaration=True)
    print(f"Generated sitemap with {len(files)} URLs at", out)

if __name__ == "__main__":
    main()
