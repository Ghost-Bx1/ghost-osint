#!/usr/bin/env python3
# ghost-osint.py - Extended OSINT Framework
# By Gh0st-Bx1 | github.com/Ghost-Bx1

import argparse
import csv
import hashlib
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

VERSAO = "3.0.0"


def _build_banner():
    import re as _re
    G = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    W = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "=" * IW; sp = " " * IW
    TL = "+"; TR = "+"; BL = "+"; BR = "+"; VB = "|"
    hl = "-" * 44; bar = "|"
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

    info_block = [
        f"{G}{N}GHOST-OSINT{X}",
        f"{Cy}v{VERSAO}  {D}Extended OSINT Framework{X}",
        f"{D}{hl}{X}",
        f"{W}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}--target --whois --certs --subdomains --wayback --urlscan{X}",
        f"{D}--email --breach --email-intel --username --permute{X}",
        f"{D}--ip --geo --reverse-ip --asn --shodan{X}",
        f"{D}--dns-deep --tech --dorks --buckets --all{X}",
        f"{D}--output FILE.json  --csv  --proxy  --timeout N{X}",
    ]

    out = [f"{G}+{eq}+{X}", f"{G}|{sp}|{X}"]
    for left, center, right in ga:
        combined = left + center + right
        out.append(_row(combined))
    out.append(f"{G}|{sp}|{X}")
    for i in info_block:
        out.append(_row_l(i))
    out += [f"{G}|{sp}|{X}", f"{G}+{eq}+{X}"]
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
        "User-Agent": "Mozilla/5.0 (compatible; ghost-osint/3.0)",
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
# IP Geolocation (ip-api.com - free, no key, 45 req/min)
# ---------------------------------------------------------------------------

def ip_geolocate(ip, timeout=8):
    info(f"Geolocating {ip} ...")
    fields = "status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,reverse"
    data = _get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=timeout)
    if isinstance(data, dict) and data.get("status") == "success":
        result = {k: v for k, v in data.items() if k != "status"}
        ok(f"Geo {ip}: {data.get('city')}, {data.get('regionName')}, {data.get('country')} ({data.get('countryCode')})")
        ok(f"  ISP: {data.get('isp')} | ASN: {data.get('as')} | TZ: {data.get('timezone')}")
        if data.get("lat") and data.get("lon"):
            info(f"  Coords: {data.get('lat')},{data.get('lon')}")
        _record("geo", f"Geolocation: {ip}", result, "info")
        return result
    warn(f"Geolocation failed for {ip}: {data.get('message', 'unknown')}")
    return {}


# ---------------------------------------------------------------------------
# Reverse IP lookup (HackerTarget - free, 20 req/day)
# ---------------------------------------------------------------------------

def reverse_ip_lookup(ip, timeout=12):
    info(f"Reverse IP lookup for {ip} ...")
    data = _get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=timeout)
    if isinstance(data, str) and "error" not in data.lower() and data.strip():
        domains = [d.strip() for d in data.strip().splitlines() if d.strip()]
        ok(f"Reverse IP {ip}: {len(domains)} domain(s)")
        for d in domains[:20]:
            print(f"  {C['Cy']}>{C['X']} {d}")
        if len(domains) > 20:
            print(f"  {C['D']}... and {len(domains) - 20} more{C['X']}")
        _record("reverse_ip", f"Reverse IP: {ip}", {"ip": ip, "domains": domains}, "info")
        return domains
    warn(f"Reverse IP: no results for {ip}")
    return []


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
# Deep DNS scan via Google DNS-over-HTTPS
# ---------------------------------------------------------------------------

def dns_deep_scan(domain, timeout=10):
    info(f"Deep DNS scan for {domain} ...")
    results = {}

    def doh_query(name, rtype):
        url = f"https://dns.google/resolve?name={urllib.parse.quote(name)}&type={rtype}"
        data = _get(url, timeout=timeout)
        if isinstance(data, dict) and "Answer" in data:
            return [a.get("data", "") for a in data["Answer"]]
        return []

    mx = doh_query(domain, "MX")
    if mx:
        results["MX"] = mx
        ok(f"MX: {', '.join(mx[:5])}")

    ns = doh_query(domain, "NS")
    if ns:
        results["NS"] = ns
        ok(f"NS: {', '.join(ns[:5])}")

    a_recs = doh_query(domain, "A")
    if a_recs:
        results["A"] = a_recs
        ok(f"A: {', '.join(a_recs[:5])}")

    aaaa = doh_query(domain, "AAAA")
    if aaaa:
        results["AAAA"] = aaaa

    txt = doh_query(domain, "TXT")
    if txt:
        results["TXT"] = txt
        spf = [t for t in txt if "v=spf" in t.lower()]
        if spf:
            ok(f"SPF: {spf[0][:100]}")
            results["SPF"] = spf
        else:
            warn(f"No SPF record for {domain}")

    dmarc = doh_query(f"_dmarc.{domain}", "TXT")
    if dmarc:
        results["DMARC"] = dmarc
        ok(f"DMARC: {dmarc[0][:100]}")
    else:
        warn(f"No DMARC for {domain} - email spoofing may be possible")

    caa = doh_query(domain, "CAA")
    if caa:
        results["CAA"] = caa
        ok(f"CAA: {', '.join(caa[:3])}")
    else:
        warn(f"No CAA record for {domain} - certificate issuance unrestricted")

    dkim_selectors = ["default", "google", "mail", "dkim", "k1", "selector1", "selector2", "s1", "s2"]
    dkim_found = {}
    for sel in dkim_selectors:
        dkim = doh_query(f"{sel}._domainkey.{domain}", "TXT")
        if dkim:
            dkim_found[sel] = dkim
            ok(f"DKIM [{sel}]: found")
    if dkim_found:
        results["DKIM"] = dkim_found

    cname = doh_query(domain, "CNAME")
    if cname:
        results["CNAME"] = cname
        ok(f"CNAME: {', '.join(cname)}")

    _record("dns_deep", f"Deep DNS: {domain}", {"domain": domain, "records": results}, "info")
    return results


# ---------------------------------------------------------------------------
# Technology detection via HTTP headers + body fingerprinting
# ---------------------------------------------------------------------------

def tech_detect(domain, timeout=10):
    info(f"Technology detection for {domain} ...")
    detected = []
    headers_captured = {}

    for scheme in ("https", "http"):
        url = f"{scheme}://{domain}/"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,*/*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                headers_captured = {k.lower(): v for k, v in r.headers.items()}
                body = r.read(32768).decode("utf-8", errors="replace")
            break
        except Exception:
            if scheme == "http":
                warn(f"Tech detect: could not connect to {domain}")
                return detected
            continue

    server = headers_captured.get("server", "")
    if server:
        ok(f"Server: {server}")
        detected.append({"type": "server", "value": server})

    powered = headers_captured.get("x-powered-by", "")
    if powered:
        ok(f"X-Powered-By: {powered}")
        detected.append({"type": "powered_by", "value": powered})

    # Security headers audit
    sec_headers = {
        "strict-transport-security": "HSTS",
        "content-security-policy": "CSP",
        "x-frame-options": "X-Frame-Options",
        "x-content-type-options": "X-Content-Type-Options",
        "referrer-policy": "Referrer-Policy",
        "permissions-policy": "Permissions-Policy",
    }
    present_sec = []
    missing_sec = []
    for hdr, label in sec_headers.items():
        if headers_captured.get(hdr):
            present_sec.append(label)
        else:
            missing_sec.append(label)

    if present_sec:
        ok(f"Security headers present: {', '.join(present_sec)}")
    if missing_sec:
        warn(f"Missing security headers: {', '.join(missing_sec)}")
        detected.append({"type": "missing_security_headers", "value": missing_sec})

    # CMS / framework fingerprinting
    tech_patterns = {
        "WordPress":  ["wp-content/", "wp-includes/", "/wp-json/", "wp-embed"],
        "Drupal":     ["drupal.js", "sites/default/files", "Drupal.settings", "drupal.min.js"],
        "Joomla":     ["joomla!", "/components/com_", "Joomla"],
        "Laravel":    ["laravel_session", "_token", "csrf-token", "XSRF-TOKEN"],
        "Django":     ["csrfmiddlewaretoken", "django"],
        "Flask":      ["werkzeug", "flask"],
        "React":      ["react.production.min.js", "__REACT_", "data-reactroot", "react-dom"],
        "Vue.js":     ["vue.min.js", "__vue__", "v-app", "vue.runtime"],
        "Angular":    ["ng-version", "angular.min.js", "ng-app", "angular.js"],
        "Next.js":    ["__next", "_next/static", "__NEXT_DATA__"],
        "Nuxt.js":    ["__nuxt", "_nuxt/", "nuxt.js"],
        "jQuery":     ["jquery.min.js", "jquery-", "jQuery("],
        "Bootstrap":  ["bootstrap.min.css", "bootstrap.min.js", "bootstrap.bundle"],
        "Cloudflare": ["__cflb", "__cfuid", "cf-ray", "__cf_bm"],
        "PHP":        ["PHPSESSID", "X-Powered-By: PHP"],
        "ASP.NET":    ["ASP.NET_SessionId", "__VIEWSTATE", "aspnet", "__RequestVerificationToken"],
        "Webpack":    ["webpack", "__webpack_require__", "webpackChunk"],
        "GraphQL":    ["/graphql", "\"__typename\"", "graphiql"],
        "Shopify":    ["cdn.shopify.com", "shopify.com/s/files", "Shopify.theme"],
        "WooCommerce": ["woocommerce", "wc-ajax="],
    }

    for tech, patterns in tech_patterns.items():
        if any(p in body for p in patterns):
            ok(f"  Detected: {tech}")
            detected.append({"type": "technology", "value": tech})

    # CDN / proxy detection
    cdn_map = {
        "cf-ray": "Cloudflare",
        "x-amz-cf-id": "AWS CloudFront",
        "x-akamai-transformed": "Akamai",
        "x-fastly-request-id": "Fastly",
        "x-varnish": "Varnish",
        "x-cache": "Cache/CDN",
        "via": "Proxy/CDN",
    }
    for hdr, cdn in cdn_map.items():
        if headers_captured.get(hdr):
            ok(f"  CDN/Cache: {cdn}")
            detected.append({"type": "cdn", "value": cdn})

    result = {"domain": domain, "technologies": detected, "headers": headers_captured}
    _record("tech", f"Tech fingerprint: {domain}", result, "info")
    return detected


# ---------------------------------------------------------------------------
# Email intelligence (Gravatar, MX provider, disposable check)
# ---------------------------------------------------------------------------

def email_intelligence(email, timeout=10):
    info(f"Email intelligence for {email} ...")
    result = {"email": email}

    if "@" not in email:
        err(f"Invalid email: {email}")
        return {}

    local, domain = email.rsplit("@", 1)
    result["local"] = local
    result["domain"] = domain

    name_parts = re.split(r"[._\-+]", local)
    name_parts = [p for p in name_parts if len(p) > 1 and p.isalpha()]
    if name_parts:
        ok(f"Name parts extracted: {', '.join(name_parts)}")
        result["name_parts"] = name_parts

    email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    try:
        req = urllib.request.Request(gravatar_url, method="HEAD", headers={
            "User-Agent": "ghost-osint/3.0"
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            if r.status == 200:
                profile_data = _get(f"https://www.gravatar.com/{email_hash}.json", timeout=timeout)
                if isinstance(profile_data, dict) and "entry" in profile_data:
                    entry = profile_data["entry"][0] if profile_data["entry"] else {}
                    result["gravatar"] = {
                        "exists": True,
                        "avatar": f"https://www.gravatar.com/avatar/{email_hash}",
                        "display_name": entry.get("displayName", ""),
                        "username": entry.get("preferredUsername", ""),
                        "profile_url": entry.get("profileUrl", ""),
                    }
                    ok(f"Gravatar found: display_name={result['gravatar']['display_name']}")
                else:
                    result["gravatar"] = {"exists": True, "avatar": f"https://www.gravatar.com/avatar/{email_hash}"}
                    ok("Gravatar avatar exists")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            result["gravatar"] = {"exists": False}
            info("No Gravatar for this email")
    except Exception as e:
        result["gravatar"] = {"exists": "unknown", "error": str(e)}

    # MX provider detection
    doh_url = f"https://dns.google/resolve?name={urllib.parse.quote(domain)}&type=MX"
    mx_data = _get(doh_url, timeout=timeout)
    if isinstance(mx_data, dict) and "Answer" in mx_data:
        mx_records = [a.get("data", "") for a in mx_data["Answer"]]
        result["mx_records"] = mx_records
        mx_str = " ".join(mx_records).lower()
        providers = {
            "Google Workspace": ["google.com", "googlemail.com", "aspmx.l.google"],
            "Microsoft 365": ["outlook.com", "protection.outlook.com"],
            "Proofpoint": ["pphosted.com"],
            "Mimecast": ["mimecast.com"],
            "Barracuda": ["barracudanetworks.com"],
            "Zoho": ["zoho.com"],
            "FastMail": ["fastmail.com"],
            "Yahoo": ["yahoodns.net"],
            "Amazon SES": ["amazonaws.com"],
            "Cloudflare Email": ["cloudflare.net"],
        }
        for provider, patterns in providers.items():
            if any(p in mx_str for p in patterns):
                ok(f"Email provider: {provider}")
                result["email_provider"] = provider
                break

    # Disposable email domains
    disposable = {
        "mailinator.com", "tempmail.com", "guerrillamail.com", "10minutemail.com",
        "throwaway.email", "yopmail.com", "fakeinbox.com", "trashmail.com",
        "maildrop.cc", "dispostable.com", "getairmail.com", "mailnull.com",
        "sharklasers.com", "guerrillamailblock.com", "spamgourmet.com",
    }
    if domain.lower() in disposable:
        warn(f"Disposable email domain: {domain}")
        result["disposable"] = True
    else:
        result["disposable"] = False

    _record("email_intel", f"Email intelligence: {email}", result, "info")
    return result


# ---------------------------------------------------------------------------
# OSINT dork generator
# ---------------------------------------------------------------------------

def osint_dorks(query, timeout=5):
    info(f"Generating OSINT dork URLs for '{query}' ...")
    q = urllib.parse.quote(query)
    dorks = {
        "Google": [
            f"https://www.google.com/search?q=site:{q}",
            f"https://www.google.com/search?q=inurl:{q}+filetype:pdf",
            f"https://www.google.com/search?q=intext:{q}+password",
            f"https://www.google.com/search?q={q}+site:pastebin.com",
            f"https://www.google.com/search?q={q}+site:github.com+password+OR+token+OR+secret",
            f"https://www.google.com/search?q={q}+filetype:env+OR+filetype:sql+OR+filetype:log",
            f"https://www.google.com/search?q=intitle:index.of+{q}",
            f"https://www.google.com/search?q={q}+site:linkedin.com",
        ],
        "GitHub": [
            f"https://github.com/search?q={q}+password&type=code",
            f"https://github.com/search?q={q}+api_key&type=code",
            f"https://github.com/search?q={q}+secret&type=code",
            f"https://github.com/search?q={q}+token&type=code",
            f"https://github.com/search?q={q}+DATABASE_URL&type=code",
            f"https://github.com/search?q={q}+BEGIN+RSA+PRIVATE&type=code",
            f"https://github.com/search?q={q}+filename:.env&type=code",
        ],
        "Shodan": [
            f"https://www.shodan.io/search?query=hostname:{q}",
            f"https://www.shodan.io/search?query=org:{q}",
            f"https://www.shodan.io/search?query=ssl:{q}",
            f"https://www.shodan.io/search?query=http.html:{q}",
        ],
        "Censys": [
            f"https://search.censys.io/certificates?q={q}",
            f"https://search.censys.io/hosts?q={q}",
        ],
        "crt.sh": [
            f"https://crt.sh/?q=%.{q}",
            f"https://crt.sh/?q={q}",
        ],
        "Wayback": [
            f"https://web.archive.org/web/*/{q}/*",
        ],
        "VirusTotal": [
            f"https://www.virustotal.com/gui/domain/{q}",
        ],
        "GreyNoise": [
            f"https://viz.greynoise.io/query/?gnql={q}",
        ],
    }
    for engine, urls in dorks.items():
        print(f"\n  {C['N']}{C['Cy']}[{engine}]{C['X']}")
        for u in urls:
            print(f"    {C['D']}{u}{C['X']}")
    _record("dorks", f"OSINT dorks: {query}", {"query": query, "dorks": dorks}, "info")
    return dorks


# ---------------------------------------------------------------------------
# Username permutation generator
# ---------------------------------------------------------------------------

def username_permute(text, timeout=5):
    info(f"Generating username permutations for '{text}' ...")
    extra_parts = []
    base = text
    if "@" in text:
        local, _ = text.rsplit("@", 1)
        base = local
    base_clean = re.sub(r"[^a-z0-9]", "", base.lower())
    extra_parts = [p for p in re.split(r"[._\-+@ ]", base.lower()) if len(p) > 1]

    permutations = set()
    permutations.add(base_clean)
    permutations.add(base.lower())

    for n in ["0", "1", "2", "7", "99", "123", "1337", "2024", "2025", "2026"]:
        permutations.add(f"{base_clean}{n}")
        permutations.add(f"{n}{base_clean}")

    leet = str.maketrans("aeiost", "431057")
    permutations.add(base_clean.translate(leet))
    permutations.add(base_clean.replace("o", "0").replace("a", "4"))

    if len(extra_parts) >= 2:
        a, b = extra_parts[0], extra_parts[1]
        permutations.update([
            f"{a}{b}", f"{b}{a}", f"{a}.{b}", f"{a}_{b}", f"{a}-{b}",
            f"{a[0]}{b}", f"{a}{b[0]}", f"{a[0]}.{b}", f"{a[0]}_{b}",
            f"{b}.{a}", f"{b}_{a}", f"{a[0:3]}{b}", f"{a}{b[0:3]}",
        ])

    for suffix in ["_", ".", "-"]:
        permutations.add(base_clean.replace(" ", suffix))

    permutations.discard("")
    permutations.discard(" ")
    result = sorted(permutations)
    ok(f"Generated {len(result)} username permutations:")
    for p in result[:30]:
        print(f"  {C['Cy']}{p}{C['X']}")
    if len(result) > 30:
        print(f"  {C['D']}... and {len(result) - 30} more{C['X']}")
    _record("permute", f"Username permutations: {text}", {"input": text, "permutations": result}, "info")
    return result


# ---------------------------------------------------------------------------
# Wayback Machine URL harvest
# ---------------------------------------------------------------------------

def wayback_harvest(domain, limit=300, timeout=20):
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
        "User-Agent": "ghost-osint/3.0",
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
    for rtype, family in [("A", socket.AF_INET), ("AAAA", socket.AF_INET6)]:
        try:
            addrs = socket.getaddrinfo(domain, None, family)
            ips = list({a[4][0] for a in addrs})
            if ips:
                results[rtype] = ips
                ok(f"{rtype}: {', '.join(ips)}")
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
        ("RocketReach", f"https://rocketreach.co/company?name={domain.split('.')[0]}"),
        ("Clearbit", f"https://clearbit.com/companies/{domain}"),
    ]
    results = []
    for source, url in patterns:
        warn(f"{source} - manual check required:")
        print(f"  {C['Cy']}{url}{C['X']}")
        results.append({"source": source, "url": url})
    common_email_formats = [
        f"firstname.lastname@{domain}", f"f.lastname@{domain}",
        f"firstname@{domain}", f"flastname@{domain}",
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
                    "User-Agent": "Mozilla/5.0 (compatible; ghost-osint/3.0)"
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
# Username enumeration - 100+ platforms
# ---------------------------------------------------------------------------

_USERNAME_PLATFORMS = {
    # Developer / code
    "GitHub":        "https://github.com/{}",
    "GitLab":        "https://gitlab.com/{}",
    "Bitbucket":     "https://bitbucket.org/{}",
    "Gitea":         "https://gitea.com/{}",
    "Sourceforge":   "https://sourceforge.net/u/{}/",
    "npm":           "https://www.npmjs.com/~{}",
    "PyPI":          "https://pypi.org/user/{}/",
    "RubyGems":      "https://rubygems.org/profiles/{}",
    "DockerHub":     "https://hub.docker.com/u/{}",
    "HuggingFace":   "https://huggingface.co/{}",
    "Replit":        "https://replit.com/@{}",
    "CodePen":       "https://codepen.io/{}",
    "Exercism":      "https://exercism.org/profiles/{}",
    # Social media
    "Twitter/X":     "https://twitter.com/{}",
    "Instagram":     "https://www.instagram.com/{}/",
    "Facebook":      "https://www.facebook.com/{}",
    "LinkedIn":      "https://www.linkedin.com/in/{}/",
    "Reddit":        "https://www.reddit.com/user/{}/",
    "TikTok":        "https://www.tiktok.com/@{}",
    "YouTube":       "https://www.youtube.com/@{}",
    "Pinterest":     "https://www.pinterest.com/{}/",
    "Tumblr":        "https://{}.tumblr.com",
    "Snapchat":      "https://www.snapchat.com/add/{}",
    "Threads":       "https://www.threads.net/@{}",
    "Bluesky":       "https://bsky.app/profile/{}",
    "Mastodon":      "https://mastodon.social/@{}",
    "Minds":         "https://www.minds.com/{}",
    "Myspace":       "https://myspace.com/{}",
    # Microblogging / content
    "Medium":        "https://medium.com/@{}",
    "Dev.to":        "https://dev.to/{}",
    "Hashnode":      "https://hashnode.com/@{}",
    "Substack":      "https://substack.com/@{}",
    "WordPress":     "https://{}.wordpress.com",
    "Blogger":       "https://{}.blogspot.com",
    "IndieHackers":  "https://www.indiehackers.com/{}",
    # Gaming
    "Steam":         "https://steamcommunity.com/id/{}",
    "Twitch":        "https://www.twitch.tv/{}",
    "Kick":          "https://kick.com/{}",
    "Roblox":        "https://www.roblox.com/user.aspx?username={}",
    "Chess.com":     "https://www.chess.com/member/{}",
    "Lichess":       "https://lichess.org/@/{}",
    # Creative / art
    "Dribbble":      "https://dribbble.com/{}",
    "Behance":       "https://www.behance.net/{}",
    "DeviantArt":    "https://www.deviantart.com/{}",
    "ArtStation":    "https://www.artstation.com/{}",
    "Flickr":        "https://www.flickr.com/people/{}",
    "500px":         "https://500px.com/p/{}",
    "Pexels":        "https://www.pexels.com/@{}",
    "Unsplash":      "https://unsplash.com/@{}",
    # Music / audio
    "SoundCloud":    "https://soundcloud.com/{}",
    "Bandcamp":      "https://{}.bandcamp.com",
    "Last.fm":       "https://www.last.fm/user/{}",
    "Mixcloud":      "https://www.mixcloud.com/{}/",
    "Spotify":       "https://open.spotify.com/user/{}",
    # Video
    "Vimeo":         "https://vimeo.com/{}",
    "Rumble":        "https://rumble.com/c/{}",
    "Odysee":        "https://odysee.com/@{}",
    "DailyMotion":   "https://www.dailymotion.com/{}",
    # Productivity / tech
    "HackerNews":    "https://news.ycombinator.com/user?id={}",
    "ProductHunt":   "https://www.producthunt.com/@{}",
    "AngelList":     "https://angel.co/u/{}",
    "Crunchbase":    "https://www.crunchbase.com/person/{}",
    "Trello":        "https://trello.com/{}",
    "About.me":      "https://about.me/{}",
    "Gravatar":      "https://en.gravatar.com/{}",
    "Keybase":       "https://keybase.io/{}",
    # Challenge / learning
    "HackerRank":    "https://www.hackerrank.com/{}",
    "LeetCode":      "https://leetcode.com/{}",
    "Kaggle":        "https://www.kaggle.com/{}",
    "Duolingo":      "https://www.duolingo.com/profile/{}",
    "freeCodeCamp":  "https://www.freecodecamp.org/{}",
    # Community / Q&A
    "Quora":         "https://www.quora.com/profile/{}",
    "Imgur":         "https://imgur.com/user/{}",
    "Disqus":        "https://disqus.com/by/{}/",
    "Pastebin":      "https://pastebin.com/u/{}",
    # Marketplace / creator economy
    "Fiverr":        "https://www.fiverr.com/{}",
    "Patreon":       "https://www.patreon.com/{}",
    "Ko-fi":         "https://ko-fi.com/{}",
    "itch.io":       "https://{}.itch.io",
    "Ebay":          "https://www.ebay.com/usr/{}",
    "Etsy":          "https://www.etsy.com/shop/{}",
    "Wattpad":       "https://www.wattpad.com/user/{}",
    # Russian / international
    "VK":            "https://vk.com/{}",
    # Other
    "Telegram":      "https://t.me/{}",
}


def username_enum(username, timeout=8, threads=15):
    info(f"Username enumeration for '{username}' across {len(_USERNAME_PLATFORMS)} platforms ...")
    found = []

    def check_platform(name, url_tpl):
        url = url_tpl.format(urllib.parse.quote(username))
        try:
            req = urllib.request.Request(url, method="HEAD", headers={
                "User-Agent": "Mozilla/5.0 (compatible; ghost-osint/3.0)",
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
# CSV output
# ---------------------------------------------------------------------------

def _save_csv(output_path):
    csv_path = re.sub(r'\.json$', '.csv', output_path)
    if csv_path == output_path:
        csv_path = output_path + ".csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "title", "severity", "timestamp", "data"])
        for finding in _findings:
            writer.writerow([
                finding.get("category", ""),
                finding.get("title", ""),
                finding.get("severity", ""),
                finding.get("timestamp", ""),
                json.dumps(finding.get("data", {}), ensure_ascii=False),
            ])
    return csv_path


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _print_summary():
    print()
    print(f"{C['G']}{'=' * 60}{C['X']}")
    print(f"{C['N']}{C['G']} GHOST-OSINT v{VERSAO} - Summary{C['X']}")
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
        description="Extended OSINT Framework v3.0.0 | By Gh0st-Bx1 | github.com/Ghost-Bx1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--target", "-t", help="Target domain (e.g. example.com)")
    parser.add_argument("--email", "-e", help="Email address for breach/intelligence check")
    parser.add_argument("--hibp-key", help="HaveIBeenPwned API key")
    parser.add_argument("--ip", help="IP address for ASN/Shodan/geo/reverse-ip lookup")
    parser.add_argument("--domain", "-d", help="Alias for --target")
    # Domain modules
    parser.add_argument("--breach", action="store_true", help="Check email in breach databases (HIBP)")
    parser.add_argument("--whois", action="store_true", help="WHOIS + basic DNS lookup")
    parser.add_argument("--certs", action="store_true", help="Certificate transparency (crt.sh)")
    parser.add_argument("--github", action="store_true", help="GitHub dork URL generation")
    parser.add_argument("--paste", action="store_true", help="Pastebin/public paste search")
    parser.add_argument("--employees", action="store_true", help="Employee enumeration hints")
    parser.add_argument("--subdomains", action="store_true", help="Subdomain brute-force")
    parser.add_argument("--asn", action="store_true", help="ASN lookup for IP")
    parser.add_argument("--shodan", "--internetdb", action="store_true",
                        help="Shodan InternetDB enrichment (no key required)")
    parser.add_argument("--wayback", action="store_true",
                        help="Wayback Machine URL harvest via CDX API")
    parser.add_argument("--takeover", action="store_true",
                        help="Subdomain takeover detection")
    parser.add_argument("--urlscan", action="store_true",
                        help="URLScan.io passive lookup (no key)")
    parser.add_argument("--username", "-u", metavar="HANDLE",
                        help="Username enumeration across 100+ platforms")
    parser.add_argument("--buckets", action="store_true",
                        help="Leaky S3/GCS/Azure bucket enumeration")
    # New v3 modules
    parser.add_argument("--geo", action="store_true",
                        help="IP geolocation via ip-api.com (free, no key)")
    parser.add_argument("--reverse-ip", action="store_true",
                        help="Reverse IP lookup via HackerTarget (free)")
    parser.add_argument("--dns-deep", action="store_true",
                        help="Deep DNS scan: MX, NS, TXT, SPF, DMARC, DKIM, CAA via Google DoH")
    parser.add_argument("--tech", action="store_true",
                        help="Technology detection via HTTP headers + body fingerprinting")
    parser.add_argument("--dorks", action="store_true",
                        help="Generate OSINT dork URLs (Google, GitHub, Shodan, Censys, crt.sh)")
    parser.add_argument("--email-intel", action="store_true",
                        help="Email intelligence: Gravatar, MX provider, disposable check")
    parser.add_argument("--permute", metavar="TEXT",
                        help="Generate username permutations from name/email")
    # Output
    parser.add_argument("--all", "-a", action="store_true", help="Run all applicable modules")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--csv", action="store_true", help="Also save results as CSV file")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds (default: 10)")
    parser.add_argument("--proxy", help="Proxy HTTP/HTTPS (e.g. http://127.0.0.1:8080)")
    parser.add_argument("--no-banner", action="store_true", help="Suppress banner")
    args = parser.parse_args()

    domain = args.target or args.domain
    run_all = args.all

    if not domain and not args.email and not args.ip and not args.username and not args.permute:
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

    # --- Domain modules ---
    if domain and (run_all or args.certs):
        crt_sh_certs(domain, timeout=args.timeout)

    if domain and (run_all or args.whois):
        dns_data = dns_enum(domain, timeout=args.timeout)
        whois_lookup(domain, timeout=args.timeout)
        if (run_all or args.shodan) and dns_data:
            for ip in dns_data.get("A", []):
                shodan_internetdb(ip, timeout=args.timeout)

    if domain and (run_all or args.dns_deep):
        dns_deep_scan(domain, timeout=args.timeout)

    if domain and (run_all or args.tech):
        tech_detect(domain, timeout=args.timeout)

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

    if domain and (run_all or args.dorks):
        osint_dorks(domain, timeout=args.timeout)

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

    # --- Email modules ---
    if args.email and (run_all or args.breach):
        check_breach(args.email, api_key=args.hibp_key, timeout=args.timeout)

    if args.email and (run_all or args.email_intel):
        email_intelligence(args.email, timeout=args.timeout)

    # --- IP modules ---
    if args.ip and (run_all or args.asn):
        asn_lookup(args.ip, timeout=args.timeout)

    if args.ip and (run_all or args.shodan):
        shodan_internetdb(args.ip, timeout=args.timeout)

    if args.ip and (run_all or args.geo):
        ip_geolocate(args.ip, timeout=args.timeout)

    if args.ip and (run_all or args.reverse_ip):
        reverse_ip_lookup(args.ip, timeout=args.timeout)

    # --- Username modules ---
    if args.username:
        username_enum(args.username, timeout=args.timeout)

    if args.permute:
        username_permute(args.permute)

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

        if args.csv:
            csv_path = _save_csv(args.output)
            ok(f"CSV saved to {csv_path}")
    elif args.csv:
        warn("--csv requires --output to specify the base filename")


if __name__ == "__main__":
    main()
