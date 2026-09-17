"""Tasdiqlangan guruhlarga ehtiyotkor, limitli e'lon yuborish."""

from __future__ import annotations

import asyncio
import random

from telegram.error import Forbidden, RetryAfter, TelegramError

from search_groups import selected_groups
from spintax_utils import render_message
from warming import can_send, load_accounts, record_sent, reset_if_new_day, save_accounts


async def send_to_authorized_groups(bot, template: str, min_delay: int, max_delay: int, stop_event: asyncio.Event) -> dict:
    """Bitta botning kunlik limiti doirasida faqat tasdiqlangan guruhlarga jo'natadi."""
    accounts = load_accounts()
    if reset_if_new_day(accounts):
        save_accounts(accounts)
    result = {"sent": 0, "failed": 0, "limited": False}
    for group in selected_groups():
        if stop_event.is_set():
            break
        if not can_send(accounts):
            result["limited"] = True
            break
        await asyncio.sleep(random.randint(5, 15))
        try:
            await bot.send_message(chat_id=group["id"], text=render_message(template))
        except RetryAfter as error:
            await asyncio.sleep(int(error.retry_after) + 10)
            result["failed"] += 1
        except (Forbidden, TelegramError):
            result["failed"] += 1
        else:
            record_sent(accounts)
            result["sent"] += 1
        if not stop_event.is_set():
            await asyncio.sleep(random.randint(min_delay, max_delay))
    return result
