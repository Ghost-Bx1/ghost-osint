#!/usr/bin/env python3
# ghost-osint.py - Extended OSINT Framework
# By Gh0st-Bx1 | github.com/Ghost-Bx1

import argparse
import json
import os
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

VERSAO = "2.0.0"


def _build_banner():
    import re as _re
    G = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    W = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "═" * IW; sp = " " * IW
    TL = "╔"; TR = "╗"; BL = "╚"; BR = "╝"; VB = "║"
    hl = "─" * 44; bar = "│"
    vl = lambda s: len(_re.sub(r"\x1b\[[0-9;]*m", "", s))

    def _row(s):
        n = vl(s); p = max(0, IW - n); l = p // 2; r = p - l
        return f"{G}{VB}{X}{' ' * l}{s}{' ' * r}{G}{VB}{X}"

    def _row_l(s):
        n = vl(s); p = max(0, IW - n - 2)
        return f"{G}{VB}{X}  {s}{' ' * p}{G}{VB}{X}"

    ga = [
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠿⠟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢀⣠⣤⣶⣶⣶⣶⣶⣶⣤⣀⠢⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⢀⣴⡿⢋⡴⢿⣿⣿⣿⣿⣿⣿⣿⢷⣦⡑⠈⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⢠⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣶⣦⣤⣤⣀⠉⠻⣿⣿⣿⡿⠿⢛⢛⡻⠿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⠿⠟⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣿⣿⣿⡿⠛⠛⠻⣿⣿⣿⡿⠛⠛⢿⣿⣿⣧⠉⠉⣁⣈⣉⣁⢀⣿⣿⢋⠄⣁⣴⣶⣄⠐⢌⢻⣿⣿{X}", ""),
        ("", f"{G}⡏⠀⣴⣦⣄⠢⡙⢿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⠅⠀⠀  ⢹⣿⡿⠁⠀⠀⠀⢹⣿⣿⡆⠀⣿⣿⣿⣿⣿⡟⠁⢀⣴⣿⣿⣿⣿⣷⡈⠎⢿⣿{X}", ""),
        ("", f"{G}⡇⠀⣿⣿⣿⣷⣌⠀⠙⢿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⢿⣿⡇⠁⢻⣿⣿⣿⡿⠁⢠⣾⣿⣿⣿⡿⢿⣿⣷⠀⠘⣿{X}", ""),
        ("", f"{G}⣇⠀⢿⣿⣿⡟⣿⣷⣄⠀⠙⢿⣿⡇⠀⣸⣿⣿⡿⣿⡀⠀⠀⠀  ⢸⣿⣧⠀⠀⠀⠀⣸⡈⣿⣷⠀⡈⣿⣿⡿⠁⢀⣾⣿⣿⢩⣿⠁⣾⣿⣿⡆⠀⢿{X}", ""),
        ("", f"{G}⣿⡀⠘⣿⣿⣿⡘⣿⣿⣷⣌⠂⠉⠁⢠⣿⣿⡟⣰⢿⣷⣤⣤⣴⣿⣿⣿⣷⣄⣠⣴⣿⣧⠸⣿⣧⡐⠢⠉⠁⢀⣾⣿⣿⡇⣼⣿⢸⣿⣿⣿⣇⠀⢸{X}", ""),
        ("", f"{G}⣿⣷⡀⠸⣿⣿⣧⠸⣿⣿⣿⣿⣶⣶⣿⣿⠏⡰⢃⣾⣿⣿⣿⣿⡏⠀⠈⣿⣿⣿⣿⣿⣏⠳⣘⣿⣿⣷⣶⣾⣿⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⠀⣿⣿⣿⡄⡿⢿⣿⣿⣿⣿⣿⣷⣾⣷⣿⣿⣿⣿⣿⣿⣧⣀⣠⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⠋⢉⠉⡉⠛⠿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⢀⣿⣿⣿⣧⢸⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣾⣿⡄⠈⠀⠀⠀⠀ ⣾{X}", ""),
        ("", f"{G}⣿⡟⠀⣸⣿⣿⣿⣿⣜⡇⢿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⠻⠇⠀⠰⠀⠀ ⣀⣾{X}", ""),
        ("", f"{G}⣿⠃⢠⣿⣿⠿⠿⠿⢿⣿⠸⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢣⢸⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⢰⠜⠋⠀⢀⡄⢰⣤⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠃⢻⣿⣿{X}", ""),
        ("", f"{G}⣿⣆⠠⠀⡀⠀⠁⣿⣿⠟⠀⣽⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⢃⣿⣿⣿⡟⣸⣿⣿⣿⣿⡿⠋⢠⢃⣾⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣷⣶⠆⡄⠈⢉⣠⣴⣾⣿⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠇⠛⢏⠉⠉⠁⠤⢊⣥⣾⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⢄⠀⢾⣿⣿⣿⣿⡇⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣶⣬⣭⣶⣾⣿⣿⠏⣼⣿⣿⣿⡇⣸⣿⣿⣿⠀⣰⣿⡁⢠⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣤⣀⡀⠀⠀⠉⠉⠁⢸⣿⣿⣿⢸⣿⣿⣿⣿⡹⣿⣿⣿⣿⣿⣿⣿⣿⠋⣼⣿⣿⣿⣿⠇⣿⣿⣿⣿⡀⠹⢿⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠛⠀⣼⣿⣿⣿⢸⣿⣿⢻⣿⣷⣌⠻⣿⣿⣿⣿⠟⣡⣾⣿⡟⣼⣿⣿⠀⣿⣿⣿⣿⣿⣶⣤⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⣴⣾⣿⣿⣿⡇⢸⣿⣿⣇⢻⣿⣿⣷⣦⣭⣭⣴⣾⣿⣿⣿⢡⣿⣿⣿⠀⣿⣿⣿⣿⣿⠿⠟⠃⡀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⡐⠠⢈⡉⠛⠛⠿⡇⢸⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⠀⣁⣤⡄⠀⣀⣒⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡌⠀⣦⠀⣼⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿⣄⡈⠛⠃⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢁⣤⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣦⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⠿⠿⣿⣿⣿⣿⠟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠈⣙⠛⠛⣛⣛⠛⠀⠻⢿⣿⣿⣿⣿⣿⣿⡃⢠⣤⠀⠀⣀⣉⣁⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣤⡀⢀⠈⢿⣿⣿⣿⣿⣷⣄⠁⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠁⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⢠⣿⣿⣿⣿⣿⠟⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⢸⣿⣿⣿⡿⢁⡄⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠰⠘⣿⣿⣿⠁⠎⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡑⠈⠻⠇⠈⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
    ]

    info = [
        f"{G}{N}GHOST-OSINT{X}",
        f"{Cy}v{VERSAO}  {D}Extended OSINT Framework{X}",
        f"{D}{hl}{X}",
        f"{W}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}--target --email --domain --breach --whois --certs{X}",
        f"{D}--github --paste --employees --subdomains --asn{X}",
        f"{D}--shodan --wayback --urlscan --username --buckets --all{X}",
    ]

    out = [f"{G}{TL}{eq}{TR}{X}", f"{G}{VB}{sp}{VB}{X}"]
    for left, center, right in ga:
        combined = left + center + right
        out.append(_row(combined))
    out.append(f"{G}{VB}{sp}{VB}{X}")
    for i in info:
        out.append(_row_l(i))
    out += [f"{G}{VB}{sp}{VB}{X}", f"{G}{BL}{eq}{BR}{X}"]
    return "\n".join(out)


BANNER = _build_banner()

C = {
    "R": "\033[91m", "G": "\033[92m", "Y": "\033[93m",
    "B": "\033[94m", "M": "\033[95m", "Cy": "\033[96m",
    "W": "\033[97m", "D": "\033[2m", "N": "\033[1m", "X": "\033[0m",
}

_findings = []


def _log(tag, color, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{C['D']}[{ts}]{C['X']} {color}[{tag}]{C['X']} {msg}")


def ok(msg):   _log("+", C["G"], msg)
def warn(msg): _log("!", C["Y"], msg)
def err(msg):  _log("-", C["R"], msg)
def info(msg): _log("*", C["Cy"], msg)


def _record(category, title, data, severity="info"):
    entry = {
        "tool": "ghost-osint",
        "version": VERSAO,
        "category": category,
        "title": title,
        "severity": severity,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _findings.append(entry)
    return entry


def _get(url, headers=None, timeout=10, verify=True):
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "Mozilla/5.0 (compatible; ghost-osint/2.0)",
        "Accept": "application/json, text/plain, */*",
    })
    ctx = ssl.create_default_context()
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            raw = r.read()
            try:
                return json.loads(raw)
            except Exception:
                return raw.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_reason": str(e.reason)}
    except Exception as e:
        return {"_error": str(e)}


# ---------------------------------------------------------------------------
# Shodan InternetDB (no API key)
# ---------------------------------------------------------------------------

def shodan_internetdb(ip, timeout=8):
    """Query Shodan InternetDB for open ports, CVEs and hostnames without an API key."""
    info(f"Shodan InternetDB for {ip} ...")
    data = _get(f"https://internetdb.shodan.io/{ip}", timeout=timeout)
    if isinstance(data, dict) and "_error" not in data and "_http_error" not in data:
        ports = data.get("ports", [])
        cves = list(data.get("vulns", []))
        hostnames = data.get("hostnames", [])
        tags = data.get("tags", [])
        cpes = data.get("cpes", [])
        ok(f"InternetDB {ip}: ports={ports}, CVEs={len(cves)}, hostnames={hostnames}")
        if cves:
            warn(f"CVEs: {', '.join(cves[:10])}")
        result = {
            "ip": ip, "ports": ports, "cves": cves,
            "hostnames": hostnames, "tags": tags, "cpes": cpes,
        }
        severity = "high" if cves else "info"
        _record("shodan", f"Shodan InternetDB: {ip}", result, severity)
        return result
    warn(f"InternetDB: no data for {ip}")
    return {}


# ---------------------------------------------------------------------------
# Certificate transparency
# ---------------------------------------------------------------------------

def crt_sh_certs(domain, timeout=15):
    info(f"Querying crt.sh for {domain} ...")
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    data = _get(url, timeout=timeout)
    if isinstance(data, dict) and "_error" in data:
        err(f"crt.sh error: {data['_error']}")
        return []
    if not isinstance(data, list):
        err("crt.sh returned unexpected data")
        return []

    seen = set()
    results = []
    for entry in data:
        name = entry.get("name_value", "")
        for n in name.splitlines():
            n = n.strip().lower()
            if n and n not in seen and domain in n:
                seen.add(n)
                results.append({
                    "name": n,
                    "issuer": entry.get("issuer_name", ""),
                    "not_before": entry.get("not_before", ""),
                    "not_after": entry.get("not_after", ""),
                })

    if results:
        ok(f"Found {len(results)} certificate entries for {domain}")
        for r in results[:10]:
            print(f"  {C['G']}>{C['X']} {r['name']}  {C['D']}(expires {r['not_after']}){C['X']}")
        if len(results) > 10:
            print(f"  {C['D']}... and {len(results) - 10} more{C['X']}")
        _record("certs", f"Certificate transparency: {domain}", results, "info")
    else:
        warn(f"No certificates found for {domain}")
    return results


# ---------------------------------------------------------------------------
# Wayback Machine URL harvest
# ---------------------------------------------------------------------------

def wayback_harvest(domain, limit=300, timeout=20):
    """Harvest URLs from Wayback Machine CDX API."""
    info(f"Wayback Machine URL harvest for {domain} ...")
    cdx_url = (
        f"https://web.archive.org/cdx/search/cdx"
        f"?url={urllib.parse.quote(domain)}/*"
        f"&output=json&fl=original&collapse=urlkey&limit={limit}"
    )
    data = _get(cdx_url, timeout=timeout)
    if not isinstance(data, list):
        warn(f"Wayback CDX returned no results for {domain}")
        return []
    urls = [row[0] for row in data[1:] if row]
    ok(f"Wayback Machine: {len(urls)} unique URLs for {domain}")
    _INTERESTING = [
        ".php?", "admin", "login", "api/", "token", "password", "backup",
        ".sql", ".env", ".git", "config", "setup", "install", "debug",
        "secret", "key", "credential", "passwd", ".bak", ".old",
    ]
    interesting = [u for u in urls if any(k in u.lower() for k in _INTERESTING)]
    if interesting:
        warn(f"Interesting Wayback URLs ({len(interesting)}):")
        for u in interesting[:10]:
            print(f"  {C['Y']}>>{C['X']} {u}")
    _record("wayback", f"Wayback URLs: {domain}",
            {"domain": domain, "total": len(urls),
             "interesting": interesting[:50], "sample": urls[:50]},
            "medium" if interesting else "info")
    return urls


# ---------------------------------------------------------------------------
# Breach check
# ---------------------------------------------------------------------------

def check_breach(email, api_key=None, timeout=10):
    info(f"Checking HaveIBeenPwned for {email} ...")
    headers = {
        "User-Agent": "ghost-osint/2.0",
        "Accept": "application/json",
    }
    if api_key:
        headers["hibp-api-key"] = api_key

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}?truncateResponse=false"
    data = _get(url, headers=headers, timeout=timeout)

    if isinstance(data, dict):
        code = data.get("_http_error")
        if code == 404:
            ok(f"{email} - not found in any breach")
            return []
        if code == 401:
            warn("HIBP API key required. Pass --hibp-key YOUR_KEY")
            return []
        if code == 429:
            warn("HIBP rate limit hit - wait 1.5s between requests")
            return []
        err(f"HIBP error: {data}")
        return []

    if isinstance(data, list):
        breaches = [b.get("Name", "?") for b in data]
        warn(f"{email} found in {len(breaches)} breach(es): {', '.join(breaches[:5])}")
        _record("breach", f"Email breach: {email}", {"email": email, "breaches": breaches}, "high")
        return breaches
    return []


# ---------------------------------------------------------------------------
# WHOIS / DNS
# ---------------------------------------------------------------------------

def whois_lookup(domain, timeout=10):
    info(f"WHOIS lookup for {domain} ...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        tld = domain.rsplit(".", 1)[-1].lower()
        server_map = {
            "com": "whois.verisign-grs.com", "net": "whois.verisign-grs.com",
            "org": "whois.pir.org", "io": "whois.nic.io",
            "gov": "whois.dotgov.gov", "edu": "whois.educause.edu",
            "co": "whois.nic.co", "uk": "whois.nic.uk",
            "br": "whois.registro.br", "de": "whois.denic.de",
        }
        server = server_map.get(tld, "whois.iana.org")
        sock.connect((server, 43))
        sock.sendall(f"{domain}\r\n".encode())
        resp = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
        sock.close()
        text = resp.decode("utf-8", errors="replace")

        fields = {}
        for line in text.splitlines():
            for key in ("Registrar:", "Creation Date:", "Updated Date:", "Expiry Date:",
                        "Registry Expiry Date:", "Registrant Organization:", "Registrant Country:"):
                if line.strip().startswith(key):
                    fields[key.rstrip(":")] = line.split(":", 1)[1].strip()

        if fields:
            ok(f"WHOIS data for {domain}:")
            for k, v in fields.items():
                print(f"  {C['Cy']}{k}:{C['X']} {v}")
            _record("whois", f"WHOIS: {domain}", {"domain": domain, **fields}, "info")
        else:
            warn(f"No WHOIS fields parsed for {domain}")
        return fields
    except Exception as e:
        err(f"WHOIS error: {e}")
        return {}


def dns_enum(domain, timeout=8):
    info(f"DNS enumeration for {domain} ...")
    results = {}
    record_types = [
        ("A", socket.AF_INET), ("AAAA", socket.AF_INET6),
    ]
    for rtype, family in record_types:
        try:
            addrs = socket.getaddrinfo(domain, None, family)
            ips = list({a[4][0] for a in addrs})
            if ips:
                results[rtype] = ips
                ok(f"{rtype}: {', '.join(ips)}")
        except Exception:
            pass

    try:
        mx_host = f"_smtp._tcp.{domain}"
        socket.getaddrinfo(mx_host, None)
    except Exception:
        pass

    if results:
        _record("dns", f"DNS records: {domain}", {"domain": domain, "records": results}, "info")
    return results


# ---------------------------------------------------------------------------
# ASN lookup
# ---------------------------------------------------------------------------

def asn_lookup(ip, timeout=8):
    info(f"ASN lookup for {ip} ...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(("whois.cymru.com", 43))
        sock.sendall(f" -v {ip}\r\n".encode())
        resp = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
        sock.close()
        lines = resp.decode("utf-8", errors="replace").strip().splitlines()
        if len(lines) >= 2:
            parts = [p.strip() for p in lines[-1].split("|")]
            result = {
                "ip": ip,
                "asn": parts[0] if len(parts) > 0 else "",
                "prefix": parts[2] if len(parts) > 2 else "",
                "country": parts[3] if len(parts) > 3 else "",
                "org": parts[6] if len(parts) > 6 else "",
            }
            ok(f"ASN: {result.get('asn')} | {result.get('org')} | {result.get('country')}")
            _record("asn", f"ASN: {ip}", result, "info")
            return result
    except Exception as e:
        err(f"ASN lookup error: {e}")
    return {}


# ---------------------------------------------------------------------------
# GitHub dorks
# ---------------------------------------------------------------------------

def github_dorks(domain, timeout=12):
    info(f"GitHub dork search for {domain} ...")
    dorks = [
        f"https://github.com/search?q={urllib.parse.quote(domain)}+password&type=code",
        f"https://github.com/search?q={urllib.parse.quote(domain)}+api_key&type=code",
        f"https://github.com/search?q={urllib.parse.quote(domain)}+secret&type=code",
        f"https://github.com/search?q={urllib.parse.quote(domain)}+token&type=code",
        f"https://github.com/search?q={urllib.parse.quote(domain)}+private_key&type=code",
        f"https://github.com/search?q={urllib.parse.quote(domain)}+database_url&type=code",
    ]
    warn(f"GitHub search requires browser authentication - dork URLs generated:")
    for d in dorks:
        print(f"  {C['Cy']}{d}{C['X']}")
    _record("github_dorks", f"GitHub dork URLs: {domain}", {"domain": domain, "dorks": dorks}, "info")
    return dorks


# ---------------------------------------------------------------------------
# Pastebin search
# ---------------------------------------------------------------------------

def pastebin_search(domain, timeout=12):
    info(f"Searching for {domain} leaks in public pastes ...")
    url = f"https://psbdmp.ws/api/v3/search/{urllib.parse.quote(domain)}"
    data = _get(url, timeout=timeout)
    if isinstance(data, dict) and "data" in data:
        pastes = data["data"]
        if pastes:
            warn(f"Found {len(pastes)} paste(s) mentioning {domain}")
            for p in pastes[:5]:
                pid = p.get("id", "")
                print(f"  {C['Y']}>>{C['X']} https://pastebin.com/{pid}")
            _record("pastebin", f"Pastebin leaks: {domain}",
                    {"domain": domain, "count": len(pastes), "pastes": [p.get("id") for p in pastes[:20]]},
                    "medium")
            return pastes
    elif isinstance(data, dict) and "_error" in data:
        warn(f"Pastebin search unavailable: {data['_error']}")
    else:
        ok(f"No pastes found for {domain}")
    return []


# ---------------------------------------------------------------------------
# Employee enumeration
# ---------------------------------------------------------------------------

def enumerate_employees(domain, timeout=10):
    info(f"Employee enumeration for {domain} ...")
    patterns = [
        ("LinkedIn", f"https://www.linkedin.com/company/{domain.split('.')[0]}/people/"),
        ("Hunter.io", f"https://hunter.io/domain-search?domain={domain}"),
        ("Clearbit", f"https://clearbit.com/companies/{domain}"),
        ("RocketReach", f"https://rocketreach.co/company?name={domain.split('.')[0]}"),
    ]
    results = []
    for source, url in patterns:
        warn(f"{source} - manual check required:")
        print(f"  {C['Cy']}{url}{C['X']}")
        results.append({"source": source, "url": url})

    common_email_formats = [
        f"firstname.lastname@{domain}",
        f"f.lastname@{domain}",
        f"firstname@{domain}",
        f"flastname@{domain}",
        f"firstname_lastname@{domain}",
    ]
    ok(f"Common email formats for {domain}:")
    for fmt in common_email_formats:
        print(f"  {C['D']}{fmt}{C['X']}")

    _record("employees", f"Employee enum: {domain}",
            {"domain": domain, "sources": results, "email_formats": common_email_formats}, "info")
    return results


# ---------------------------------------------------------------------------
# Subdomain brute-force
# ---------------------------------------------------------------------------

def subdomain_bruteforce(domain, wordlist=None, timeout=5, threads=20):
    info(f"Subdomain brute-force for {domain} ...")
    default_words = [
        "www", "mail", "ftp", "api", "dev", "staging", "test", "admin",
        "app", "portal", "vpn", "remote", "webmail", "smtp", "pop", "imap",
        "ns1", "ns2", "mx", "cdn", "static", "assets", "img", "images",
        "blog", "shop", "store", "support", "docs", "wiki", "git", "gitlab",
        "jenkins", "jira", "confluence", "grafana", "kibana", "dashboard",
        "beta", "alpha", "prod", "production", "internal", "intranet", "corp",
        "login", "auth", "oauth", "sso", "secure", "ssl", "demo", "sandbox",
        "api2", "v1", "v2", "api-dev", "api-staging", "api-prod",
        "mobile", "m", "wap", "cloud", "data", "db", "mysql", "redis",
        "monitor", "status", "health", "metrics", "logs", "elk", "splunk",
    ]
    words = wordlist or default_words
    found = []

    def check(sub):
        fqdn = f"{sub}.{domain}"
        try:
            socket.setdefaulttimeout(timeout)
            ip = socket.gethostbyname(fqdn)
            return fqdn, ip
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check, w): w for w in words}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                fqdn, ip = res
                ok(f"Found: {fqdn} -> {ip}")
                found.append({"subdomain": fqdn, "ip": ip})

    if found:
        _record("subdomains", f"Subdomains: {domain}", {"domain": domain, "found": found}, "info")
    else:
        warn(f"No subdomains resolved for {domain}")
    return found


# ---------------------------------------------------------------------------
# Subdomain takeover detection
# ---------------------------------------------------------------------------

_TAKEOVER_FINGERPRINTS = {
    "github.io": "There isn't a GitHub Pages site here",
    "githubusercontent.com": "There isn't a GitHub Pages site here",
    "herokuapp.com": "No such app",
    "netlify.app": "Not Found",
    "netlify.com": "Not Found",
    "shopify.com": "Sorry, this shop is currently unavailable",
    "fastly.net": "Fastly error: unknown domain",
    "pantheonsite.io": "The gods are wise, but do not know of the site",
    "readthedocs.io": "unknown to Read the Docs",
    "readme.io": "Project doesnt exist",
    "ghost.io": "The thing you were looking for is no longer here",
    "surge.sh": "project not found",
    "bitbucket.io": "Repository not found",
    "launchrock.com": "It looks like you may have taken a wrong turn",
    "zendesk.com": "Help Center Closed",
    "desk.com": "Sorry, We Couldn't Find That Page",
    "uservoice.com": "This UserVoice subdomain is currently available",
    "tumblr.com": "Whatever you were looking for doesn't currently exist",
    "wpengine.com": "The site you were looking for couldn't be found",
    "wordpress.com": "Do you want to register",
    "s3.amazonaws.com": "NoSuchBucket",
    "azurewebsites.net": "404 Web Site not found",
    "cloudapp.net": "404 Web Site not found",
    "trafficmanager.net": "404 Web Site not found",
    "azureedge.net": "404 Web Site not found",
    "acquia-test.co": "If you are an Acquia Cloud customer",
    "myshopify.com": "Sorry, this shop is currently unavailable",
    "feedpress.me": "The feed has not been found",
    "fly.dev": "404 Not Found",
    "render.com": "There's nothing here",
}


def check_subdomain_takeover(subdomains, timeout=8):
    """Check discovered subdomains for takeover via HTTP fingerprinting."""
    if not subdomains:
        return []
    info(f"Checking {len(subdomains)} subdomains for takeover ...")
    vulnerable = []

    def check_one(item):
        fqdn = item.get("subdomain", "")
        if not fqdn:
            return None
        for scheme in ("https", "http"):
            url = f"{scheme}://{fqdn}/"
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; ghost-osint/2.0)"
                })
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                    body = r.read(8192).decode("utf-8", errors="replace")
                    for svc, fp in _TAKEOVER_FINGERPRINTS.items():
                        if fp.lower() in body.lower():
                            return {"subdomain": fqdn, "service": svc, "fingerprint": fp}
                break
            except urllib.error.HTTPError as e:
                try:
                    body = e.read(4096).decode("utf-8", errors="replace")
                except Exception:
                    body = ""
                for svc, fp in _TAKEOVER_FINGERPRINTS.items():
                    if fp.lower() in body.lower():
                        return {"subdomain": fqdn, "service": svc, "fingerprint": fp}
                break
            except Exception:
                continue
        return None

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(check_one, s): s for s in subdomains}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                warn(f"Possible takeover: {res['subdomain']} -> {res['service']} ({res['fingerprint']!r})")
                vulnerable.append(res)

    if vulnerable:
        _record("takeover", "Subdomain takeover candidates",
                {"count": len(vulnerable), "findings": vulnerable}, "high")
    else:
        ok("No subdomain takeover indicators found")
    return vulnerable


# ---------------------------------------------------------------------------
# URLScan.io passive lookup
# ---------------------------------------------------------------------------

def urlscan_lookup(domain, timeout=12):
    """Passive URLScan.io search - no API key required."""
    info(f"URLScan.io passive lookup for {domain} ...")
    url = f"https://urlscan.io/api/v1/search/?q=domain:{urllib.parse.quote(domain)}&size=20"
    data = _get(url, timeout=timeout)
    if isinstance(data, dict) and "results" in data:
        results = data["results"]
        ok(f"URLScan.io: {len(results)} scans for {domain}")
        entries = []
        for r in results[:15]:
            page = r.get("page", {})
            task = r.get("task", {})
            scan_id = r.get("_id", "")
            entry = {
                "url": page.get("url", ""),
                "ip": page.get("ip", ""),
                "country": page.get("country", ""),
                "server": page.get("server", ""),
                "asn_name": page.get("asnname", ""),
                "scan_date": task.get("time", ""),
                "report": f"https://urlscan.io/result/{scan_id}/",
                "screenshot": f"https://urlscan.io/screenshots/{scan_id}.png",
            }
            entries.append(entry)
            print(f"  {C['Cy']}>{C['X']} {entry['url']}  {C['D']}[{entry['ip']} / {entry['country']}]{C['X']}")
        _record("urlscan", f"URLScan.io: {domain}", {"domain": domain, "scans": entries}, "info")
        return entries
    elif isinstance(data, dict) and "_error" in data:
        warn(f"URLScan.io error: {data['_error']}")
    else:
        warn(f"No URLScan.io results for {domain}")
    return []


# ---------------------------------------------------------------------------
# Email harvest from certs
# ---------------------------------------------------------------------------

def email_harvest_from_certs(domain, timeout=15):
    info(f"Extracting potential emails from certificate SANs for {domain} ...")
    certs = crt_sh_certs(domain, timeout=timeout)
    emails = set()
    for c in certs:
        name = c.get("name", "")
        if "@" in name:
            emails.add(name)
    if emails:
        ok(f"Found {len(emails)} email-like SAN entries")
        for e in emails:
            print(f"  {C['Cy']}{e}{C['X']}")
        _record("emails", f"Emails from certs: {domain}", {"domain": domain, "emails": list(emails)}, "info")
    return list(emails)


# ---------------------------------------------------------------------------
# Username enumeration (Sherlock-style, 50+ platforms)
# ---------------------------------------------------------------------------

_USERNAME_PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "LinkedIn": "https://www.linkedin.com/in/{}/",
    "Facebook": "https://www.facebook.com/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Tumblr": "https://{}.tumblr.com",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "Hashnode": "https://hashnode.com/@{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Keybase": "https://keybase.io/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://www.behance.net/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Mixcloud": "https://www.mixcloud.com/{}/",
    "About.me": "https://about.me/{}",
    "Gravatar": "https://en.gravatar.com/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "npm": "https://www.npmjs.com/~{}",
    "PyPI": "https://pypi.org/user/{}",
    "RubyGems": "https://rubygems.org/profiles/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/{}",
    "CodePen": "https://codepen.io/{}",
    "Replit": "https://replit.com/@{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Disqus": "https://disqus.com/by/{}/",
    "AngelList": "https://angel.co/u/{}",
    "Crunchbase": "https://www.crunchbase.com/person/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Ebay": "https://www.ebay.com/usr/{}",
    "Etsy": "https://www.etsy.com/shop/{}",
    "Trello": "https://trello.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Mastodon": "https://mastodon.social/@{}",
    "Gitea": "https://gitea.com/{}",
}


def username_enum(username, timeout=8, threads=15):
    """Sherlock-style username lookup across 50+ platforms via HEAD requests."""
    info(f"Username enumeration for '{username}' across {len(_USERNAME_PLATFORMS)} platforms ...")
    found = []

    def check_platform(name, url_tpl):
        url = url_tpl.format(urllib.parse.quote(username))
        try:
            req = urllib.request.Request(url, method="HEAD", headers={
                "User-Agent": "Mozilla/5.0 (compatible; ghost-osint/2.0)",
                "Accept": "*/*",
            })
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                if r.status < 400:
                    return name, url, True
        except urllib.error.HTTPError as e:
            if e.code < 400:
                return name, url, True
            return name, url, False
        except Exception:
            return name, url, None
        return name, url, False

    not_found = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check_platform, nm, tpl): nm for nm, tpl in _USERNAME_PLATFORMS.items()}
        for fut in as_completed(futures):
            nm, url, status = fut.result()
            if status is True:
                ok(f"[{nm}] {url}")
                found.append({"platform": nm, "url": url})
            elif status is False:
                not_found.append(nm)

    warn(f"Username '{username}': found on {len(found)}/{len(_USERNAME_PLATFORMS)} platforms")
    if found:
        _record("username", f"Username: {username}",
                {"username": username, "found": found, "not_found": not_found}, "info")
    return found


# ---------------------------------------------------------------------------
# Leaky cloud bucket enumeration
# ---------------------------------------------------------------------------

def leaky_buckets(domain, timeout=8):
    """Enumerate potential leaky S3/GCS/Azure buckets based on domain name variants."""
    info(f"Leaky bucket enumeration for {domain} ...")
    base = domain.split(".")[0].lower().replace("-", "").replace("_", "")
    base_dash = domain.split(".")[0].lower()
    variants = set()
    for name in [base, base_dash, domain.replace(".", "-"), domain.split(".")[0]]:
        for suffix in ["", "-dev", "-prod", "-staging", "-backup", "-data", "-logs",
                       "-assets", "-media", "-files", "-uploads", "-static", "-public",
                       "-private", "-internal", "-config", "-secrets", "-db", "-images",
                       ".dev", ".prod", "-s3", "-bucket", "-store", "-cdn", "-archive"]:
            v = f"{name}{suffix}"
            if re.match(r'^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$', v):
                variants.add(v)

    results = []

    def check_s3(bucket):
        url = f"https://{bucket}.s3.amazonaws.com/"
        data = _get(url, timeout=timeout, verify=False)
        if isinstance(data, str):
            if "<ListBucketResult" in data:
                return bucket, "S3", "open", url
            if "AccessDenied" in data or "AllAccessDisabled" in data:
                return bucket, "S3", "exists_private", url
        return None

    def check_gcs(bucket):
        url = f"https://storage.googleapis.com/{bucket}/"
        data = _get(url, timeout=timeout, verify=False)
        if isinstance(data, str) and ("<ListBucketResult" in data or "xmlns.googleapis.com" in data):
            return bucket, "GCS", "open", url
        if isinstance(data, dict) and data.get("_http_error") == 403:
            return bucket, "GCS", "exists_private", url
        return None

    def check_azure(bucket):
        url = f"https://{bucket}.blob.core.windows.net/"
        data = _get(url, timeout=timeout, verify=False)
        if isinstance(data, str) and ("<?xml" in data or "EnumerationResults" in data):
            return bucket, "Azure", "open", url
        if isinstance(data, dict) and data.get("_http_error") == 403:
            return bucket, "Azure", "exists_private", url
        return None

    variant_list = list(variants)
    with ThreadPoolExecutor(max_workers=20) as ex:
        all_futures = []
        for v in variant_list:
            all_futures.append(ex.submit(check_s3, v))
            all_futures.append(ex.submit(check_gcs, v))
            all_futures.append(ex.submit(check_azure, v))
        for fut in as_completed(all_futures):
            res = fut.result()
            if res:
                bucket, provider, status, url = res
                if status == "open":
                    warn(f"OPEN BUCKET: [{provider}] {url}")
                elif status == "exists_private":
                    info(f"Exists (private): [{provider}] {url}")
                results.append({"bucket": bucket, "provider": provider, "status": status, "url": url})

    open_buckets = [r for r in results if r["status"] == "open"]
    if open_buckets:
        _record("buckets", f"Open cloud buckets: {domain}",
                {"domain": domain, "open": open_buckets, "all": results}, "high")
    elif results:
        _record("buckets", f"Cloud buckets: {domain}",
                {"domain": domain, "open": [], "all": results}, "info")
    else:
        ok(f"No accessible cloud buckets found for {domain}")
    return results


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _print_summary():
    print()
    print(f"{C['G']}{'=' * 60}{C['X']}")
    print(f"{C['N']}{C['G']} GHOST-OSINT - Summary{C['X']}")
    print(f"{C['G']}{'=' * 60}{C['X']}")

    cats = {}
    for f in _findings:
        cats.setdefault(f["category"], []).append(f)

    total = len(_findings)
    sev_counts = {}
    for f in _findings:
        sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1

    colors = {"high": C["R"], "medium": C["Y"], "info": C["Cy"], "low": C["G"]}
    print(f"\n Total findings: {C['N']}{total}{C['X']}")
    for sev in ("high", "medium", "low", "info"):
        count = sev_counts.get(sev, 0)
        if count:
            col = colors.get(sev, C["W"])
            print(f"  {col}[{sev.upper()}]{C['X']} {count}")

    if _findings:
        print(f"\n{C['D']} Categories:{C['X']}")
        for cat, items in cats.items():
            print(f"  {C['G']}>{C['X']} {cat}: {len(items)} item(s)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="ghost-osint",
        description="Extended OSINT Framework | By Gh0st-Bx1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--target", "-t", help="Target domain (e.g. example.com)")
    parser.add_argument("--email", "-e", help="Email address for breach check")
    parser.add_argument("--hibp-key", help="HaveIBeenPwned API key")
    parser.add_argument("--ip", help="IP address for ASN/Shodan lookup")
    parser.add_argument("--domain", "-d", help="Alias for --target")
    parser.add_argument("--breach", action="store_true", help="Check email in breach databases")
    parser.add_argument("--whois", action="store_true", help="WHOIS + DNS lookup")
    parser.add_argument("--certs", action="store_true", help="Certificate transparency (crt.sh)")
    parser.add_argument("--github", action="store_true", help="GitHub dork URL generation")
    parser.add_argument("--paste", action="store_true", help="Pastebin/public paste search")
    parser.add_argument("--employees", action="store_true", help="Employee enumeration hints")
    parser.add_argument("--subdomains", action="store_true", help="Subdomain brute-force")
    parser.add_argument("--asn", action="store_true", help="ASN lookup for IP")
    parser.add_argument("--shodan", "--internetdb", action="store_true",
                        help="Shodan InternetDB enrichment for discovered IPs (no key)")
    parser.add_argument("--wayback", action="store_true",
                        help="Wayback Machine URL harvest via CDX API")
    parser.add_argument("--takeover", action="store_true",
                        help="Subdomain takeover detection (auto-runs after --subdomains)")
    parser.add_argument("--urlscan", action="store_true",
                        help="URLScan.io passive lookup (no key)")
    parser.add_argument("--username", "-u", metavar="HANDLE",
                        help="Sherlock-style username enumeration across 50+ platforms")
    parser.add_argument("--buckets", action="store_true",
                        help="Leaky S3/GCS/Azure bucket enumeration from domain variants")
    parser.add_argument("--all", "-a", action="store_true", help="Run all modules")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds (default: 10)")
    parser.add_argument("--proxy", help="Proxy HTTP/HTTPS (ex: http://127.0.0.1:8080)")
    parser.add_argument("--no-banner", action="store_true", help="Suprimir banner")
    args = parser.parse_args()

    domain = args.target or args.domain
    run_all = args.all

    if not domain and not args.email and not args.ip and not args.username:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    if not getattr(args, "no_banner", False):
        print(BANNER)
    print()

    if getattr(args, "proxy", None):
        os.environ["http_proxy"] = args.proxy
        os.environ["https_proxy"] = args.proxy

    start = time.time()

    if domain and (run_all or args.certs):
        crt_sh_certs(domain, timeout=args.timeout)

    if domain and (run_all or args.whois):
        dns_data = dns_enum(domain, timeout=args.timeout)
        whois_lookup(domain, timeout=args.timeout)
        if (run_all or args.shodan) and dns_data:
            for rtype in ("A",):
                for ip in dns_data.get(rtype, []):
                    shodan_internetdb(ip, timeout=args.timeout)

    if domain and (run_all or args.wayback):
        wayback_harvest(domain, timeout=args.timeout + 10)

    if domain and (run_all or args.urlscan):
        urlscan_lookup(domain, timeout=args.timeout)

    if domain and (run_all or args.github):
        github_dorks(domain, timeout=args.timeout)

    if domain and (run_all or args.paste):
        pastebin_search(domain, timeout=args.timeout)

    if domain and (run_all or args.employees):
        enumerate_employees(domain, timeout=args.timeout)

    if domain and (run_all or args.subdomains):
        subs = subdomain_bruteforce(domain, timeout=args.timeout)
        if (run_all or args.takeover) and subs:
            check_subdomain_takeover(subs, timeout=args.timeout)
        if (run_all or args.shodan) and subs:
            seen_ips = set()
            for s in subs:
                ip = s.get("ip", "")
                if ip and ip not in seen_ips:
                    seen_ips.add(ip)
                    shodan_internetdb(ip, timeout=args.timeout)

    if domain and (run_all or args.buckets):
        leaky_buckets(domain, timeout=args.timeout)

    if args.email and (run_all or args.breach):
        check_breach(args.email, api_key=args.hibp_key, timeout=args.timeout)

    if args.ip and (run_all or args.asn):
        asn_lookup(args.ip, timeout=args.timeout)

    if args.ip and (run_all or args.shodan):
        shodan_internetdb(args.ip, timeout=args.timeout)

    if args.username:
        username_enum(args.username, timeout=args.timeout)

    elapsed = time.time() - start
    info(f"Completed in {elapsed:.1f}s")
    _print_summary()

    if args.output:
        out = {
            "tool": "ghost-osint",
            "version": VERSAO,
            "target": domain,
            "email": args.email,
            "ip": args.ip,
            "username": args.username,
            "findings": _findings,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        ok(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
