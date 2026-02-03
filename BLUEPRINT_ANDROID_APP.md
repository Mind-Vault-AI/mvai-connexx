# 📱 MVAI Connexx Android App - Blueprint & Handover

**Aangemaakt:** 2026-01-22
**Doel:** Google Play Store deployment voor MVAI Connexx
**Type:** Android WebView app (native container voor Flask web app)
**Status:** 🔨 In ontwikkeling

---

## 🎯 Architectuur Overzicht

```
┌─────────────────────────────────────────┐
│   Google Play Store                     │
│   (klanten downloaden app)              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   MVAI Connexx.apk/.aab                 │
│   Android WebView Container             │
│   - Splash screen                       │
│   - Progress bar                        │
│   - Offline detectie                    │
│   - Push notifications (future)         │
└──────────────┬──────────────────────────┘
               │
               │ HTTPS
               ▼
┌─────────────────────────────────────────┐
│   Hostinger VPS                         │
│   https://mvai-connexx.com              │
│   (Flask app draait hier)               │
│   - All business logic                  │
│   - Database (SQLite)                   │
│   - Payment processing                  │
│   - AI Assistant                        │
└─────────────────────────────────────────┘
```

---

## 📂 Android Project Structuur

```
android/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/mindvault/mvaiconnexz/
│   │       │   └── MainActivity.java          # WebView implementation
│   │       ├── res/
│   │       │   ├── layout/
│   │       │   │   └── activity_main.xml      # UI layout
│   │       │   ├── drawable/
│   │       │   │   ├── ic_launcher.png        # App icon (512x512)
│   │       │   │   └── splash_logo.png        # Splash screen
│   │       │   ├── values/
│   │       │   │   ├── strings.xml            # App naam, URL config
│   │       │   │   ├── colors.xml             # Brand kleuren
│   │       │   │   └── styles.xml             # App theme
│   │       │   └── xml/
│   │       │       └── network_security_config.xml  # HTTPS config
│   │       └── AndroidManifest.xml            # Permissions, metadata
│   ├── build.gradle                           # App dependencies
│   └── proguard-rules.pro                     # Code obfuscation
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties          # Gradle version
├── build.gradle                               # Project config
├── settings.gradle                            # Module settings
└── README_ANDROID.md                          # Build instructies
```

---

## 🔧 Technische Specificaties

### App Details
- **Package Name:** `com.mindvault.mvaiconnexz`
- **App Name:** MVAI Connexx
- **Version Code:** 1
- **Version Name:** 1.0.0
- **Min SDK:** 21 (Android 5.0 Lollipop - 94% coverage)
- **Target SDK:** 34 (Android 14)
- **Compile SDK:** 34

### URL Configuration
- **Production URL:** `https://mvai-connexx.com`
- **Staging URL:** `https://mvai-connexx.onrender.com` (als fallback)
- **Local Testing:** `http://10.0.2.2:5000` (Android Emulator → localhost)

### Permissions
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### Features
✅ **WebView met JavaScript enabled**
✅ **DOM Storage enabled** (voor login sessies)
✅ **File upload support** (voor CSV imports)
✅ **Offline detectie** (toast message als geen internet)
✅ **HTTPS enforced** (network security config)
✅ **Progress bar** tijdens laden
✅ **Splash screen** (MVAI branding)
✅ **Back button** navigeert binnen app
✅ **Pull-to-refresh**

❌ **Push notifications** (future - na launch)
❌ **Offline caching** (future - PWA upgrade)

---

## 📋 Bestaande Features (Blijven Intact!)

**KRITIEK:** Android app is alleen een CONTAINER. Alle features blijven in Flask app:

✅ Multi-tenant database (21 tables)
✅ Payment processing (Gumroad + Stripe)
✅ Email notifications (4 types)
✅ Subscription management (6 pricing tiers)
✅ AI Assistant
✅ Analytics dashboard
✅ API keys
✅ Security monitoring
✅ Admin panel
✅ Customer portal
✅ 20 HTML templates

**NIETS hiervan wordt aangepast!** Android app laadt gewoon de website.

---

## 🚀 Build Process

### Stap 1: Android Studio Setup
```bash
# Download Android Studio: https://developer.android.com/studio
# Installeer Java JDK 17
# Installeer Android SDK via Android Studio
```

### Stap 2: Project Aanmaken
```bash
cd /home/user/mvai-connexx
mkdir -p android
cd android

# Initialiseer Gradle project
gradle init --type basic
```

### Stap 3: Build APK/AAB
```bash
cd android
./gradlew assembleRelease          # Bouwt .apk (voor testing)
./gradlew bundleRelease             # Bouwt .aab (voor Play Store)
```

Output:
- `.apk` → `app/build/outputs/apk/release/app-release.apk`
- `.aab` → `app/build/outputs/bundle/release/app-release.aab`

### Stap 4: Signing (Vereist voor Play Store)
```bash
# Genereer keystore (1x, bewaar goed!)
keytool -genkey -v -keystore mvai-connexx.keystore \
  -alias mvai-connexx-key \
  -keyalg RSA -keysize 2048 -validity 10000

# Sign AAB
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore mvai-connexx.keystore \
  app/build/outputs/bundle/release/app-release.aab \
  mvai-connexx-key
```

### Stap 5: Upload naar Play Console
1. Ga naar https://play.google.com/console
2. Create app → "MVAI Connexx"
3. Upload signed `.aab`
4. Vul metadata in (screenshots, beschrijving)
5. Submit for review

---

## 🎨 Branding Assets Needed

### App Icon (MOET GEMAAKT WORDEN)
- **512x512 PNG** - Play Store listing
- **192x192 PNG** - Launcher icon (hdpi)
- **144x144 PNG** - Launcher icon (xhdpi)
- **96x96 PNG** - Launcher icon (xxhdpi)
- **72x72 PNG** - Launcher icon (xxxhdpi)

**Kleuren:** #00ff41 (neon green) + #1a1a1a (dark)
**Logo:** "MVAI" tekst + circuit board pattern achtergrond

### Screenshots (Voor Play Store)
- 1080x1920 (phone) - minimaal 2 screenshots
- Dashboard view
- Login screen
- Analytics view

### Feature Graphic
- 1024x500 PNG - Header image in Play Store

---

## 🔐 Security Checklist

✅ **HTTPS only** (network_security_config.xml)
✅ **Certificate pinning** (voor productie domein)
✅ **Obfuscation** (ProGuard enabled)
✅ **API keys NIET in app** (alles server-side)
✅ **SSL verification** enabled
✅ **File upload filtering** (alleen CSV/safe types)

---

## 📊 Testing Strategie

### Pre-Launch Tests:
1. ✅ **Emulator test** - Android 5.0, 10, 14
2. ✅ **Physical device test** - minimaal 1 echt toestel
3. ✅ **Network scenarios:**
   - WiFi verbinding
   - Mobile data (4G/5G)
   - Offline → toast message werkt?
   - Slow connection → progress bar werkt?
4. ✅ **Functionaliteit:**
   - Login flow
   - Dashboard navigatie
   - CSV export download
   - Payment redirect naar Gumroad
   - AI assistant chat
5. ✅ **Back button** gedrag
6. ✅ **Rotation** (portrait/landscape)

### Play Console Internal Testing Track:
- Upload naar "Internal testing"
- Test met 2-3 testers
- Fix bugs
- Promote naar "Production"

---

## 📝 Google Play Store Metadata

### Korte Beschrijving (80 chars):
> Logistieke data-assistent met AI. Excel-chaos opgelost. Voor MKB transport.

### Lange Beschrijving (4000 chars):
```
MVAI Connexx - De Logistieke Data-Assistent voor MKB

Verdrinkt jouw bedrijf in Excel-sheets? Verzendingen, voorraad, kosten, routes - allemaal losse bestanden zonder overzicht?

MVAI Connexx centraliseert alle logistieke data in 1 dashboard met ingebouwde AI-copiloot.

🎯 VOOR WIE?
- Transport & logistiek bedrijven (2-50 medewerkers)
- Webshops met eigen distributie
- Groothandels met vrachtbeheer
- Iedereen die meer dan 100 verzendingen/maand doet

✅ WAT KUN JE?
• Centraal logboek voor ALLE data
• AI assistent: "Hoeveel kostten route 12 vorige maand?" → Direct antwoord
• Real-time kostenoverzicht
• Analytics dashboard met grafieken
• Multi-user samenwerking
• CSV import/export
• API integratie met je systemen
• Security monitoring

💰 PRICING:
• Demo - Gratis (100 logs)
• Particulier - €19/maand
• Starter - €29/maand
• MKB - €49/maand
• Professional - €99/maand
• Enterprise - €299/maand

Probeer gratis. Opzeggen kan altijd.

🔐 VEILIG:
• Multi-tenant isolatie
• HTTPS encryptie
• Geen data-deling tussen klanten
• GDPR compliant

📞 SUPPORT:
• Email: info@mindvault-ai.com
• Website: https://mvai-connexx.com
```

### Categorie:
- Primair: **Business**
- Secundair: **Productivity**

### Tags:
logistics, transport, fleet management, business intelligence, AI assistant, data analytics, MKB, Excel alternative

---

## 🎯 Success Metrics

### Week 1:
- ✅ App live in Play Store
- 🎯 10 downloads (vrienden/familie test)
- 🎯 0 crashes

### Maand 1:
- 🎯 50 downloads
- 🎯 10 actieve gebruikers
- 🎯 2 betalende klanten (€19-€49 tier)
- 🎯 4.0+ star rating

### Maand 3:
- 🎯 200 downloads
- 🎯 50 actieve gebruikers
- 🎯 10 betalende klanten
- 🎯 €300+ MRR

---

## ⚠️ KRITIEKE WAARSCHUWINGEN

### ❌ NIET DOEN:
1. **Bestaande Flask code NIET aanpassen** - Android is alleen container
2. **Geen API keys in Android code** - alles server-side
3. **Geen database in app** - alles blijft op server
4. **Geen lokale opslag van klantdata** - GDPR risk

### ✅ WEL DOEN:
1. **URL configureerbaar maken** - makkelijk switchen tussen staging/prod
2. **Error handling** - duidelijke messages als server down is
3. **Versienummering** - elke Play Store update = version code +1
4. **Keystore BACKUP** - verlies = nooit meer updates kunnen pushen!

---

## 📞 Handover Checklist

Voor volgende developer/maintainer:

- [ ] Android Studio geïnstalleerd (versie 2024.1+)
- [ ] Java JDK 17 geïnstalleerd
- [ ] `mvai-connexx.keystore` bestand (KRITIEK - BEWAAR VEILIG!)
- [ ] Keystore wachtwoord (in password manager)
- [ ] Google Play Console toegang (info@mindvault-ai.com)
- [ ] Hostinger VPS IP/domein configuratie
- [ ] Test devices voor QA (minimaal 1 Android phone)

---

## 🔄 Update Process (Future)

Als Flask app updates krijgt:
1. Deploy update naar Hostinger VPS
2. Test in browser (https://mvai-connexx.com)
3. Test in Android app (app herlaadt automatisch nieuwe versie)
4. **GEEN** nieuwe Android app build nodig!

Als Android container updates nodig heeft (nieuwe features, UI fixes):
1. Update Android code
2. Verhoog `versionCode` in `build.gradle`
3. Build nieuwe `.aab`
4. Sign met keystore
5. Upload naar Play Console
6. Submit for review (24-48u)

---

## 📚 Resources

- [Android WebView Guide](https://developer.android.com/develop/ui/views/layout/webapps/webview)
- [Play Console Help](https://support.google.com/googleplay/android-developer)
- [App Signing Best Practices](https://developer.android.com/studio/publish/app-signing)

---

**Gemaakt volgens LEAN/PDCA principes:**
- ✅ Plan: Deze blueprint
- ⏳ Do: Android Studio build (volgende stap)
- ⏳ Check: Internal testing track
- ⏳ Act: Production release

**99.9% SLA doel:** App uptime = Flask server uptime (Hostinger VPS monitoring vereist)

---

_Dit document wordt up-to-date gehouden bij elke Android app wijziging._
