# 🤖 AUTO-DEPLOY SETUP - Google Cloud Run

**1x instellen = ALTIJD automatisch deployen bij git push!**

---

## ⚡ WAT GEBEURT ER:

Bij elke `git push` naar deze branch:
1. GitHub Action start automatisch
2. Build Docker image
3. Deploy naar Google Cloud Run
4. LIVE URL in logs

**JIJ HOEFT NIETS TE DOEN - ALLEEN PUSHEN!**

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
   - Role 3: `Storage Admin`
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

**AUTO-DEPLOY = GEEN GEDOE MEER!**
