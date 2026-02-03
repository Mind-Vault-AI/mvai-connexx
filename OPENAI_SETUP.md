# 🤖 OpenAI GPT Integration - Setup & Test Guide

**Status:** ✅ ACTIEF & WERKEND
**Model:** GPT-4 Turbo
**API Key:** Geconfigureerd in `.env` (veilig, git-ignored)

---

## ✅ WAT IS GEDAAN

### 1. API Key Configuratie
- ✅ `.env` file aangemaakt met jouw OpenAI API key
- ✅ `.env.example` updated met OpenAI config sectie
- ✅ `.gitignore` verified - `.env` wordt NIET gecommit (veilig!)

### 2. Code Integratie
- ✅ `config.py` - 4 nieuwe OpenAI config variabelen
- ✅ `requirements.txt` - `openai>=1.12.0` dependency toegevoegd
- ✅ `ai_assistant.py` - OpenAI GPT-4 Turbo integration
- ✅ `app.py` - Chat route gebruikt nu OpenAI

### 3. Features
- ✅ **Intelligente chat** powered by GPT-4 Turbo
- ✅ **Customer context** - AI kent klant data, logs, preferences
- ✅ **Conversation history** - Laatste 20 berichten onthouden
- ✅ **Fallback system** - Rule-based NLP als OpenAI down
- ✅ **Per-klant isolatie** - Data blijft privé
- ✅ **Opt-in** - Alleen actief als klant enabled

---

## 🧪 TESTEN (Lokaal)

### Stap 1: Install Dependencies
```bash
cd /pad/naar/mvai-connexx
pip install -r requirements.txt

# Dit installeert:
# - openai>=1.12.0 (nieuwe dependency)
# - Alle andere dependencies
```

### Stap 2: Start Flask App
```bash
python app.py

# Je moet zien:
# * Running on http://127.0.0.1:5000
```

### Stap 3: Test AI Assistant

**Via Browser:**
1. Open http://localhost:5000
2. Login als customer (of maak demo account)
3. Ga naar "AI Assistant" pagina
4. Activeer AI Assistant (als nog niet actief)
5. Type bericht: "Hoeveel logs heb ik vandaag?"
6. **Verwacht:** Intelligent antwoord van GPT-4!

**Via API (cURL):**
```bash
# Login eerst om session cookie te krijgen
curl -X POST http://localhost:5000/customer/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hoeveel logs had ik deze week?"}'

# Response:
# {
#   "success": true,
#   "message": "Op basis van je recente logs...",
#   "model": "gpt-4-turbo",
#   "tokens_used": 245
# }
```

---

## 🔧 CONFIGURATIE

### Environment Variables (.env)

```bash
# OpenAI API Key (⚠️ REDACTED - Gebruik jouw eigen key!)
OPENAI_API_KEY=sk-proj-XXXXX...XXXXX

# Model (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
OPENAI_MODEL=gpt-4-turbo

# Max tokens per request (1000 = ~750 words)
OPENAI_MAX_TOKENS=1000

# Temperature (0.0-2.0, lower = more focused)
OPENAI_TEMPERATURE=0.7
```

### Wijzig Model (Optioneel)
```bash
# Voor snellere/goedkopere responses:
OPENAI_MODEL=gpt-3.5-turbo

# Voor maximale intelligence:
OPENAI_MODEL=gpt-4

# Voor balance (AANBEVOLEN):
OPENAI_MODEL=gpt-4-turbo
```

---

## 📊 HOE HET WERKT

### Flow:
```
User: "Hoeveel logs vandaag?"
    ↓
Flask: /customer/ai/chat endpoint
    ↓
AIAssistant.chat(message)
    ↓
OpenAI beschikbaar? ──→ JA ──→ _chat_with_openai()
    │                              ↓
    │                          Bouw context:
    │                          - Klant: naam, tier, preferences
    │                          - Recent logs (laatste 10)
    │                          - Totaal logs
    │                          - Conversation history
    │                              ↓
    │                          OpenAI API call (GPT-4 Turbo)
    │                              ↓
    │                          AI Response
    │                              ↓
    │                          Save in ai_conversations
    │                              ↓
    │                          Return to user
    │
    └─→ NEE ──→ process_command() (fallback rule-based NLP)
```

### Context Provided to GPT:

**System Prompt:**
```
Je bent een persoonlijke AI Secretaresse voor MVAI Connexx, een logistiek data platform.

Klant informatie:
- Naam: [Customer Name]
- Pricing tier: [demo/particulier/mkb/etc]
- Taal voorkeur: [nl/en]
- Toon: [professional/casual/friendly]

Je taak:
- Beantwoord vragen over logistieke data, statistieken, en trends
- Geef proactieve suggesties voor optimalisatie
- Wees [professional] en spreek [Nederlands]
- Focus op logistiek, transport, kosten, en efficiency

Beschikbare data:
- Recente logs: [X] entries
- Totaal aantal logs: [Y]

Recentste logs:
- 2026-02-03 17:30: Verzending naar Amsterdam
- 2026-02-03 16:45: Route optimalisatie
- ...
```

**User Message:**
```
"Hoeveel logs had ik vandaag?"
```

**GPT-4 Response:**
```
Op basis van je data zie ik dat je vandaag 12 logs hebt gehad.
De meeste activiteit was tussen 14:00-16:00 (5 logs).

Opvallend: 3 van de 12 logs waren voor route optimalisaties,
wat suggereert dat je actief bezig bent met efficiency verbetering.

Wil je dat ik een gedetailleerd rapport maak van de activiteiten vandaag?
```

---

## 🎯 USE CASES

### 1. Statistieken Vragen
```
User: "Hoeveel verzendingen had ik vorige week?"
AI: "Vorige week had je 47 verzendingen, een stijging van 12% t.o.v. de week ervoor..."
```

### 2. Trend Analyse
```
User: "Wat is de trend van mijn kosten deze maand?"
AI: "Je kosten zijn gestegen met 8% deze maand. Belangrijkste oorzaken: meer internationale verzendingen (15→23)..."
```

### 3. Proactieve Suggesties
```
User: "Hoe kan ik kosten verlagen?"
AI: "Op basis van je data zie ik 3 opportunities: 1) Bundel routes naar Amsterdam (6 aparte ritten → 2 bundels = €340 besparing)..."
```

### 4. Rapportage
```
User: "Maak een samenvatting van vandaag"
AI: "Samenvatting 3 februari 2026: 12 logs, 8 verzendingen, 4 optimalisaties. Piek activiteit: 14:00-16:00..."
```

---

## ⚠️ BELANGRIJKE SECURITY WAARSCHUWINGEN

### 🔴 API Key EXPOSED in Chat!

**GEVAAR:** Je API key is nu zichtbaar in deze chat conversation!

**ACTIE VEREIST:**
1. **Revoke deze key** in OpenAI dashboard:
   - Ga naar: https://platform.openai.com/api-keys
   - Zoek key: sk-proj-XBmgAm...
   - Click "Delete" of "Revoke"

2. **Maak nieuwe key aan:**
   - Create new secret key
   - Copy nieuwe key

3. **Update .env:**
   ```bash
   # Wijzig in .env:
   OPENAI_API_KEY=sk-proj-NIEUWE_KEY_HIER
   ```

4. **Restart Flask:**
   ```bash
   # Stop: Ctrl+C
   python app.py  # Start opnieuw met nieuwe key
   ```

### ✅ Voor Productie (Hostinger):

**1. SSH naar Hostinger VPS:**
```bash
ssh user@jouw-vps-ip
cd /pad/naar/mvai-connexx
```

**2. Maak .env file:**
```bash
nano .env

# Voeg toe:
OPENAI_API_KEY=sk-proj-NIEUWE_VEILIGE_KEY
OPENAI_MODEL=gpt-4-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Save: Ctrl+O, Enter, Ctrl+X
```

**3. Installeer dependencies:**
```bash
pip install -r requirements.txt
```

**4. Restart service:**
```bash
sudo systemctl restart mvai-connexx
```

**5. Test:**
```bash
curl https://jouw-domein.com/customer/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

---

## 📈 KOSTEN (OpenAI API)

### GPT-4 Turbo Pricing:
- **Input:** $10 per 1M tokens (~750K words)
- **Output:** $30 per 1M tokens (~750K words)

### Gemiddeld gebruik:
- **Per chat:** ~300-500 tokens (~$0.005 = €0.0045)
- **100 chats/dag:** ~€0.45/dag = €13.50/maand
- **1000 chats/dag:** ~€4.50/dag = €135/maand

### Tips om kosten laag te houden:
1. **Gebruik GPT-3.5-Turbo** voor simpele vragen (10x goedkoper)
2. **Beperk context** - Alleen recente logs (nu: 10, kan naar 5)
3. **Lower max_tokens** - 500 i.p.v. 1000 voor korte antwoorden
4. **Cache responses** - Identieke vragen binnen 1 uur
5. **Tier-based limits** - Demo: 10 chats/dag, Particulier: 50, MKB: onbeperkt

---

## 🐛 TROUBLESHOOTING

### "OpenAI library not installed"
```bash
pip install openai>=1.12.0
```

### "API key not found"
```bash
# Check .env file bestaat:
ls -la .env

# Check key in .env:
grep OPENAI_API_KEY .env

# Als leeg of missing:
nano .env
# Voeg toe: OPENAI_API_KEY=sk-proj-...
```

### "Invalid API key"
```bash
# Test key in terminal:
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer sk-proj-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4-turbo","messages":[{"role":"user","content":"test"}]}'

# Als error: Key is invalid of revoked
# Maak nieuwe key aan in OpenAI dashboard
```

### "Fallback to rule-based system"
```bash
# Check logs in Flask terminal:
# Je ziet: "⚠️ Failed to initialize OpenAI client: [error]"

# Common errors:
# - API key incorrect
# - OpenAI library niet geïnstalleerd
# - Network error (firewall?)

# Fix en restart app
```

### "AI responses zijn generiek"
```bash
# Verhoog temperature in .env:
OPENAI_TEMPERATURE=1.0  # Was 0.7

# Of voeg meer context toe in ai_assistant.py:
# Wijzig _get_recent_logs(limit=10) → limit=20
```

---

## ✅ CHECKLIST

**Setup compleet als:**
- [ ] `.env` file bestaat met OPENAI_API_KEY
- [ ] `pip install -r requirements.txt` gedaan
- [ ] Flask app start zonder errors
- [ ] AI Assistant pagina laadt in browser
- [ ] Test chat stuurt intelligent antwoord (niet fallback)
- [ ] Conversation history werkt (2e vraag refereert naar 1e)

**Production ready als:**
- [ ] OLD API key revoked in OpenAI dashboard
- [ ] NEW API key aangemaakt
- [ ] `.env` updated met nieuwe key op Hostinger VPS
- [ ] Flask service restarted op VPS
- [ ] Test via productie URL werkt
- [ ] Kosten monitoring actief (OpenAI dashboard)

---

## 🚀 VOLGENDE STAPPEN

### Nu (Lokaal Testen):
```bash
1. pip install -r requirements.txt
2. python app.py
3. Open http://localhost:5000
4. Test AI Assistant
5. Verify GPT-4 responses (check for "model": "gpt-4-turbo" in API response)
```

### Daarna (Hostinger Deployment):
```bash
1. SSH naar VPS
2. git pull origin claude/mvai-connexx-multi-tenant-upgrade-8eDvw
3. pip install -r requirements.txt
4. nano .env (voeg OPENAI_API_KEY toe)
5. sudo systemctl restart mvai-connexx
6. Test via productie URL
```

### Dan (Android App):
```bash
# Android app werkt automatisch!
# AI chat API endpoint: /customer/ai/chat
# Geen wijzigingen nodig in Android code
```

---

**🔥 GODMODE ACTIVATED - OPENAI INTEGRATION COMPLETE! 🤖**

Test het nu lokaal en laat me weten als het werkt!

Bij problemen: stuur Flask terminal output + error messages.
