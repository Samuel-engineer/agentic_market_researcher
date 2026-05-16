# Troubleshooting — Connexion Azure AI Foundry avec CrewAI 1.14.4

## Résumé des problèmes rencontrés et solutions appliquées

---

## Problème 1 — `DeploymentNotFound`

**Erreur :**
```
(DeploymentNotFound) The API deployment for this resource does not exist.
```

**Cause :**  
Le nom de déploiement dans `agents.py` était `gpt-4o`, mais le déploiement réel sur la ressource Azure s'appelait `OpenAICreate-20260516160352`. Le nom de déploiement doit correspondre **exactement** à ce qui est visible dans Azure Portal > Azure OpenAI > Deployments.

**Tentative de correction :**  
```python
# AVANT (incorrect)
model="azure/gpt-4o"

# APRÈS (corrigé pour l'ancienne ressource)
model="azure/OpenAICreate-20260516160352"
```

> Cette ressource (`worspace11.openai.azure.com`) a été abandonnée au profit d'Azure AI Foundry.

---

## Problème 2 — `404 Resource not found` (ancienne ressource)

**Erreur :**
```
Azure endpoint not found. Check endpoint URL: https://worspace11.openai.azure.com/
```

**Cause :**  
L'endpoint `worspace11.openai.azure.com` était injoignable (ressource supprimée ou mal orthographiée). Décision de migrer vers Azure AI Foundry (`services.ai.azure.com`).

---

## Problème 3 — `404 Resource not found` (Foundry, cognitiveservices)

**Erreur :**
```
(404) Resource not found
```

**Endpoint testé :**
```
https://toaly-mp8hfk4v-swedencentral.cognitiveservices.azure.com/
```

**Cause :**  
L'endpoint `cognitiveservices.azure.com` sans le chemin de déploiement complet est rejeté par le SDK `azure.ai.inference` utilisé nativement par CrewAI 1.14.4. La correction était d'ajouter le chemin complet :
```
https://toaly-mp8hfk4v-swedencentral.cognitiveservices.azure.com/openai/deployments/gpt-4o
```
Mais cela a conduit au problème suivant.

---

## Problème 4 — `(BadRequest) API version not supported` ← Problème principal

**Erreur :**
```
(BadRequest) API version not supported
Code: BadRequest
Message: API version not supported
```

**Cause (root cause) :**  
CrewAI **1.14.4** n'utilise **plus LiteLLM** pour Azure. Il a son propre provider Azure (`crewai/llms/providers/azure/completion.py`) qui instancie directement le SDK `azure.ai.inference.ChatCompletionsClient`.

Ce SDK injecte **automatiquement** un header `api-version` dans chaque requête (par exemple `2024-06-01`). Or, le endpoint Azure AI Foundry sur le path `/openai/v1/` (format OpenAI-compatible) **ne supporte pas le paramètre `api-version`** — il utilise la versioning implicite via le path `/v1/`.

Versions testées, toutes rejetées :
- `api_version="2025-01-01-preview"` → `BadRequest`
- `api_version="2024-05-01-preview"` → `BadRequest`
- SDK `azure.ai.inference` sans version explicite → `BadRequest` (le SDK injecte quand même sa valeur par défaut)

**Ce qui a été testé et échoué :**
```python
# Toutes ces configurations échouent car azure.ai.inference injecte toujours api-version
endpoints_fail = [
    "https://toaly-mp8hfk4v-swedencentral.services.ai.azure.com/api/projects/Agent",
    "https://toaly-mp8hfk4v-swedencentral.services.ai.azure.com",
    "https://toaly-mp8hfk4v-swedencentral.services.ai.azure.com/api/projects/Agent/openai/deployments/gpt-4o",
]
```

---

## Solution finale ✅

**Principe :** Contourner le provider Azure natif de CrewAI en utilisant le provider `openai/` (LiteLLM + SDK `openai` standard), qui envoie les requêtes sans `api-version` — compatible avec le endpoint Foundry `/openai/v1`.

### Configuration `src/agents.py`

```python
azure_llm = LLM(
    model="openai/gpt-4o",        # Provider OpenAI (pas "azure/"), utilise le SDK openai standard
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_ENDPOINT")  # Foundry endpoint /openai/v1
    # Pas d'api_version : non requis sur /openai/v1
)
```

### Configuration `.env`

```env
AZURE_API_KEY=<clé de la ressource Foundry>
AZURE_ENDPOINT=https://toaly-mp8hfk4v-swedencentral.services.ai.azure.com/api/projects/Agent/openai/v1
```

### Pourquoi ça fonctionne

| Provider CrewAI | SDK sous-jacent | Envoie `api-version` ? | Compatible Foundry `/openai/v1` |
|---|---|---|---|
| `azure/gpt-4o` | `azure.ai.inference` | ✅ Oui (toujours) | ❌ Non |
| `openai/gpt-4o` + `base_url` | `openai` (LiteLLM) | ❌ Non | ✅ Oui |

---

## Référence des endpoints Azure AI Foundry

| Usage | Format endpoint |
|---|---|
| OpenAI v1 (chat, embeddings) | `https://<resource>.services.ai.azure.com/api/projects/<project>/openai/v1` |
| Responses API | `https://<resource>.services.ai.azure.com/api/projects/<project>/openai/v1/responses` |
| Chat completions direct | `https://<resource>.services.ai.azure.com/api/projects/<project>/openai/v1/chat/completions` |

---

## Versions des packages au moment de la résolution

| Package | Version |
|---|---|
| `crewai` | 1.14.4 |
| `crewai-tools` | 1.14.4 |
| Python | 3.13 |
