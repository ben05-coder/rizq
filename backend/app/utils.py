import json
import re
from typing import Dict, Any


def parse_gpt_json(response_text: str) -> Dict[str, Any]:
    """
    Extracts and parses JSON from GPT response.
    Handles markdown code blocks and other formatting issues.

    Args:
        response_text: Raw text response from GPT that should contain JSON

    Returns:
        Parsed JSON as dictionary, or empty dict if parsing fails
    """
    if not response_text:
        return {}

    # Try direct JSON parse first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    # Matches ```json ... ``` or ``` ... ```
    code_block_match = re.search(
        r'```(?:json)?\s*(\{.*?\})\s*```',
        response_text,
        re.DOTALL
    )
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1))
        except json.JSONDecodeError:
            pass

    # Fallback: find first complete JSON object {...}
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # If all parsing fails, return empty dict
    return {}


def extract_structured_digest(digest_text: str) -> Dict[str, Any]:
    """
    Extracts structured information from digest response.

    Expected format from GPT:
    {
        "summary": "...",
        "highlights": ["...", "..."],
        "insights": ["...", "..."],
        "action_items": ["...", "..."],
        "questions": ["...", "..."]
    }

    Args:
        digest_text: Raw digest text from GPT

    Returns:
        Structured digest dictionary
    """
    parsed = parse_gpt_json(digest_text)

    # Ensure all expected fields exist with defaults
    return {
        "summary": parsed.get("summary", ""),
        "highlights": parsed.get("highlights", []),
        "insights": parsed.get("insights", []),
        "action_items": parsed.get("action_items", []),
        "questions": parsed.get("questions", [])
    }


def extract_smartnotes(smartnotes_text: str) -> Dict[str, Any]:
    """
    Extracts structured smart notes from GPT response.

    Expected format:
    {
        "summary": "...",
        "structured_notes": ["...", "..."],
        "flashcards": [{"front": "...", "back": "..."}, ...],
        "quizzes": ["...", "..."],
        "eli12": "..."
    }

    Args:
        smartnotes_text: Raw smartnotes text from GPT

    Returns:
        Structured smartnotes dictionary
    """
    parsed = parse_gpt_json(smartnotes_text)

    return {
        "summary": parsed.get("summary", ""),
        "structured_notes": parsed.get("structured_notes", []),
        "flashcards": parsed.get("flashcards", []),
        "quizzes": parsed.get("quizzes", []),
        "eli12": parsed.get("eli12", "")
    }


def extract_flashcards(flashcard_text: str) -> list:
    """
    Extracts flashcards from GPT response.

    Expected format:
    {
        "flashcards": [
            {"front": "Question or term", "back": "Answer or definition"},
            ...
        ]
    }

    Args:
        flashcard_text: Raw flashcard text from GPT

    Returns:
        List of flashcard dictionaries
    """
    parsed = parse_gpt_json(flashcard_text)
    flashcards = parsed.get("flashcards", [])

    # Validate flashcard format
    valid_flashcards = []
    for card in flashcards:
        if isinstance(card, dict) and "front" in card and "back" in card:
            valid_flashcards.append({
                "front": str(card["front"]),
                "back": str(card["back"])
            })

    return valid_flashcards
