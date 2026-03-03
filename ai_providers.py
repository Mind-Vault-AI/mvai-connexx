"""
MVAI Connexx - Multi-AI Provider Abstraction Layer
Ondersteunt: OpenAI (GPT-4), Claude (Anthropic), Gemini (Google), Cohere
Elke klant kan zijn eigen API key gebruiken (BYOK - Bring Your Own Key)
"""
import base64
import hashlib
import requests
from cryptography.fernet import Fernet

import database as db
import config

# ── Optional library imports (graceful degradation) ─────────────────────
try:
    from openai import OpenAI
    OPENAI_LIB = True
except ImportError:
    OPENAI_LIB = False

try:
    import anthropic
    ANTHROPIC_LIB = True
except ImportError:
    ANTHROPIC_LIB = False

# ── Provider catalog ─────────────────────────────────────────────────────
PROVIDERS = {
    'openai': {
        'name': 'OpenAI (GPT-4)',
        'icon': '🤖',
        'models': ['gpt-4-turbo', 'gpt-4o', 'gpt-4', 'gpt-3.5-turbo'],
        'default_model': 'gpt-4-turbo',
        'api_key_label': 'OpenAI API Key',
        'api_key_placeholder': 'sk-...',
        'badge_color': '#10a37f',
    },
    'anthropic': {
        'name': 'Claude (Anthropic)',
        'icon': '🧠',
        'models': ['claude-opus-4-6', 'claude-sonnet-4-6', 'claude-haiku-4-5-20251001'],
        'default_model': 'claude-sonnet-4-6',
        'api_key_label': 'Anthropic API Key',
        'api_key_placeholder': 'sk-ant-...',
        'badge_color': '#d97706',
    },
    'gemini': {
        'name': 'Gemini (Google)',
        'icon': '✨',
        'models': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro'],
        'default_model': 'gemini-1.5-flash',
        'api_key_label': 'Google AI API Key',
        'api_key_placeholder': 'AIza...',
        'badge_color': '#4285f4',
    },
    'cohere': {
        'name': 'Cohere (Command R+)',
        'icon': '🌐',
        'models': ['command-r-plus', 'command-r', 'command'],
        'default_model': 'command-r',
        'api_key_label': 'Cohere API Key',
        'api_key_placeholder': '...',
        'badge_color': '#39594d',
    },
}


# ── Encryption helpers ────────────────────────────────────────────────────
def _get_fernet() -> Fernet:
    """Maak Fernet cipher van SECRET_KEY (SHA-256 → 32 bytes → base64url)"""
    secret = config.Config.SECRET_KEY.encode()
    key = base64.urlsafe_b64encode(hashlib.sha256(secret).digest())
    return Fernet(key)


def encrypt_api_key(plaintext: str) -> str:
    return _get_fernet().encrypt(plaintext.encode()).decode()


def decrypt_api_key(ciphertext: str) -> str:
    return _get_fernet().decrypt(ciphertext.encode()).decode()


# ── Base provider class ───────────────────────────────────────────────────
class BaseProvider:
    provider_name: str = 'base'

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def chat(self, system_prompt: str, messages: list, max_tokens: int = 1000) -> dict:
        raise NotImplementedError

    def test_connection(self) -> dict:
        """Test of de API key werkt met een minimaal verzoek"""
        try:
            result = self.chat(
                "Je bent een test assistent. Antwoord heel kort.",
                [{"role": "user", "content": "Zeg alleen het woord OK."}],
                max_tokens=10
            )
            return {"success": True, "message": f"Verbinding succesvol via {self.provider_name}"}
        except Exception as e:
            return {"success": False, "message": str(e)}


# ── OpenAI provider ───────────────────────────────────────────────────────
class OpenAIProvider(BaseProvider):
    provider_name = 'openai'

    def __init__(self, api_key: str, model: str = 'gpt-4-turbo'):
        super().__init__(api_key, model)
        if not OPENAI_LIB:
            raise ImportError("openai package niet geïnstalleerd")
        self.client = OpenAI(api_key=api_key)

    def chat(self, system_prompt: str, messages: list, max_tokens: int = 1000) -> dict:
        api_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            api_messages.append({"role": msg["role"], "content": msg["content"]})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            max_tokens=max_tokens,
            temperature=0.7
        )

        return {
            'success': True,
            'message': response.choices[0].message.content,
            'model': self.model,
            'provider': 'openai',
            'tokens_used': response.usage.total_tokens if response.usage else 0
        }


# ── Anthropic / Claude provider ───────────────────────────────────────────
class AnthropicProvider(BaseProvider):
    provider_name = 'anthropic'

    def __init__(self, api_key: str, model: str = 'claude-sonnet-4-6'):
        super().__init__(api_key, model)
        if not ANTHROPIC_LIB:
            raise ImportError("anthropic package niet geïnstalleerd")
        self.client = anthropic.Anthropic(api_key=api_key)

    def chat(self, system_prompt: str, messages: list, max_tokens: int = 1000) -> dict:
        api_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]

        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=api_messages,
            max_tokens=max_tokens,
        )

        return {
            'success': True,
            'message': response.content[0].text,
            'model': self.model,
            'provider': 'anthropic',
            'tokens_used': response.usage.input_tokens + response.usage.output_tokens
        }


# ── Google Gemini provider (REST) ─────────────────────────────────────────
class GeminiProvider(BaseProvider):
    provider_name = 'gemini'
    BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models'

    def __init__(self, api_key: str, model: str = 'gemini-1.5-flash'):
        super().__init__(api_key, model)

    def chat(self, system_prompt: str, messages: list, max_tokens: int = 1000) -> dict:
        contents = []

        # Gemini system instruction via dedicated field
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.7,
            }
        }

        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            payload["contents"].append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        url = f"{self.BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        text = data['candidates'][0]['content']['parts'][0]['text']
        tokens = data.get('usageMetadata', {}).get('totalTokenCount', 0)

        return {
            'success': True,
            'message': text,
            'model': self.model,
            'provider': 'gemini',
            'tokens_used': tokens
        }


# ── Cohere provider (REST v2) ─────────────────────────────────────────────
class CohereProvider(BaseProvider):
    provider_name = 'cohere'
    BASE_URL = 'https://api.cohere.ai/v2/chat'

    def __init__(self, api_key: str, model: str = 'command-r'):
        super().__init__(api_key, model)

    def chat(self, system_prompt: str, messages: list, max_tokens: int = 1000) -> dict:
        api_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            api_messages.append({"role": msg["role"], "content": msg["content"]})

        payload = {
            "model": self.model,
            "messages": api_messages,
            "max_tokens": max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        text = data['message']['content'][0]['text']
        usage = data.get('usage', {}).get('tokens', {})
        tokens = usage.get('input_tokens', 0) + usage.get('output_tokens', 0)

        return {
            'success': True,
            'message': text,
            'model': self.model,
            'provider': 'cohere',
            'tokens_used': tokens
        }


# ── Provider factory ──────────────────────────────────────────────────────
def _build_provider(provider_name: str, api_key: str, model: str) -> BaseProvider:
    """Maak een provider object op basis van naam"""
    builders = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'gemini': GeminiProvider,
        'cohere': CohereProvider,
    }
    cls = builders.get(provider_name)
    if not cls:
        raise ValueError(f"Onbekende provider: {provider_name}")
    return cls(api_key, model)


def _get_platform_provider() -> BaseProvider | None:
    """
    Gebruik platform-brede API keys als beschikbaar.
    Prioriteit: OpenAI → Anthropic → Gemini → None
    """
    cfg = config.Config

    if getattr(cfg, 'OPENAI_API_KEY', ''):
        return OpenAIProvider(cfg.OPENAI_API_KEY, cfg.OPENAI_MODEL)

    if getattr(cfg, 'ANTHROPIC_API_KEY', ''):
        return AnthropicProvider(cfg.ANTHROPIC_API_KEY)

    if getattr(cfg, 'GEMINI_API_KEY', ''):
        return GeminiProvider(cfg.GEMINI_API_KEY)

    return None


def get_provider_for_customer(customer_id: int) -> BaseProvider | None:
    """
    Haal de AI provider op voor een specifieke klant.
    Volgorde van prioriteit:
    1. Klant eigen API key (BYOK)
    2. Platform-brede keys uit config
    3. None → valt terug op rule-based systeem in ai_assistant.py
    """
    customer_config = get_customer_provider_config(customer_id)

    if customer_config:
        provider_name = customer_config.get('provider', 'openai')
        default_model = PROVIDERS.get(provider_name, {}).get('default_model', '')
        model = customer_config.get('model') or default_model

        encrypted_key = customer_config.get('api_key_encrypted')
        if encrypted_key:
            try:
                api_key = decrypt_api_key(encrypted_key)
                return _build_provider(provider_name, api_key, model)
            except Exception as e:
                print(f"⚠️ Kon klant API key niet ontsleutelen: {e}")

    return _get_platform_provider()


# ── Database operations ───────────────────────────────────────────────────
def get_customer_provider_config(customer_id: int) -> dict | None:
    """Haal AI provider configuratie op voor klant"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM customer_ai_providers WHERE customer_id = ?',
            (customer_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def save_customer_provider_config(
    customer_id: int,
    provider: str,
    model: str,
    api_key: str | None = None
) -> bool:
    """Sla AI provider configuratie op voor klant (upsert)"""
    if provider not in PROVIDERS:
        raise ValueError(f"Onbekende provider: {provider}")

    encrypted_key = encrypt_api_key(api_key) if api_key and api_key.strip() else None

    with db.get_db() as conn:
        cursor = conn.cursor()
        existing = get_customer_provider_config(customer_id)

        if existing:
            if encrypted_key:
                cursor.execute('''
                    UPDATE customer_ai_providers
                    SET provider = ?, model = ?, api_key_encrypted = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE customer_id = ?
                ''', (provider, model, encrypted_key, customer_id))
            else:
                # Bewaar bestaande key als geen nieuwe is opgegeven
                cursor.execute('''
                    UPDATE customer_ai_providers
                    SET provider = ?, model = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE customer_id = ?
                ''', (provider, model, customer_id))
        else:
            cursor.execute('''
                INSERT INTO customer_ai_providers
                    (customer_id, provider, model, api_key_encrypted)
                VALUES (?, ?, ?, ?)
            ''', (customer_id, provider, model, encrypted_key))

    return True


def delete_customer_api_key(customer_id: int) -> bool:
    """Verwijder API key van klant (privacy/veiligheid)"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customer_ai_providers
            SET api_key_encrypted = NULL, updated_at = CURRENT_TIMESTAMP
            WHERE customer_id = ?
        ''', (customer_id,))
    return True


def test_provider_config(provider: str, api_key: str, model: str) -> dict:
    """Test of een provider + API key combinatie werkt"""
    if provider not in PROVIDERS:
        return {"success": False, "message": f"Onbekende provider: {provider}"}

    if not model:
        model = PROVIDERS[provider]['default_model']

    try:
        p = _build_provider(provider, api_key, model)
        return p.test_connection()
    except ImportError as e:
        return {"success": False, "message": f"Library niet beschikbaar: {e}"}
    except Exception as e:
        return {"success": False, "message": str(e)}
