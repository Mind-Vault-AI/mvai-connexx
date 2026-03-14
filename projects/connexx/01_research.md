# Research — MVAI Connexx

## Marktvalidatie

| Vraag | Antwoord |
|-------|----------|
| Wat is het product? | Multi-tenant AI platform voor bedrijven en particulieren |
| Wie is de doelgroep? | MKB + particulieren die AI-tools willen zonder technische kennis |
| Wat is de pijnpunt? | Toegang tot AI-tools is versnipperd, duur en complex |
| Concurrentie? | ChatGPT Plus, Jasper, Copy.ai — maar geen NL-focused multi-tenant SaaS |
| Monetisatie? | Gumroad abonnementen (Starter/Professional/Enterprise) |

## Product Features

- Multi-tenant customer management
- BYOK (Bring Your Own Key) AI providers
- Integraties (webhooks, API keys)
- Analytics dashboard
- AI assistent (OpenAI + Anthropic)
- Export CSV / data portabiliteit
- Admin beheer panel

## Technische Stack

- Backend: Python Flask
- Database: SQLite (persistent volume)
- Hosting: Hostinger VPS (connexx.mindvault-ai.com)
- Deploy: GitHub Actions → SSH → systemd
- Betalingen: Gumroad
