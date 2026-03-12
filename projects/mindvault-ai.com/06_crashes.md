# Crashes & Issues — mindvault-ai.com

| Datum | Issue | Oorzaak | Fix | Preventie |
|-------|-------|---------|-----|-----------|
| 2026-03-12 | Hostinger API error 1016 | Cloudflare → origin DNS issue aan Hostinger kant | Manuele DNS setup via hPanel | API token geldig houden, monitor API |
| 2026-03-12 | apt mirror 404 op VPS | Proxy `21.0.0.101` dient oude packages niet | `apt install nginx=1.24.0-2ubuntu7 --allow-downgrades` | VPS infra documenteren |
| 2026-03-12 | DNS resolution failure Python | Container DNS resolver niet geconfigureerd | curl werkt via proxy, Python socket niet | Gebruik curl voor externe requests op VPS |
