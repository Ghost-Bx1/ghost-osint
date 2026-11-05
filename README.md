# Ghost-OSINT

> Extended OSINT framework - domain, email and IP intelligence from public sources.

```
  GHOST-OSINT  v1.0.0  |  Extended OSINT Framework
  By Gh0st-Bx1         |  github.com/Ghost-Bx1
```

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=flat-square)
![Category](https://img.shields.io/badge/Category-OSINT-purple?style=flat-square)

---

## Overview

Ghost-OSINT aggregates passive and semi-passive intelligence from public sources: certificate transparency logs, breach databases, WHOIS/DNS/ASN data, GitHub dork generation, public paste sites, and employee pattern enumeration.

| Module        | Source          | Description                                            |
|---------------|-----------------|--------------------------------------------------------|
| `--certs`     | crt.sh          | Certificate transparency - subdomain discovery         |
| `--whois`     | WHOIS servers   | Registrar, creation date, registrant, nameservers      |
| `--breach`    | HaveIBeenPwned  | Email breach check (requires paid API key)             |
| `--github`    | GitHub Search   | Dork URL generation for manual review                  |
| `--paste`     | psbdmp.ws       | Public paste site search                               |
| `--employees` | LinkedIn/Hunter | Email pattern enumeration and manual check URLs        |
| `--subdomains`| DNS brute-force | 60+ common subdomains, multithreaded                   |
| `--asn`       | Cymru WHOIS     | ASN, prefix, organization, country                     |
| `--all`       | All sources     | Run all modules                                        |

---

## Requirements

```
Python 3.6+
No external dependencies (stdlib only)
HaveIBeenPwned API key required for --breach (paid tier)
```

---

## Installation

```bash
git clone https://github.com/Ghost-Bx1/ghost-osint
cd ghost-osint
python ghost-osint.py --help
```

---

## Usage

```bash
# Full OSINT sweep on a domain
python ghost-osint.py --target example.com --all

# Selected modules
python ghost-osint.py --target example.com --certs --whois --subdomains

# Email breach check
python ghost-osint.py --email user@example.com --breach --hibp-key YOUR_KEY

# GitHub dork generation + paste search
python ghost-osint.py --target example.com --github --paste

# ASN lookup from IP
python ghost-osint.py --ip 1.2.3.4 --asn

# Full sweep with JSON output
python ghost-osint.py --target example.com --all -o osint.json
```

---

## Reference

| Flag              | Description                                           |
|-------------------|-------------------------------------------------------|
| `--target / -t`   | Target domain                                         |
| `--email / -e`    | Email address for breach check                        |
| `--ip`            | IP address for ASN lookup                             |
| `--hibp-key`      | HaveIBeenPwned API v3 key                             |
| `--breach`        | Check email against breach databases                  |
| `--whois`         | WHOIS and DNS record lookup                           |
| `--certs`         | Certificate transparency via crt.sh                   |
| `--github`        | GitHub dork URL generation                            |
| `--paste`         | Public paste site search                              |
| `--employees`     | Employee enumeration hints and email patterns         |
| `--subdomains`    | Subdomain brute-force with built-in wordlist          |
| `--asn`           | ASN lookup via Cymru                                  |
| `--all / -a`      | Run all modules                                       |
| `--output / -o`   | Save results as JSON                                  |
| `--timeout`       | HTTP timeout in seconds (default: 10)                 |

---

## Roadmap

Improvements planned based on analysis of theHarvester, Recon-ng, SpiderFoot and amass:

| Priority | Feature | Description |
|----------|---------|-------------|
| High | Shodan InternetDB | For discovered IPs: open ports, CVEs, tags (malware/honeypot) - no API key required |
| High | Wayback Machine URL harvest | Extract historical endpoints from CDX API - reveals old paths and forgotten endpoints |
| High | Subdomain takeover detection | For each subdomain, check CNAME chain for unclaimed services (GitHub Pages, Heroku, S3, Shopify) |
| High | URLScan.io passive lookup | Screenshots, DOM, HTTP headers, TLS info, page links for target domain - no key needed for search |
| High | Username enumeration (Sherlock-style) | Check a handle across 50 platforms via HEAD requests using stdlib urllib (`--username HANDLE`) |
| High | Leaky bucket enumeration | Generate name permutations + common suffixes and probe S3/GCS/Azure HEAD requests |
| Medium | OTX AlienVault threat feed | Domain/IP threat correlation: associated IPs, malware hashes, C2 correlation - no key needed |
| Medium | HudsonRock infostealer check | Check if domain emails appear in infostealer credential logs (cavalier API) |
| Medium | CommonCrawl index lookup | Retrieve all indexed URLs/paths for target domain via CDX API |
| Medium | Reverse DNS on discovered IPs | PTR lookup on every found IP to discover sibling domains (stdlib socket) |
| Medium | Structured dork list (20+) | Generate `site:`, `inurl:`, `filetype:`, `intitle:`, `"@domain.com" -site:` combos ready to paste |
| Medium | DNS historical records | Past A/MX/NS records via HackerTarget free API to find old IPs still responding |
| Low | VirusTotal passive DNS | Subdomains, resolutions, reputation score (requires API key) |
| Low | Hunter.io email finder | Professional emails with confidence score (requires API key) |
| Low | Change tracking / diff mode | Compare two JSON outputs: classify findings as new/removed/unchanged (`--diff old.json`) |

## Notes

- `--breach` requires a paid HaveIBeenPwned API key from hibp.haveibeenpwned.com
- `--github` generates dork URLs only - actual search requires authenticated browser session
- `--employees` generates manual check URLs; no scraping is performed

---

## Ghost Toolkit

| Tool | Description |
|------|-------------|
| [ghost-ad](https://github.com/Ghost-Bx1/ghost-ad) | Active Directory - LDAP, Kerberoasting, AS-REP Roasting, BloodHound-lite |
| [ghost-cloud](https://github.com/Ghost-Bx1/ghost-cloud) | Cloud Security - AWS, Azure and GCP misconfiguration scanner |
| [ghost-fuzz](https://github.com/Ghost-Bx1/ghost-fuzz) | Web Fuzzing - directory brute-force, parameter fuzzing, vhost enumeration |
| [ghost-osint](https://github.com/Ghost-Bx1/ghost-osint) | OSINT - domain, email and IP intelligence from public sources |
| [ghost-privesc](https://github.com/Ghost-Bx1/ghost-privesc) | Privilege Escalation - Linux privesc checker, 17 vectors, GTFOBins |
| [ghost-recon](https://github.com/Ghost-Bx1/ghost-recon) | Reconnaissance - DNS, SSL, WAF, subdomain enumeration, email security |
| [ghost-report](https://github.com/Ghost-Bx1/ghost-report) | Reporting - pentest report generator from any ghost-* JSON output |
| [ghost-scan](https://github.com/Ghost-Bx1/ghost-scan) | Port Scanner - async TCP/UDP scanner with banner grabbing and CVE correlation |
| [ghost-shell](https://github.com/Ghost-Bx1/ghost-shell) | Payload Generation - reverse shell and web shell generator, 25+ languages |
| [ghost-spray](https://github.com/Ghost-Bx1/ghost-spray) | Credential Attacks - password spraying, stuffing, default credential testing |
| [ghost-wifi](https://github.com/Ghost-Bx1/ghost-wifi) | WiFi Attacks - monitor mode, deauth, WPA/WPA2 capture, PMKID, WPS, Evil Twin |

---

## Disclaimer

For use in authorized environments only. Penetration testing, CTF competitions, and offensive security research with explicit permission from the environment owner. The author is not responsible for misuse.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
