"""Ruxsatsiz guruhlarni qidirish o'rniga administrator tasdiqlagan guruhlar ro'yxati."""

from __future__ import annotations

import json
from pathlib import Path

GROUPS_FILE = Path(__file__).with_name("groups.json")
SELECTED_FILE = Path(__file__).with_name("selected_groups.json")


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, groups: list[dict]) -> None:
    path.write_text(json.dumps(groups, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def selected_groups() -> list[dict]:
    return _load(SELECTED_FILE)


def add_authorized_group(chat_id: int, title: str) -> bool:
    """Faqat bot qo'shilgan va admin tomonidan tasdiqlangan chatni saqlaydi."""
    group = {"id": chat_id, "title": title}
    all_groups = _load(GROUPS_FILE)
    if any(item["id"] == chat_id for item in all_groups):
        return False
    all_groups.append(group)
    _save(GROUPS_FILE, all_groups)
    chosen = selected_groups()
    chosen.append(group)
    _save(SELECTED_FILE, chosen)
    return True


def remove_group(chat_id: int) -> bool:
    groups = selected_groups()
    new_groups = [item for item in groups if item["id"] != chat_id]
    if len(groups) == len(new_groups):
        return False
    _save(SELECTED_FILE, new_groups)
    return True
