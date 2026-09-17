"""Matnni reklama mazmunini saqlagan holda ko'rinishini o'zgartirish vositalari."""

from __future__ import annotations

import random
import re

PREFIXES = ["Diqqat", "Muhim", "Yangilik", "E'lon", "Taklif", ""]
EMOJIS = ["🔥", "⚡", "💥", "✨", "🌟", "🎯", "🚀", "💎", "👀", "⭐", "📢", "❗", "✅", ""]
PUNCTUATION = [".", "..", "...", "!", "!!", "?", ""]
SPINTAX_PATTERN = re.compile(r"\{([^{}]+)\}")


def resolve_spintax(text: str) -> str:
    """Har bir ``{a|b|c}`` blokidan bitta variant tanlaydi."""
    while True:
        match = SPINTAX_PATTERN.search(text)
        if not match:
            return text
        choices = [item.strip() for item in match.group(1).split("|") if item.strip()]
        replacement = random.choice(choices) if choices else ""
        text = text[: match.start()] + replacement + text[match.end() :]


def render_message(template: str) -> str:
    """Spintax, prefix, emoji va yakuniy tinish belgilarini qo'llaydi."""
    body = resolve_spintax(template).strip().rstrip(".!?")
    prefix, emoji, ending = random.choice(PREFIXES), random.choice(EMOJIS), random.choice(PUNCTUATION)
    lead = " ".join(part for part in (emoji, f"{prefix}!" if prefix else "") if part)
    return " ".join(part for part in (lead, body + ending) if part)
