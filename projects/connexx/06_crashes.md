# Crashes & Issues — MVAI Connexx

| Datum | Issue | Oorzaak | Fix | Preventie |
|-------|-------|---------|-----|-----------|
| 2026-03-12 | Hostinger API error 1016 (Cloudflare) | Direct IP call geblokkeerd door Cloudflare | Manuele DNS setup via hPanel | API token geldig houden, fallback plan |
| 2026-03-12 | apt mirror 404 op VPS | Proxy `21.0.0.101` serveert oude packages | `apt install nginx=1.24.0-2ubuntu7 --allow-downgrades` | VPS infra documenteren |
| 2026-03-12 | DNS resolution failure Python | Container DNS resolver niet geconfigureerd | curl werkt via proxy, Python socket niet | Gebruik curl voor externe requests op VPS |
| 2026-03-12 | SyntaxError api.py op Render | Corrupte `h` prefix in bestand | Verwijderd in commit | Pre-commit syntax check toevoegen |
| 2026-03-14 | Hostinger MCP API error 1003 | Direct IP access geblokkeerd door Cloudflare | Manuele acties via hPanel | API token configureren met juiste origin header |
