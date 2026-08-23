from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from pprint import pprint
from typing import Any

from dotenv import load_dotenv

try:
    from google import genai
except Exception as import_exc:  # pragma: no cover
    genai = None
    _GENAI_IMPORT_ERROR = import_exc
else:
    _GENAI_IMPORT_ERROR = None


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
FALLBACK_MODELS = ["gemini-3.6-flash", "gemini-2.5-flash"]

GENAI_CLIENT = genai.Client(api_key=GEMINI_API_KEY) if genai is not None and GEMINI_API_KEY else None


def _build_investigation_prompt(blind_spot: dict[str, Any]) -> str:
    return f"""
You are a cautious government data analyst.

You must return ONLY valid JSON with no markdown code fences and no preamble text.
Return this exact JSON structure and key names:
{{
  "hypotheses": [
    {{"text": "...", "confidence_pct": 0-100, "label": "HYPOTHESIS - NOT CONFIRMED"}}
  ],
  "evidence_gaps": ["...", "...", "..."],
  "investigation_brief": {{
    "problem": "...",
    "observed_contradiction": "...",
    "evidence": "...",
    "uncertainty": "...",
    "affected_groups": "...",
    "additional_evidence_required": "...",
    "recommended_steps": "..."
  }}
}}

Requirements:
1) Generate exactly 3 hypotheses ranked by plausibility.
2) Every hypothesis must include a confidence_pct that reflects genuine uncertainty.
3) No confidence_pct may exceed 75.
4) Never state hypotheses as confirmed facts. Use hedged language such as "possible", "may indicate", and "could suggest".
5) Include at least 3 concrete evidence gaps that name specific missing data types.
6) Keep each investigation_brief field concise: 1-3 sentences.
7) Base everything strictly on the department name and numeric indicators below.
8) Do not invent additional statistics.
9) Do not claim knowledge of real events.

Input blind spot data:
{json.dumps(blind_spot, ensure_ascii=True, indent=2)}
""".strip()


def _strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def generate_investigation(blind_spot: dict[str, Any]) -> dict[str, Any]:
    if genai is None:
        return {
            "error": f"google.genai import failed: {_GENAI_IMPORT_ERROR}",
        }

    if not GEMINI_API_KEY:
        return {
            "error": "GEMINI_API_KEY is not set in environment variables.",
        }

    if GENAI_CLIENT is None:
        return {
            "error": "Unable to initialize google.genai client.",
        }

    prompt = _build_investigation_prompt(blind_spot)
    raw_text = ""

    last_error = None

    model_candidates = [PRIMARY_MODEL, *FALLBACK_MODELS]
    seen = set()

    for model_name in model_candidates:
        if not model_name:
            continue
        if model_name in seen:
            continue
        seen.add(model_name)
        try:
            chat = GENAI_CLIENT.chats.create(model=model_name)
            response = chat.send_message(prompt)
            raw_text = getattr(response, "text", "") or ""
            cleaned_text = _strip_markdown_fences(raw_text)
            return json.loads(cleaned_text)
        except json.JSONDecodeError as exc:
            print("Failed to parse Gemini JSON response.")
            print("Raw response:")
            print(raw_text)
            return {"error": f"Failed to parse JSON response: {exc}"}
        except Exception as exc:
            last_error = exc
            error_text = str(exc).lower()
            if "401" in error_text or "unauthenticated" in error_text or "access_token_type_unsupported" in error_text:
                return {
                    "error": (
                        "Gemini authentication failed. GEMINI_API_KEY must be a valid "
                        "Google AI Studio API key, not an OAuth access token."
                    )
                }
            # If the model is unavailable, try the next candidate.
            if "not found" in error_text or "no longer available" in error_text or "404" in error_text:
                continue
            return {"error": f"Gemini request failed: {exc}"}

    return {
        "error": (
            "Gemini request failed for all model candidates "
            f"{model_candidates}: {last_error}"
        )
    }


if __name__ == "__main__":
    backend_root = Path(__file__).resolve().parents[2]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    from app.services.blind_spot_detector import get_all_blind_spots

    all_blind_spots = get_all_blind_spots()

    if not all_blind_spots:
        print("No blind spots found.")
    else:
        top_blind_spot = all_blind_spots[0]
        investigation = generate_investigation(top_blind_spot)
        pprint(investigation, sort_dicts=False)
