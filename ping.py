#!/usr/bin/env python3
"""
Ping a list of Gemini models and report availability / latency / short reply.
Requires: pip install google-genai
Set your key: export GEMINI_API_KEY="your-key"   (or GOOGLE_API_KEY)
"""

import os
import time
from typing import List, Dict, Any

import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Machine-callable model names from earlier discussion
MODELS: List[str] = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-3-flash-preview"
]

PING_PROMPT = """
Respond with exactly the single word. 
The word must be: pong
Do not add any other text, explanation, or punctuation.
"""


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
        )
    return genai.Client(api_key=api_key)


def ping_model(client: genai.Client, model: str) -> Dict[str, Any]:
    start = time.perf_counter()

    try:
        # Use Chat instead of models.generate_content().
        # This is the recommended API when AFC is involved.
        chat = client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                max_output_tokens=16,
                temperature=0.0,
            ),
        )

        response = chat.send_message(PING_PROMPT)

        latency_ms = (time.perf_counter() - start) * 1000
        text = (response.text or "").strip()

        return {
            "model": model,
            "status": "OK",
            "latency_ms": round(latency_ms, 1),
            "reply": text[:80] + ("…" if len(text) > 80 else ""),
            "error": None,
        }

    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000

        return {
            "model": model,
            "status": "FAIL",
            "latency_ms": round(latency_ms, 1),
            "reply": None,
            "error": str(e)[:200],
        }

def main() -> None:
    print("Gemini model ping report")
    print("=" * 70)

    client = get_client()
    results = []

    for model in MODELS:
        print(f"Pinging {model} …", end=" ", flush=True)
        result = ping_model(client, model)
        results.append(result)

        if result["status"] == "OK":
            print(f"OK  ({result['latency_ms']} ms)  →  {result['reply']!r}")
        else:
            print(f"FAIL ({result['latency_ms']} ms)")
            # print(f"      {result['error']}")

    print("\n" + "=" * 70)
    print("Summary")
    print("-" * 70)
    ok = sum(1 for r in results if r["status"] == "OK")
    fail = len(results) - ok
    print(f"Total: {len(results)}   OK: {ok}   FAIL: {fail}")

    if fail:
        print("\nFailed models:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  • {r['model']}")
                print(f"    {r['error']}")


if __name__ == "__main__":
    main()