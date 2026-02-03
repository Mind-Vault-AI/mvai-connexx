# MVAI Connexx - Android App Build Instructies

## 📋 Vereisten

### Software:
- **Android Studio** - Download: https://developer.android.com/studio
- **Java JDK 17** - Download: https://adoptium.net/temurin/releases/
- **Git** - Voor repository management

### Accounts:
- **Google Play Console** - https://play.google.com/console (€25 eenmalig)
- Account: info@mindvault-ai.com

---

## 🚀 Build Process

### Stap 1: Open Project in Android Studio

```bash
# Open Android Studio
# File → Open → Selecteer /mvai-connexx/android folder
```

### Stap 2: Sync Gradle

Android Studio zal automatisch Gradle dependencies downloaden.

Als je errors ziet:
- Tools → SDK Manager → Installeer Android SDK 34
- File → Sync Project with Gradle Files

### Stap 3: Test in Emulator (Lokaal)

```bash
# Maak emulator aan:
# Tools → Device Manager → Create Device
# Kies: Pixel 6 Pro, Android 14 (API 34)

# Run app:
# Klik groene "Run" knop (of Shift+F10)
```

**Wijzig URL voor lokaal testen:**
- Open `MainActivity.java`
- Wijzig: `private static final String APP_URL = "http://10.0.2.2:5000";`
- Dit wijst naar localhost:5000 op je machine

### Stap 4: Build Release APK (Voor Testing)

```bash
cd android
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release-unsigned.apk`

### Stap 5: Build Release AAB (Voor Play Store)

```bash
cd android
./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

---

## 🔐 App Signing (VERPLICHT voor Play Store)

### Eenmalig: Keystore Aanmaken

```bash
cd android/app

# Genereer keystore
keytool -genkey -v -keystore mvai-connexx.keystore \
  -alias mvai-connexx-key \
  -keyalg RSA -keysize 2048 -validity 10000

# Vul in:
# - Wachtwoord: [BEWAAR DIT VEILIG!]
# - Naam: Mind Vault AI
# - Organisatie: Mind Vault AI
# - Stad: Amsterdam
# - Land: NL
```

**⚠️ KRITIEK:** Bewaar `mvai-connexx.keystore` + wachtwoord veilig!
- Backup naar USB stick
- Zet in password manager (1Password, Bitwarden)
- **Als je dit verliest = NOOIT meer app updates kunnen pushen!**

### Configureer Signing in build.gradle

Open `android/app/build.gradle` en voeg toe:

```gradle
android {
    ...
    signingConfigs {
        release {
            storeFile file('mvai-connexx.keystore')
            storePassword 'JE_KEYSTORE_WACHTWOORD'
            keyAlias 'mvai-connexx-key'
            keyPassword 'JE_KEY_WACHTWOORD'
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            ...
        }
    }
}
```

**Veiliger:** Gebruik environment variables:

```bash
# In ~/.bashrc of ~/.zshrc
export MVAI_KEYSTORE_PASSWORD="je_wachtwoord"
export MVAI_KEY_PASSWORD="je_wachtwoord"
```

```gradle
signingConfigs {
    release {
        storeFile file('mvai-connexx.keystore')
        storePassword System.getenv('MVAI_KEYSTORE_PASSWORD')
        keyAlias 'mvai-connexx-key'
        keyPassword System.getenv('MVAI_KEY_PASSWORD')
    }
}
```

### Build Signed AAB

```bash
./gradlew bundleRelease

# Output: app/build/outputs/bundle/release/app-release.aab (SIGNED!)
```

---

## 📤 Upload naar Google Play Store

### 1. Google Play Console Setup

https://play.google.com/console

**Account vereist:** info@mindvault-ai.com (€25 eenmalig)

### 2. Create App

- Klik "Create app"
- App naam: **MVAI Connexx**
- Default language: **Nederlands (Nederland)**
- App type: **App**
- Free/Paid: **Free** (in-app purchases via Gumroad)

### 3. App Content

**Privacy Policy URL:** https://mvai-connexx.com/legal

**App Categorie:**
- Category: Business
- Tags: logistics, transport, AI assistant, data analytics

**Target Audience:**
- Age rating: 3+ (Everyone)

**Content Rating:**
- Gebruik Google's vragenlijst → Business app, geen sensitive content

### 4. Store Listing

**Short description (80 chars):**
```
Logistieke data-assistent met AI. Excel-chaos opgelost. Voor MKB transport.
```

**Long description (4000 chars):**
```
MVAI Connexx - De Logistieke Data-Assistent voor MKB

Verdrinkt jouw bedrijf in Excel-sheets? Verzendingen, voorraad, kosten, routes - allemaal losse bestanden zonder overzicht?

MVAI Connexx centraliseert alle logistieke data in 1 dashboard met ingebouwde AI-copiloot.

🎯 VOOR WIE?
• Transport & logistiek bedrijven (2-50 medewerkers)
• Webshops met eigen distributie
• Groothandels met vrachtbeheer
• Iedereen die meer dan 100 verzendingen/maand doet

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
Email: info@mindvault-ai.com
Website: https://mvai-connexx.com
```

**Screenshots (MOET JE NOG MAKEN):**
- Minimaal 2 screenshots (1080x1920)
- Aanbevolen: 4-8 screenshots
- Toon: Login screen, Dashboard, Analytics, AI Assistant

**Feature Graphic:**
- 1024x500 PNG
- Header image in Play Store

**App Icon:**
- 512x512 PNG
- Transparante achtergrond

### 5. Upload AAB

- Production → Releases → Create new release
- Upload `app-release.aab`
- Release notes:
  ```
  Eerste release van MVAI Connexx!

  Features:
  - Logboek voor verzendingen en transacties
  - AI assistent voor data-vragen
  - Analytics dashboard
  - Multi-user samenwerking
  - Veilige multi-tenant opslag
  ```

### 6. Submit for Review

- Review duurt 24-48 uur
- Google test app op malware, policy violations
- Bij goedkeuring: App live in Play Store!

---

## 🔄 Updates Pushen (Future)

### App Update (Nieuwe Android versie)

1. Wijzig `versionCode` en `versionName` in `app/build.gradle`:
   ```gradle
   versionCode 2        // Was 1, nu 2
   versionName "1.1.0"  // Was 1.0.0, nu 1.1.0
   ```

2. Build nieuwe AAB:
   ```bash
   ./gradlew bundleRelease
   ```

3. Upload naar Play Console:
   - Production → Create new release
   - Upload nieuwe AAB
   - Release notes: wat is er nieuw?

### Flask App Update (Geen Android update nodig!)

Als je alleen Flask app wijzigt (nieuwe features, bug fixes):
1. Deploy update naar Hostinger VPS
2. Android app laadt automatisch nieuwe versie
3. **GEEN** nieuwe Android build/upload nodig!

---

## 🐛 Troubleshooting

### "Gradle sync failed"
```bash
# Cleanup en rebuild
cd android
./gradlew clean
./gradlew build
```

### "SDK not found"
- Android Studio → Tools → SDK Manager
- Installeer Android SDK 34
- Accepteer licenses: `./gradlew --refresh-dependencies`

### "Keystore not found"
- Check pad naar keystore in `build.gradle`
- Moet relatief zijn: `file('mvai-connexx.keystore')`

### "INTERNET permission denied"
- Check `AndroidManifest.xml` heeft `<uses-permission android:name="android.permission.INTERNET" />`

### App laadt niet in emulator
- Check `APP_URL` in `MainActivity.java`
- Voor emulator: gebruik `http://10.0.2.2:5000`
- Voor fysiek device: gebruik LAN IP (bijv. `http://192.168.1.100:5000`)

### "WebView blank screen"
- Check browser console in Android Studio Logcat
- JavaScript errors? → Check Flask app console
- Network error? → Check Flask server draait

---

## 📊 Testing Checklist

Voor Play Store upload:

- [ ] App start zonder crashes
- [ ] WebView laadt https://mvai-connexx.com correct
- [ ] Login flow werkt
- [ ] Dashboard navigatie werkt
- [ ] Back button navigeert binnen app
- [ ] Offline detectie toont toast message
- [ ] Progress bar werkt tijdens laden
- [ ] Payment redirect (Gumroad) opent externe browser
- [ ] CSV download werkt
- [ ] App draait op Android 5.0+ (test meerdere versies)
- [ ] Portrait/landscape rotation werkt

---

## 🎯 Launch Checklist

- [ ] Keystore aangemaakt en veilig opgeslagen
- [ ] AAB signed met keystore
- [ ] Google Play Console account actief (€25 betaald)
- [ ] Store listing compleet (screenshots, beschrijving, icon)
- [ ] Privacy policy live op https://mvai-connexx.com/legal
- [ ] Hostinger VPS draait (Flask app bereikbaar via HTTPS)
- [ ] Internal testing gedaan (minimaal 2 testers)
- [ ] AAB uploaded naar Production track
- [ ] Submitted for review

---

## 📞 Support

**Vragen over Android build:**
- Android Docs: https://developer.android.com/docs
- Stack Overflow: https://stackoverflow.com/questions/tagged/android

**Google Play Console issues:**
- Support: https://support.google.com/googleplay/android-developer

**MVAI Connexx specifiek:**
- Email: info@mindvault-ai.com

---

**Succes met de launch! 🚀**

_Vergeet niet: keystore backup maken!_
