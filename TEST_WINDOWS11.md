# 🪟 Android App Testen op Windows 11 (Lenovo Laptop)

**Voor:** Windows 11 gebruikers
**Hardware:** Lenovo laptop
**Doel:** Veilig Android app testen ZONDER Play Store

---

## ✅ STAP-VOOR-STAP (Windows 11)

### Stap 1: Download Android Studio

**Direct download link:**
```
https://redirector.gvt1.com/edgedl/android/studio/install/2023.3.1.18/android-studio-2023.3.1.18-windows.exe
```

Of via website: https://developer.android.com/studio

**Bestandsgrootte:** ~1 GB
**Installatie ruimte:** ~4 GB

### Stap 2: Installeer Android Studio

```
1. Dubbelklik android-studio-2023.3.1.18-windows.exe

2. Setup wizard:
   ✅ "Android Studio"
   ✅ "Android Virtual Device" (emulator)
   → Next

3. Install Location: C:\Program Files\Android\Android Studio
   → Next

4. Start Menu Folder: Android Studio
   → Install

5. Wacht 5-10 minuten (installeert bestanden)

6. "Finish" → Android Studio start automatisch
```

### Stap 3: First-Time Setup Wizard

```
1. "Import Android Studio Settings"
   → "Do not import settings"
   → OK

2. "Welcome"
   → Next

3. "Install Type"
   → "Standard" (aanbevolen)
   → Next

4. "Select UI Theme"
   → Kies: "Darcula" (dark) of "Light"
   → Next

5. "Verify Settings"
   → Android SDK Location: C:\Users\[JOUW NAAM]\AppData\Local\Android\Sdk
   → Next

6. "License Agreement"
   → Accepteer alle licenses (scroll naar beneden, klik Accept)
   → Finish

7. Wacht 10-15 minuten (downloadt Android SDK, emulator images)
```

### Stap 4: Open MVAI Connexx Project

```
1. Android Studio hoofdscherm
   → "Open" (of File → Open)

2. Navigate naar je project folder:
   C:\Users\[JOUW NAAM]\...\mvai-connexx\android

3. Klik "OK"

4. Gradle Sync start automatisch
   → Zie "Gradle Build" in bottom panel
   → Wacht 5-10 minuten (eerste keer duurt lang)
   → Je ziet "BUILD SUCCESSFUL" in build output
```

**Als je errors ziet:**
```
Tools → SDK Manager
→ SDK Platforms tab: Installeer "Android 14.0 (U)" (API 34)
→ SDK Tools tab: Installeer "Android SDK Build-Tools 34"
→ Apply → OK
```

### Stap 5: Maak Virtual Device (Emulator)

```
1. In Android Studio:
   Tools → Device Manager

2. "Create Device" knop (+ icoon)

3. Select Hardware:
   → Category: Phone
   → Kies: "Pixel 6 Pro" (6.7", 1440x3120)
   → Next

4. System Image:
   → Release Name: "UpsideDownCake" (Android 14.0, API 34)
   → Als "Download" link staat → klik + wacht (~1 GB download)
   → Als "x86_64" staat → selecteer die
   → Next

5. Verify Configuration:
   → AVD Name: "Pixel_6_Pro_API_34"
   → Startup orientation: Portrait
   → Show Advanced Settings (optioneel):
     - RAM: 2048 MB (2 GB)
     - Internal Storage: 2048 MB
   → Finish
```

### Stap 6: Wijzig APP_URL naar Lokaal

```
1. In Android Studio, open:
   app → src → main → java → com.mindvault.mvaiconnexz → MainActivity.java

2. Zoek regel 27:
   private static final String APP_URL = "https://mvai-connexx.com";

3. Wijzig naar:
   private static final String APP_URL = "http://10.0.2.2:5000";

4. Save (Ctrl+S)
```

**Waarom 10.0.2.2?**
Dit is speciaal Android emulator adres voor "localhost op je laptop"

### Stap 7: Start Flask App Lokaal

**Open PowerShell of Command Prompt:**

```powershell
# Navigate naar project
cd C:\Users\[JOUW NAAM]\...\mvai-connexx

# Check Python geïnstalleerd
python --version
# Moet zien: Python 3.9+

# Als Python niet gevonden:
# Download: https://www.python.org/downloads/windows/
# → Python 3.11.x, installeer, enable "Add to PATH"

# Start Flask app
python app.py

# Je moet zien:
# * Running on http://127.0.0.1:5000
# (Press CTRL+C to quit)
```

**LAAT DIT TERMINAL VENSTER OPEN!** Flask moet blijven draaien.

### Stap 8: Run Android App in Emulator

```
1. In Android Studio:
   → Klik groene "Run" knop (▶) rechts bovenin
   → Of: Shift+F10

2. "Select Deployment Target"
   → Kies "Pixel_6_Pro_API_34"
   → OK

3. Emulator start op (30 sec - 1 min)
   → Nieuw venster opent (Android phone op je scherm)

4. App installeert automatisch
   → Splash screen verschijnt
   → MVAI Connexx app opent

5. Je zou Flask login scherm moeten zien!
```

### Stap 9: Test Alle Features

**Test in emulator:**

✅ **Login:**
- Klik "Customer Login" (of admin)
- Vul access code in (gebruik demo code of maak nieuwe aan)
- Check of je dashboard ziet

✅ **Navigatie:**
- Klik menu items (Logs, Analytics, API Keys, etc.)
- Check of pagina's laden
- Druk Android "Back" button (◀ in emulator)
- Moet teruggaan naar vorige pagina (niet app sluiten)

✅ **Features:**
- Open Logs pagina → zie je data?
- Open Analytics → zie je grafieken?
- Probeer CSV export → download werkt?
- Open Subscription → zie je pricing tiers?

✅ **External Links:**
- Klik upgrade naar "Particulier" (€19)
- Moet externe browser openen (Gumroad)
- Niet binnen app blijven!

✅ **Offline Test:**
- In emulator: swipe down from top
- Settings → Network & Internet → WiFi → Off
- App moet toast tonen: "Geen internetverbinding"

✅ **Rotation:**
- In emulator: Ctrl+F11 (rotate screen)
- App moet landscape mode tonen
- Content moet responsive blijven

### Stap 10: Check Logs voor Errors

```
1. In Android Studio (niet emulator):
   View → Tool Windows → Logcat

2. Filter dropdown (links) → "No Filters"
   → Type in filter box: "MVAI" of "MainActivity"

3. Check op RODE regels (errors)
   → Groene/blauwe regels = OK (info/debug)
   → Gele regels = warnings (meestal OK)
   → Rode regels = ERRORS (moet gefixed worden)

4. Als errors:
   → Copy error message
   → Stuur naar mij
   → Ik debug + fix
```

---

## 🐛 WINDOWS 11 TROUBLESHOOTING

### "Android Studio not opening"
```powershell
# Check Java installed:
java -version

# Als niet gevonden:
# Android Studio komt met embedded JDK, maar soms:
# Download JDK 17: https://adoptium.net/temurin/releases/
```

### "Gradle sync failed"
```
File → Invalidate Caches → Invalidate and Restart
→ Wacht op restart
→ Gradle sync zou opnieuw moeten proberen
```

### "Emulator not starting"
```
1. Check Hyper-V enabled:
   → Windows Search: "Turn Windows features on or off"
   → Enable "Hyper-V" + "Windows Hypervisor Platform"
   → Restart laptop

2. Check BIOS virtualization:
   → Restart laptop → F2 (Lenovo) → BIOS
   → Enable "Intel VT-x" of "AMD-V"
   → Save & Exit
```

### "Emulator slow"
```
Android Studio → Tools → SDK Manager → SDK Tools
→ Install "Intel x86 Emulator Accelerator (HAXM)"
→ Apply → OK
→ Restart emulator
```

### "Python not found"
```powershell
# Download Python:
https://www.python.org/downloads/windows/

# Installeer Python 3.11.x
# ⚠️ ENABLE "Add Python to PATH" tijdens installatie!

# Verify:
python --version
```

### "Flask app won't start"
```powershell
# Install dependencies:
cd C:\Users\[JOUW NAAM]\...\mvai-connexx
pip install -r requirements.txt

# Start:
python app.py
```

### "WebView blank in emulator"
```
1. Check Flask app draait (http://localhost:5000 in browser moet werken)
2. Check APP_URL = "http://10.0.2.2:5000" (niet localhost!)
3. Check Logcat voor JavaScript errors
```

### "Windows Firewall blocks Flask"
```
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Change settings → Allow another app
4. Browse → Selecteer python.exe
5. Enable "Private" + "Public"
6. OK
```

---

## 📋 WINDOWS 11 SHORTCUTS

**In Android Studio:**
- `Ctrl+F9` - Build project
- `Shift+F10` - Run app
- `Ctrl+S` - Save file
- `Ctrl+Alt+L` - Format code
- `Alt+F12` - Open terminal

**In Emulator:**
- `Ctrl+F11` - Rotate screen
- `Ctrl+F12` - Toggle keyboard
- `Ctrl+M` - Open emulator menu
- `Ctrl+K` - Keyboard input

**PowerShell:**
- `Ctrl+C` - Stop Flask app
- `Ctrl+L` - Clear terminal
- `cd` - Change directory
- `dir` - List files

---

## ⚙️ WINDOWS 11 SYSTEEM VEREISTEN

**Minimaal:**
- RAM: 8 GB (voor Android Studio + Emulator)
- Disk: 8 GB vrije ruimte
- Processor: Intel i5 of equivalent
- Virtualization: Enabled in BIOS

**Aanbevolen (Lenovo laptop):**
- RAM: 16 GB (voor soepele emulator)
- SSD: Voor snelle builds
- Dedicated GPU: Helpt emulator performance

**Check je specs:**
```powershell
# RAM:
systeminfo | findstr "Total Physical Memory"

# Processor:
wmic cpu get name

# Disk space:
wmic logicaldisk get size,freespace,caption
```

---

## 🎯 COMPLETE TEST FLOW (Windows 11)

**Terminal 1 (PowerShell - Flask):**
```powershell
cd C:\Users\[JOUW NAAM]\...\mvai-connexx
python app.py
# LAAT OPEN!
```

**Terminal 2 (Android Studio):**
```
1. Open project: android/
2. Wijzig APP_URL → http://10.0.2.2:5000
3. Start emulator: Run (▶)
4. Test app in emulator
5. Check Logcat voor errors
```

**Browser (Optional - verify Flask):**
```
http://localhost:5000
→ Zou login scherm moeten tonen
→ Bevestigt Flask werkt
```

---

## ✅ SUCCESS CHECKLIST

**Setup compleet als:**
- [ ] Android Studio installed
- [ ] Emulator created (Pixel 6 Pro)
- [ ] Project opens zonder Gradle errors
- [ ] Flask app start (python app.py)
- [ ] App runs in emulator
- [ ] Login scherm zichtbaar in emulator

**Ready voor testing als:**
- [ ] Login werkt
- [ ] Dashboard navigatie werkt
- [ ] Features laden (Logs, Analytics)
- [ ] Back button werkt
- [ ] Geen crashes in Logcat

**Ready voor Play Store als:**
- [ ] ALLE features getest
- [ ] 0 errors in Logcat
- [ ] Offline mode werkt
- [ ] External links werken
- [ ] App voelt smooth/responsive

---

## 🚀 VOLGENDE STAPPEN

**Na succesvolle emulator test:**

1. **Optie A:** Test op fysiek Android device
   - Build APK: `./gradlew assembleDebug`
   - Install via USB: `adb install app-debug.apk`

2. **Optie B:** Internal Testing (Play Console)
   - Maak keystore
   - Build AAB: `./gradlew bundleRelease`
   - Upload naar Internal Testing track

3. **Optie C:** Production release
   - Alleen na 100% test success
   - Upload naar Production track
   - Submit for review (24-48u)

---

## 📞 HULP NODIG?

**Als je vastloopt:**
1. Check Logcat in Android Studio (rode errors)
2. Screenshot van error
3. Stuur naar mij
4. Ik debug + fix + push update

**Common Windows 11 issues:**
- Hyper-V niet enabled → Enable in Windows Features
- Firewall blokkeert Flask → Allow python.exe
- Python not found → Add to PATH tijdens installatie
- Emulator slow → Install HAXM accelerator

---

**KLAAR VOOR WINDOWS 11! 🪟**

Download Android Studio → Volg stappen hierboven → Test veilig lokaal!

Totale tijd: ~1 uur (eerste keer setup + test)
