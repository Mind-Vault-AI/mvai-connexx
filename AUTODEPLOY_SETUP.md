# 🤖 AUTO-DEPLOY SETUP - Google Cloud Run

**1x instellen = ALTIJD automatisch deployen bij git push!**

---

## ⚡ WAT GEBEURT ER:

Bij elke `git push` naar deze branch:
1. GitHub Action start automatisch
2. **Controleert of GCP_SA_KEY secret is ingesteld**
3. Als secret aanwezig: Build Docker image en deploy naar Google Cloud Run
4. Als secret ontbreekt: Skip deployment met duidelijke instructies
5. LIVE URL in logs (bij succesvolle deployment)

**JIJ HOEFT NIETS TE DOEN - ALLEEN PUSHEN!**

---

## 🆕 NIEUWE FEATURE: Graceful Secret Handling

De workflow controleert nu automatisch of het `GCP_SA_KEY` secret is ingesteld:

- ✅ **Secret aanwezig**: Deployment verloopt normaal
- ⚠️ **Secret ontbreekt**: Deployment wordt overgeslagen met duidelijke instructies
- ❌ **Geen fouten meer**: De workflow faalt niet meer hard, maar toont waarschuwingen

Dit betekent dat de workflow altijd succesvol zal zijn, zelfs als de secret nog niet is ingesteld!

---

## 🔧 SETUP (5 MINUTEN):

### Stap 1: Service Account Key maken

1. Ga naar Google Cloud Console:
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts?project=mindvault-ai-com
   ```

2. **CREATE SERVICE ACCOUNT**
   - Name: `github-actions-deployer`
   - Click **CREATE AND CONTINUE**

3. **Grant permissions:**
   - Role 1: `Cloud Run Admin`
   - Role 2: `Service Account User`
   - Role 3: `Storage Object Admin` (bij voorkeur alleen op de specifieke deployment bucket)
   - Click **CONTINUE** → **DONE**

4. **Create key:**
   - Click op de nieuwe service account
   - **KEYS** tab
   - **ADD KEY** → **Create new key**
   - Type: **JSON**
   - Download de `.json` file

### Stap 2: GitHub Secret toevoegen

1. Ga naar GitHub repo:
   ```
   https://github.com/Mind-Vault-AI/mvai-connexx/settings/secrets/actions
   ```

2. **New repository secret**
   - Name: `GCP_SA_KEY`
   - Value: Plak de HELE INHOUD van de `.json` file
   - Click **Add secret**

### Stap 3: KLAAR!

**Nu bij elke `git push`:**
- GitHub Action start automatisch
- Deploy naar Cloud Run
- LIVE binnen 3-5 minuten!

**Check deployment:**
```
https://github.com/Mind-Vault-AI/mvai-connexx/actions
```

---

## 📋 WORKFLOW STATUS BEGRIJPEN

Na een push, zie je in de Actions tab:

### ✅ Scenario 1: Secret is ingesteld
```
✓ check-secrets         (✅ GCP_SA_KEY secret is configured)
✓ deploy                (🚀 DEPLOYED TO: https://...)
- deployment-skipped    (Skipped)
```

### ⚠️ Scenario 2: Secret ontbreekt
```
✓ check-secrets         (⚠️ GCP_SA_KEY secret is not set)
- deploy                (Skipped)
✓ deployment-skipped    (📖 Instructions shown)
```

Beide scenario's resulteren in een **groene workflow** - geen fouten meer!

---

## 🎯 ALTERNATIEF: Handmatige Deploy (1 commando)

Als je GitHub Actions niet wil:

```bash
# Google Cloud CLI (lokaal):
gcloud run deploy mvai-connexx \
  --source . \
  --region=europe-west1 \
  --allow-unauthenticated \
  --memory=1Gi \
  --project=mindvault-ai-com
```

---

## ✅ VERIFICATIE

Na setup, test met:

```bash
git commit --allow-empty -m "test: trigger auto-deploy"
git push
```

Check: https://github.com/Mind-Vault-AI/mvai-connexx/actions

**GROEN = LIVE!** 🚀

---

## 🔍 TROUBLESHOOTING

### Workflow toont warnings maar faalt niet
Dit is **normaal** als de GCP_SA_KEY secret nog niet is ingesteld. De workflow:
- Controleert de secret
- Toont een waarschuwing als deze ontbreekt
- Skipt de deployment
- Geeft instructies voor het instellen van de secret

Dit is **geen fout** - het is bedoeld gedrag!

### Deployment wel nodig?
Volg de setup instructies hierboven om de GCP_SA_KEY secret toe te voegen.

### Deployment NIET nodig?
Geen probleem! De workflow blijft groen en alles werkt normaal.

---

**AUTO-DEPLOY = GEEN GEDOE MEER!**
