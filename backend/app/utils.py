import json
import re
from typing import Dict, Any, List


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


def remove_repetitive_endings(text: str, min_repetitions: int = 2) -> str:
    """
    Removes repetitive phrases from the end of text.

    Whisper sometimes hallucinates and repeats the same phrase at the end
    of transcriptions. This function detects and removes such repetitions.

    Args:
        text: The transcript text to clean
        min_repetitions: Minimum number of repetitions to trigger removal (default: 2)

    Returns:
        Cleaned text with repetitive endings removed
    """
    if not text or len(text) < 50:
        return text

    # Method 1: Check for exact substring repetition at the end
    # This catches fragments that repeat exactly, even without sentence boundaries
    text_length = len(text)
    min_pattern_length = 20  # Minimum characters for a repeating pattern
    max_pattern_length = min(500, text_length // 3)  # Check up to 500 chars or 1/3 of text

    # Look for repeating patterns at the very end
    for pattern_length in range(min_pattern_length, max_pattern_length):
        # Get the pattern from the end
        pattern = text[-pattern_length:]

        # Count consecutive repetitions working backwards
        repetition_count = 1
        check_pos = text_length - pattern_length

        while check_pos >= pattern_length:
            prev_segment = text[check_pos - pattern_length:check_pos]
            if prev_segment == pattern:
                repetition_count += 1
                check_pos -= pattern_length
            else:
                break

        # If we found repetitions, remove all but one
        if repetition_count >= min_repetitions:
            # Keep text up to the start of repetitions, plus one instance of the pattern
            cutoff = check_pos + pattern_length
            cleaned_text = text[:cutoff]

            # Clean up: if we cut mid-sentence, try to end at a sentence boundary
            last_period = cleaned_text.rfind('.')
            last_question = cleaned_text.rfind('?')
            last_exclaim = cleaned_text.rfind('!')
            last_sentence_end = max(last_period, last_question, last_exclaim)

            if last_sentence_end > len(cleaned_text) - 100:  # If sentence end is near the end
                cleaned_text = cleaned_text[:last_sentence_end + 1]

            print(f"Removed {repetition_count - 1} repetitions of {pattern_length}-char pattern at end", flush=True)
            return cleaned_text.strip()

    # Method 2: Check sentence-level repetition (original logic, for different patterns)
    sentences = re.split(r'[.!?]+\s+', text)

    if len(sentences) < 3:
        return text

    # Check the last few sentences for repetition
    check_range = min(15, len(sentences))  # Increased from 10 to 15
    last_sentences = sentences[-check_range:]

    # Find repeating sentence patterns
    for pattern_length in range(1, len(last_sentences) // 2 + 1):
        pattern = tuple(last_sentences[-pattern_length:])

        # Count how many times this pattern appears at the end
        repetition_count = 1
        pos = len(last_sentences) - pattern_length

        while pos >= pattern_length:
            prev_pattern = tuple(last_sentences[pos - pattern_length:pos])
            if prev_pattern == pattern:
                repetition_count += 1
                pos -= pattern_length
            else:
                break

        # If we found enough repetitions, remove them
        if repetition_count >= min_repetitions:
            keep_sentences = sentences[:-check_range] + last_sentences[:pos + pattern_length]
            cleaned_text = '. '.join(s for s in keep_sentences if s.strip())

            if cleaned_text and not cleaned_text.endswith('.'):
                cleaned_text += '.'

            print(f"Removed {repetition_count - 1} sentence repetitions at end of transcript", flush=True)
            return cleaned_text

    # No repetitions found
    return text


def remove_hallucinations(text: str) -> str:
    """
    Removes common Whisper hallucinations from transcripts.

    Whisper sometimes hallucinates when encountering silence or noise:
    - Number counting sequences (1, 2, 3... or "one, two, three...")
    - Common YouTube phrases ("Thank you for watching", "Please subscribe")
    - Repeated "okay", "yeah", "um" sequences

    Args:
        text: The transcript text to clean

    Returns:
        Cleaned text with hallucinations removed
    """
    if not text or len(text) < 20:
        return text

    original_length = len(text)

    # Pattern 1: Remove long counting sequences (numeric)
    # Matches: "1, 2, 3, 4, 5..." or "1 2 3 4 5..." up to 100
    counting_pattern = r'\b(?:(?:\d+[,\s]*){10,})\b'
    text = re.sub(counting_pattern, '', text)

    # Pattern 1b: Remove word/phrase repetitions (like "Long March. Long March. Long March...")
    # This catches the actual issue in the transcript
    # Look for the same 1-5 word phrase repeated 5+ times
    words = text.split()
    if len(words) > 20:
        # Check last 200 words for repetitive patterns
        check_section = words[-200:]

        # Try different pattern lengths (1-5 words)
        for pattern_length in range(1, 6):
            if pattern_length > len(check_section):
                break

            # Get the pattern from the very end
            pattern = ' '.join(check_section[-pattern_length:])

            # Count how many times this exact pattern appears consecutively at the end
            repetitions = 0
            pos = len(check_section) - pattern_length

            while pos >= pattern_length:
                candidate = ' '.join(check_section[pos - pattern_length:pos])
                if candidate.lower() == pattern.lower():
                    repetitions += 1
                    pos -= pattern_length
                else:
                    break

            # If found 5+ repetitions, remove them
            if repetitions >= 4:  # Pattern appears 5+ times total (4 extra + 1 original)
                # Keep everything before the repetitions
                keep_words = words[:-200] + check_section[:pos + pattern_length]
                text = ' '.join(keep_words)
                print(f"Removed {repetitions} repetitions of phrase: '{pattern}'", flush=True)
                break

    # Pattern 2: Remove spelled-out counting
    # Matches: "one, two, three, four, five..."
    word_numbers = r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten)(?:[,\s]+(?:one|two|three|four|five|six|seven|eight|nine|ten)){5,}\b'
    text = re.sub(word_numbers, '', text, flags=re.IGNORECASE)

    # Pattern 3: Remove common YouTube hallucinations
    youtube_phrases = [
        r'thank you for watching',
        r'please subscribe',
        r'don\'t forget to like',
        r'hit the bell icon',
        r'check out my other videos'
    ]
    for phrase in youtube_phrases:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)

    # Pattern 4: Remove excessive filler word sequences at the end
    # If the last 100 chars are mostly "okay yeah um right", remove them
    if len(text) > 100:
        last_section = text[-100:]
        filler_words = ['okay', 'yeah', 'um', 'uh', 'right', 'so']
        word_count = len(last_section.split())
        filler_count = sum(1 for word in last_section.lower().split() if word.strip('.,!?') in filler_words)

        # If more than 70% filler words, likely hallucination
        if word_count > 0 and (filler_count / word_count) > 0.7:
            # Find the last sentence boundary before the filler section
            text = text[:-100]
            last_period = text.rfind('.')
            last_question = text.rfind('?')
            last_exclaim = text.rfind('!')
            last_boundary = max(last_period, last_question, last_exclaim)

            if last_boundary > 0:
                text = text[:last_boundary + 1]

    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    # Add back period if needed
    if text and not text.endswith(('.', '?', '!')):
        text += '.'

    if len(text) < original_length * 0.9:  # If we removed more than 10%
        print(f"Removed hallucinations: reduced text from {original_length} to {len(text)} chars", flush=True)

    return text
