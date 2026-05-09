# Interview Notes

## 30-second explanation

I built a Multi-Provider AI Support Ticket Classifier scenarios. It compares OpenAI, Claude, Gemini, and Groq for the same customer messages, measures latency and token usage, and extracts validated structured output using Pydantic. I also implemented a fallback pattern so the system can continue if one provider fails.

## Why this is useful

In real enterprise AI systems, we should not only focus on prompt writing. We also need:

- Structured outputs
- Validation
- Provider abstraction
- Fallback and resiliency
- Latency and cost comparison
- Safe handling of sensitive customer data

## Good resume bullet

Built a Python-based multi-provider GenAI prototype for saas customer-support classification using OpenAI, Anthropic Claude, Google Gemini, Groq, and Pydantic. Implemented structured output validation, latency/token comparison, and provider fallback handling for production-style reliability.

## Possible next enhancement

Expose the classifier as a FastAPI endpoint and deploy it to Azure App Service or Azure Container Apps with Key Vault-based secret management and Application Insights telemetry.
