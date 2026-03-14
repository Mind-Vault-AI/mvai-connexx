# MVAI Verplichte Werkwijze — Godmode Protocol

> "Je kunt alleen jezelf verbeteren door fouten en klantfeedback te accepteren,
> issues te omarmen en asap te verbeteren. Zo word en blijf je geloofwaardig."

---

## Vaste Werkcyclus (elk project, elke sprint)

| Stap | Actie | Output |
|------|-------|--------|
| 1 RESEARCH | Wat vraagt de markt? Valideer EERST. | `01_research.md` |
| 2 SPAR SESSIE | Brainstorm + overeenstemming bereiken | `02_spar_sessie.md` |
| 3 OVEREENGEKOMEN | Schriftelijk vastgelegd (spec) | `03_spec.md` |
| 4 BUILD | 99.9 SLA kwaliteitsstandaard | Code + tests |
| 5 TEST | QA voor delivery | Testrapport |
| 6 DEPLOY | Live met monitoring | Deploy log |
| 7 MONITOR | Uptime, errors, crashes loggen | `06_crashes.md` |
| 8 CRASH REPORT | Elke issue gedocumenteerd met oorzaak + fix | `06_crashes.md` |
| 9 LESSONS LEARNED | Na elke sprint/project | `07_lessons.md` |
| 10 VERBETER | Werkwijze + product updaten op basis van feedback | Nieuwe cyclus |

---

## Kwaliteitsstandaarden

- **99.9 SLA**: Uptime bewaking, auto-restart processen
- **Crash borging**: Elke fout gelogd met timestamp, oorzaak, fix, preventie
- **Marktvalidatie**: Research-vragen beantwoord VÓÓR build
- **Godmode**: Na overeenstemming → volledige autonomie
- **Infra-discipline**: ALLEEN Render + Hostinger — geen nieuwe abonnementen

---

## Bouw Principes (altijd)

### Frontend
- Responsive (mobile first, 768px / 1024px breakpoints)
- Dark MVAI huisstijl: `#0f1520` navy, `#5aafaf` teal, Inter font
- Smooth animaties (IntersectionObserver fade-ups)
- Toegankelijk, snel ladend

### Backend
- Rate limiting op alle endpoints
- Input validatie + sanitatie
- CSRF bescherming
- HTTPS only
- Honeypot op alle formulieren

### Exit Strategie
- Alles self-hosted op Render + Hostinger
- CSV export van alle data (geen vendor lock-in)
- Open source dependencies
- Database backup dagelijks

### Safety
- Geen plaintext secrets in code of git
- GDPR compliant (EU Frankfurt hosted)
- Multi-tenant isolatie
- Encrypted customer API keys

---

## Infra Overzicht

| Service | Platform | Status | Aanraken? |
|---------|----------|--------|-----------|
| apexflash.pro | Render + Hostinger | ✅ Actief | Nee |
| connexx.mindvault-ai.com | Hostinger VPS | ✅ Actief | Alleen via ticket |
| mindvault-ai.com | Hostinger WordPress | 🔧 In build | Ja |

---

## Contact & Socials

- **Email**: info@mindvault-ai.com
- **LinkedIn**: https://www.linkedin.com/company/mindvault-ai
- **Socials**: TikTok, Reddit, YouTube, Telegram, X, Pinterest, Discord, Instagram, Facebook, Snapchat

---

## BOX Drive Mapstructuur

```
BOX Drive/MVAI/
├── 00_WERKWIJZE/               ← Dit document + updates
├── 01_PROJECTEN/
│   ├── mindvault-ai.com/       ← Sync met: projects/mindvault-ai.com/
│   ├── connexx/                ← Sync met: projects/connexx/
│   └── apexflash/              ← Sync met: projects/apexflash/
├── 02_TEMPLATES/               ← Herbruikbare docs
└── 03_ARCHIEF/                 ← Afgeronde projecten
```

Sync: Kopieer de inhoud van `projects/` naar BOX Drive na elke sprint.

---

## Lessons Learned Register

| Datum | Project | Issue | Fix | Preventie |
|-------|---------|-------|-----|-----------|
| 2026-03-12 | connexx | Hostinger API error 1016 (Cloudflare) | Manuele DNS setup | API token geldig houden, fallback plan |
| 2026-03-12 | infra | apt mirror proxy broken op VPS | `--allow-downgrades` flag | Document VPS apt issues |
