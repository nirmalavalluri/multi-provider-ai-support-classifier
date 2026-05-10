# Multi-Provider AI Support Ticket Classifier

A portfolio GenAI project that classifies SaaS customer support tickets using multiple LLM providers — built by a .NET developer learning Agentic AI.

Compares **OpenAI**, **Anthropic Claude**, **Google Gemini**, and **Groq / Llama** on the same SaaS support scenario using Pydantic structured outputs, latency tracking, and a production-style provider fallback pattern.

---

## The .NET Developer Perspective

Coming from an ASP.NET / C# background, every concept in this project maps directly to something I already knew:

| .NET / C# Concept | This Project's Equivalent |
|---|---|
| Strongly-typed C# DTO | `SupportTicketIntent` Pydantic model |
| JSON deserialization to typed object | `responses.parse()` with schema validation |
| Polly retry / fallback policy | Multi-provider fallback chain |
| `IHttpClientFactory` with named clients | OpenAI, Anthropic, Gemini, Groq SDK instances |
| `appsettings.json` + Azure Key Vault | `.env` + `python-dotenv` |
| Middleware / request pipeline | System prompt (LLM behaviour control) |
| Strategy pattern | `PROVIDER_MAP` — each provider is a swappable strategy |

**The syntax changed. The engineering mindset did not.**

> Currently learning Agentic AI through K21 Academy's program with Atul Sharma.
> Each lab I take the concepts and build my own original project in a different domain to reinforce the learning.

---

## Business Scenario

**NexaCloud SaaS** receives thousands of customer support tickets daily through its helpdesk portal. Before routing each ticket to the right team, the system must understand:

- What is the customer's issue? *(billing / technical / account / feature_request / integration)*
- How urgent is it?
- What is the customer's sentiment?
- Which team should handle it?
- What should the support agent do first?

### Example Input

```
I upgraded to the Business plan last Tuesday and my team still cannot
access the advanced analytics dashboard. We have a client presentation
tomorrow and this is blocking us completely. Please escalate this now.
```

### Example Output

```json
{
  "category": "technical",
  "urgency": "critical",
  "sentiment": "frustrated",
  "team": "technical_support",
  "entities": ["Business plan", "last Tuesday", "advanced analytics dashboard", "client presentation"],
  "summary": "Customer upgraded to Business plan but team cannot access advanced analytics, blocking a client presentation.",
  "recommended_action": "Escalate to senior technical support immediately; verify plan entitlements and provision analytics access within 2 hours."
}
```

---

## Sample Support Tickets

Five original synthetic SaaS support scenarios used in this project:

| # | Scenario | Category | Urgency |
|---|---|---|---|
| 1 | Team cannot access analytics after plan upgrade | technical | critical |
| 2 | Charged after cancelling subscription | billing | high |
| 3 | Zapier integration stops syncing data | integration | high |
| 4 | API rate limit too low for enterprise usage | feature_request | medium |
| 5 | How to export data before subscription ends | account | low |

---

## Architecture

```
Support Ticket
      │
      ▼
 Provider Router
 ┌──────────────────────────────────────────────┐
 │  OpenAI → Anthropic → Gemini → Groq          │  ← Fallback chain (like Polly in .NET)
 └──────────────────────────────────────────────┘
      │
      ▼
 Pydantic Validation  ← Like C# DTO deserialization
      │
      ▼
 SupportTicketIntent (structured result)
      │
      ▼
 Routing / Helpdesk / CRM
```

---

## Project Structure

```
multi-provider-ai-support-classifier/
├── src/
│   └── ai_support_classifier/
│       ├── schemas.py        # SupportTicketIntent Pydantic model
│       ├── providers.py      # OpenAI, Anthropic, Gemini, Groq implementations
│       ├── fallback.py       # Multi-provider fallback chain
│       ├── mock_provider.py  # Demo without API keys
│       ├── prompts.py        # Prompt templates
│       ├── json_utils.py     # JSON sanitization helpers
│       ├── config.py         # API key configuration
│       └── cli.py            # Command-line interface
├── examples/
│   └── sample_messages.json  # 5 original synthetic SaaS support tickets
├── tests/
│   ├── test_schemas.py
│   └── test_json_utils.py
├── docs/
│   ├── architecture.md
│   └── interview_notes.md
├── .env.example
├── requirements.txt
└── pyproject.toml
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/nirmalavalluri/multi-provider-ai-support-classifier.git
cd multi-provider-ai-support-classifier
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Add your keys to `.env`:

```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
```

Never commit `.env` to GitHub.

---

## Run the Project

### Demo mode — no API keys needed

```bash
python -m ai_support_classifier.cli demo
```

### Classify a single ticket

```bash
python -m ai_support_classifier.cli classify \
  --provider mock \
  --message "My Zapier integration stopped syncing data three days ago and I have lost all my workflow automations."
```

### Compare all configured providers

```bash
python -m ai_support_classifier.cli compare \
  --message "I was charged $299 after cancelling my subscription last month. Please refund immediately."
```

### Run the fallback chain

```bash
python -m ai_support_classifier.cli fallback \
  --message "Our entire team has been locked out of the platform since this morning. We cannot work at all."
```

---

## Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Multi-provider LLM comparison | OpenAI, Anthropic Claude, Google Gemini, Groq / Llama |
| Native structured output | OpenAI `responses.parse()` with Pydantic |
| Prompt-based structured output | Anthropic JSON extraction + Pydantic validation |
| Schema-based structured output | Gemini `response_schema` |
| Provider fallback pattern | `fallback.py` — mirrors Polly in .NET |
| Schema validation | Pydantic `SupportTicketIntent` model |
| Secure key management | `python-dotenv` — mirrors Azure Key Vault pattern |
| Mock provider | Demo without API keys — CI/CD friendly |

---

## Interview Talking Points

> I built a multi-provider AI support ticket classifier for a SaaS helpdesk scenario. The system compares OpenAI, Anthropic Claude, Google Gemini, and Groq for the same customer tickets, measures latency and token usage, and returns schema-validated structured outputs using Pydantic. I implemented a provider fallback chain — similar to the Polly resilience pattern I used in my .NET APIs — so the system stays resilient if a provider fails. As a .NET developer, the engineering patterns were identical across both worlds; only the language and SDKs changed.

---

## Notes

- This is a learning and portfolio project — not a production SaaS system.
- All support tickets are synthetic and contain no real customer data.
- Do not send real customer PII, account credentials, or payment details to external LLM APIs.
- Model names and SDK APIs evolve — keep model names configurable via `.env`.

---

## License

MIT License
