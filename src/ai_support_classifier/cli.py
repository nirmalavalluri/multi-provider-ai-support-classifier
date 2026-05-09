from __future__ import annotations

import argparse
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .fallback import classify_with_fallback, compare_providers
from .providers import build_provider

console = Console()


def _to_json(result) -> str:
    return result.model_dump_json(indent=2)


def handle_classify(args: argparse.Namespace) -> None:
    provider = build_provider(args.provider)
    result = provider.classify(args.message)
    console.print(Panel(_to_json(result), title=f"Classification - {result.provider}"))


def handle_compare(args: argparse.Namespace) -> None:
    results = compare_providers(args.message)

    table = Table(title="Provider Comparison")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Status")
    table.add_column("Latency")
    table.add_column("Category")
    table.add_column("Urgency")

    for result in results:
        category = result.intent.category if result.intent else "-"
        urgency = result.intent.urgency if result.intent else "-"
        table.add_row(
            result.provider,
            result.model,
            result.status,
            f"{result.latency_seconds}s",
            category,
            urgency,
        )

    console.print(table)
    console.print_json(json.dumps([r.model_dump() for r in results], default=str))


def handle_fallback(args: argparse.Namespace) -> None:
    result = classify_with_fallback(args.message)
    console.print(Panel(_to_json(result), title="Fallback Result"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Multi-provider SaaS customer support AI classifier")
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify_parser = subparsers.add_parser("classify", help="Classify a customer message with one provider")
    classify_parser.add_argument("--provider", default="mock", choices=["mock", "openai", "anthropic", "claude", "gemini", "groq", "llama"])
    classify_parser.add_argument("--message", required=True)
    classify_parser.set_defaults(func=handle_classify)

    compare_parser = subparsers.add_parser("compare", help="Compare configured providers")
    compare_parser.add_argument("--message", required=True)
    compare_parser.set_defaults(func=handle_compare)

    fallback_parser = subparsers.add_parser("fallback", help="Classify using provider fallback order")
    fallback_parser.add_argument("--message", required=True)
    fallback_parser.set_defaults(func=handle_fallback)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
