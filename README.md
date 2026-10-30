# ghost-osint

**Extended OSINT Framework**

By Gh0st-Bx1 | github.com/Ghost-Bx1

---

## Description

ghost-osint performs extended open-source intelligence gathering. It mines certificate transparency logs, checks breach databases, performs WHOIS/DNS/ASN lookups, generates GitHub dork URLs, searches public paste sites, and enumerates employee patterns.

## Usage

```
python ghost-osint.py --target example.com --all
python ghost-osint.py --target example.com --certs --whois --subdomains
python ghost-osint.py --email user@example.com --breach --hibp-key YOUR_KEY
python ghost-osint.py --target example.com --github --paste
python ghost-osint.py --ip 1.2.3.4 --asn
python ghost-osint.py --target example.com --all -o osint.json
```

## Options

| Flag | Description |
|------|-------------|
| `--target` / `-t` | Target domain |
| `--email` / `-e` | Email address for breach check |
| `--ip` | IP address for ASN lookup |
| `--hibp-key` | HaveIBeenPwned API v3 key |
| `--breach` | Check email in breach databases (HIBP) |
| `--whois` | WHOIS + DNS record lookup |
| `--certs` | Certificate transparency via crt.sh |
| `--github` | GitHub dork URL generation |
| `--paste` | Pastebin/public paste search |
| `--employees` | Employee enumeration hints |
| `--subdomains` | Subdomain brute-force (built-in wordlist) |
| `--asn` | ASN lookup via Cymru |
| `--all` / `-a` | Run all modules |
| `--output` / `-o` | Save results as JSON |
| `--timeout` | HTTP timeout in seconds (default: 10) |

## Modules

| Module | Source | Notes |
|--------|--------|-------|
| `--certs` | crt.sh | Certificate transparency - finds subdomains |
| `--whois` | WHOIS servers | Registrar, creation date, registrant |
| `--breach` | HaveIBeenPwned v3 | Requires paid API key |
| `--github` | GitHub Search | Generates dork URLs (requires manual browsing) |
| `--paste` | psbdmp.ws | Pastebin dump search |
| `--employees` | LinkedIn/Hunter | Generates manual check URLs + email patterns |
| `--subdomains` | DNS brute-force | ~60 common subdomains, multithreaded |
| `--asn` | Cymru WHOIS | ASN, prefix, org, country |

## Notes

- HaveIBeenPwned breach check requires a paid API key (hibp.haveibeenpwned.com)
- GitHub dorks generate URLs only - actual search requires browser authentication
- Employee enumeration generates manual check URLs; no scraping performed

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)
