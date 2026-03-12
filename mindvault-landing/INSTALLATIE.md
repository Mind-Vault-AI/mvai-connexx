# Installatie — Mind Vault AI WordPress Theme

## Vereisten
- WordPress 6.x met Astra theme geïnstalleerd
- hPanel toegang (hostinger.com)

## Stappen (~5 minuten)

### 1. ZIP aanmaken
Zip de volledige `mindvault-landing/` map:
- Windows: rechtermuisknop → Compressen naar ZIP
- Mac: rechtermuisknop → Compress
- Resultaat: `mindvault-landing.zip`

### 2. Uploaden via WordPress
1. Ga naar: **WordPress Admin** (mindvault-ai.com/wp-admin)
2. Menu: **Weergave** → **Thema's**
3. Klik: **Nieuw toevoegen** → **Thema uploaden**
4. Selecteer `mindvault-landing.zip` → **Nu installeren**
5. Klik: **Activeren**

### 3. Homepage instellen
1. Menu: **Pagina's** → **Nieuwe pagina**
2. Titel: `Home` → Publiceer
3. Menu: **Instellingen** → **Lezen**
4. Selecteer: **Statische pagina** → **Startpagina: Home**
5. Opslaan

### 4. Google Analytics activeren
Open `front-page.php` (via hPanel → File Manager of BOX Drive FTP)
Vervang op regel 8:
```
G-XXXXXXXXXX
```
Door jouw GA4 property ID (bijv. `G-ABC123DEF4`)

### 5. Social media links invullen
In `front-page.php`, zoek op `href="#"` en vervang met echte URLs:
- TikTok: `https://www.tiktok.com/@mindvaultai`
- Instagram: `https://www.instagram.com/mindvaultai`
- YouTube: `https://www.youtube.com/@mindvaultai`
- etc.

## Klaar!
Bezoek mindvault-ai.com — de nieuwe dark landing page is live.

## Support
info@mindvault-ai.com
