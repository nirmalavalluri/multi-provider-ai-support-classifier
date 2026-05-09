# Architecture Notes

## Goal

Build a small but realistic GenAI prototype for saas customer support classification.

## Main components

1. **Customer message input**
   - Text message from chatbot, email, or support form.

2. **Provider layer**
   - OpenAI
   - Anthropic Claude
   - Google Gemini
   - Groq / Llama
   - Mock provider for demos and tests

3. **Classification schema**
   - `category`
   - `urgency`
   - `sentiment`
   - `entities`
   - `summary`
   - `recommended_action`

4. **Validation layer**
   - Pydantic validates model output before the result is used by downstream systems.

5. **Fallback layer**
   - Tries providers in sequence.
   - Returns the first valid structured result.
   - Captures provider failures for troubleshooting.

## Production improvements to add later

- Logging and tracing with OpenTelemetry
- Centralized prompt versioning
- PII redaction before sending messages to LLMs
- Evaluation dataset with expected labels
- Cost tracking per provider
- Azure Key Vault or managed identity for secrets
- API wrapper using FastAPI
- Dockerfile and CI/CD pipeline
