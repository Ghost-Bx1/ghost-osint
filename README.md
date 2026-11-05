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
