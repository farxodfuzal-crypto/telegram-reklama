"""Administrator ruxsat bergan Telegram guruhlari uchun mustaqil e'lon boti."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import Application, CommandHandler, ContextTypes

from search_groups import add_authorized_group, remove_group, selected_groups
from send_messages import send_to_authorized_groups
from warming import load_accounts, reset_if_new_day, save_accounts

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
send_stop_event = asyncio.Event()


def is_admin(update: Update) -> bool:
    return bool(update.effective_user and update.effective_user.id in CONFIG["admin_user_ids"])


async def require_admin(update: Update) -> bool:
    if not is_admin(update):
        await update.effective_message.reply_text("Bu buyruq faqat bot administratori uchun.")
        return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Bu bot faqat siz boshqaradigan yoki yozma ruxsat olgan guruhlarga e'lon yuboradi.\n\n"
        "Guruhga botni admin qilib qo'shing, so'ng guruhning ichida /add_group yozing.\n"
        "Boshqaruv: /settext, /list_groups, /remove_group, /send, /status, /stop"
    )


async def add_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update): return
    chat = update.effective_chat
    if chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        await update.effective_message.reply_text("/add_group ni kerakli guruhning o'zida yuboring.")
        return
    member = await context.bot.get_chat_member(chat.id, context.bot.id)
    if member.status not in ("administrator", "creator", "owner"):
        await update.effective_message.reply_text("Avval botni shu guruhda administrator qiling.")
        return
    if add_authorized_group(chat.id, chat.title or str(chat.id)):
        await update.effective_message.reply_text("Guruh ruxsatli ro'yxatga qo'shildi.")
    else:
        await update.effective_message.reply_text("Bu guruh ro'yxatda bor.")


async def set_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update): return
    text = " ".join(context.args).strip()
    if not text:
        await update.effective_message.reply_text("Misol: /settext {Salom|Assalomu alaykum}! Xizmatimiz mavjud.")
        return
    CONFIG["default_message"] = text
    (ROOT / "config.json").write_text(json.dumps(CONFIG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    await update.effective_message.reply_text("Matn saqlandi.")


async def list_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update): return
    groups = selected_groups()
    answer = "Tanlangan ruxsatli guruhlar:\n" + ("\n".join(f"• {x['title']} ({x['id']})" for x in groups) if groups else "Ro'yxat bo'sh.")
    await update.effective_message.reply_text(answer)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update): return
    try: chat_id = int(context.args[0])
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Misol: /remove_group -1001234567890")
        return
    await update.effective_message.reply_text("Guruh o'chirildi." if remove_group(chat_id) else "Bunday guruh topilmadi.")


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update): return
    send_stop_event.clear()
    await update.effective_message.reply_text("Jo'natish boshlandi. /stop bilan to'xtatasiz.")
    result = await send_to_authorized_groups(context.bot, CONFIG["default_message"], CONFIG["min_delay_seconds"], CONFIG["max_delay_seconds"], send_stop_event)
    await update.effective_message.reply_text(f"Tugadi: {result['sent']} yuborildi, {result['failed']} xato. Limit: {'yetdi' if result['limited'] else 'yetmadi'}.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update): return
    accounts = load_accounts()
    if reset_if_new_day(accounts): save_accounts(accounts)
    item = accounts["delivery_bot"]
    await update.effective_message.reply_text(f"Bugun: {item['messages_sent_today']}/{item['daily_limit']}. Guruhlar: {len(selected_groups())}.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await require_admin(update):
        send_stop_event.set(); await update.effective_message.reply_text("Jo'natish to'xtatish uchun belgilandi.")


def main() -> None:
    if CONFIG["bot_token"].startswith("PASTE_"):
        raise SystemExit("config.json ichiga BotFather tokeni va o'zingizning Telegram ID raqamingizni yozing.")
    app = Application.builder().token(CONFIG["bot_token"]).build()
    for command, handler in [("start", start), ("settext", set_text), ("add_group", add_group), ("list_groups", list_groups), ("remove_group", remove), ("send", send), ("status", status), ("stop", stop)]:
        app.add_handler(CommandHandler(command, handler))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
