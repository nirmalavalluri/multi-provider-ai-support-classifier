import json
import streamlit as st

from ai_support_classifier.fallback import classify_with_fallback, compare_providers
from ai_support_classifier.providers import build_provider

st.set_page_config(
    page_title="AI Support Ticket Classifier",
    page_icon="🎧",
    layout="wide"
)
st.title("🎧 Multi-Provider AI Support Ticket Classifier")
st.write(
    "Classify customer support tickets using mock mode or configured LLM providers."
)

sample = (
    "I canceled my Pro subscription last week, but I was charged $129.99 "
    "for an annual renewal today. Please reverse the charge and confirm my plan is canceled."
)

message = st.text_area(
    "Customer support ticket",
    value=sample,
    height=140
)

mode = st.radio(
    "Mode",
    ["Mock Provider", "Fallback", "Compare Configured Providers"],
    horizontal=True
)

if st.button("Run Classification"):
    if mode == "Mock Provider":
        result = build_provider("mock").classify(message)
        st.json(json.loads(result.model_dump_json()))

    elif mode == "Fallback":
        result = classify_with_fallback(message)
        st.json(json.loads(result.model_dump_json()))

    else:
        results = compare_providers(message)

        st.dataframe([
            {
                "provider": r.provider,
                "model": r.model,
                "status": r.status,
                "latency_seconds": r.latency_seconds,
                "category": r.intent.category if r.intent else None,
                "urgency": r.intent.urgency if r.intent else None,
                "sentiment": r.intent.sentiment if r.intent else None,
                "error": r.error,
            }
            for r in results
        ])

        st.json([json.loads(r.model_dump_json()) for r in results])