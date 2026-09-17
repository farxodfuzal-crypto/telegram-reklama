# Ruxsatli Telegram e'lon boti

Bu loyiha **faqat o'zingiz boshqaradigan yoki yozma ruxsat olgan guruhlarga** e'lon yuborish uchun mustaqil botdir. U begona guruhlarni qidirish, ikki foydalanuvchi akkauntini navbatlab ishlatish yoki spam-filtrlarni chetlab o'tishni qilmaydi.

## O'rnatish

1. Kompyuterda `python -m venv .venv` va keyin `.venv/bin/pip install -r requirements.txt` bajaring.
2. Telegram'da [@BotFather](https://t.me/BotFather) orqali bot yarating va tokenni oling.
3. `config.json` ichidagi `bot_token` o'rniga tokenni, `admin_user_ids` ichidagi `123456789` o'rniga o'zingizning Telegram ID'ingizni yozing. ID uchun @userinfobot dan foydalanishingiz mumkin.
4. `python main_bot.py` bilan ishga tushiring.
5. E'lon olishi kerak bo'lgan har bir guruhga botni administrator qilib qo'shing. Guruhning ichida administrator akkauntingizdan `/add_group` yozing.

## Buyruqlar

* `/settext matn` — e'lon matnini saqlaydi. Masalan: `/settext {Salom|Assalomu alaykum}! Yuk tashish xizmati mavjud.`
* `/list_groups` — ruxsatli guruhlarni ko'rsatadi.
* `/remove_group -100...` — guruhni yuborish ro'yxatidan olib tashlaydi.
* `/send` — kunlik limit doirasida yuboradi.
* `/status` — bugungi hisob va guruhlar soni.
* `/stop` — faol yuborishni to'xtatadi.

`accounts.json` dagi hisob har yangi kunda avtomatik nolga qaytadi. `daily_limit` ni faqat guruh administratorlari bilan kelishilgan jo'natish miqdoriga o'zgartiring.
