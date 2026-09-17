"""Kunlik ruxsat etilgan jo'natmalar hisobini xavfsiz boshqarish."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ACCOUNTS_FILE = Path(__file__).with_name("accounts.json")


def load_accounts() -> dict:
    return json.loads(ACCOUNTS_FILE.read_text(encoding="utf-8"))


def save_accounts(accounts: dict) -> None:
    ACCOUNTS_FILE.write_text(json.dumps(accounts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reset_if_new_day(accounts: dict) -> bool:
    """Sana o'zgargan bo'lsa, jo'natmalar hisoblagichini nolga qaytaradi."""
    today = date.today().isoformat()
    changed = False
    for account in accounts.values():
        if account.get("last_reset_date") != today:
            account["messages_sent_today"] = 0
            account["last_reset_date"] = today
            changed = True
    return changed


def can_send(accounts: dict, account_name: str = "delivery_bot") -> bool:
    account = accounts[account_name]
    return int(account["messages_sent_today"]) < int(account["daily_limit"])


def record_sent(accounts: dict, account_name: str = "delivery_bot") -> None:
    accounts[account_name]["messages_sent_today"] += 1
    save_accounts(accounts)
