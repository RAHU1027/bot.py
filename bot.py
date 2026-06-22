import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from motor.motor_asyncio import AsyncIOMotorClient
from aiohttp import web
from datetime import datetime

# ========================================================
# KUSHAL PREMIUM CONFIG - BAS YE EK BAAR EDIT KARO
# ========================================================
TOKEN = "8878551213:AAEuXkfq8ZLkBZYZ7umIhrePCWKyinJObDw"
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority"
# ========================================================

bot = Bot(token=TOKEN)
dp = Dispatcher()
db = AsyncIOMotorClient(MONGO_URI)['kushal_premium_db']

# --- Web Server (24/7 Keeping) ---
async def start_web_server():
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Kushal Premium Bot Running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080))).start()

# --- Helpers ---
def is_luhn_valid(cc):
    digits = [int(d) for d in str(cc) if d.isdigit()]
    return sum(digits[::-2] + [sum(divmod(2 * d, 10)) for d in digits[-2::-2]]) % 10 == 0

async def get_bin_info(bin_code):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://lookup.binlist.net/{bin_code}") as resp:
                if resp.status == 200: return await resp.json()
        except: return None
    return None

# --- Commands ---
@dp.message(Command("start"))
async def welcome(message: types.Message):
    user = message.from_user
    mention = f"[{user.full_name}](tg://user?id={user.id})"
    text = (f"🔥 **WELCOME TO KUSHAL PREMIUM CC CHECKER** 🔥\n\n"
            f"👤 User: {mention}\n"
            f"🆔 ID: `{user.id}`\n\n"
            f"Command: `.chk [cc|mm|yy|cvv]`")
    
    photos = await bot.get_user_profile_photos(user.id, limit=1)
    if photos.total_count > 0:
        await bot.send_photo(message.chat.id, photos.photos[0][0].file_id, caption=text, parse_mode="Markdown")
    else:
        await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.startswith(".chk"))
async def check_cc(message: types.Message):
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ Format: `.chk cc|mm|yy|cvv`")
    
    cc = args[1].split('|')[0]
    bin_info = await get_bin_info(cc[:6])
    
    status = "Approved ✅" if is_luhn_valid(cc) else "Declined ❌"
    bank = bin_info.get('bank', {}).get('name', 'Unknown') if bin_info else "Unknown"
    country = bin_info.get('country', {}).get('name', 'Unknown') if bin_info else "Unknown"
    brand = bin_info.get('brand', 'Unknown') if bin_info else "Unknown"
    
    result = (f"✨ **KUSHAL CC RESULT** ✨\n"
              f"━━━━━━━━━━━━━━━━━━\n"
              f"💳 **CARD:** `{cc}`\n"
              f"📡 **STATUS:** {status}\n"
              f"🏦 **BANK:** {bank}\n"
              f"🌍 **COUNTRY:** {country}\n"
              f"🏷 **TYPE:** {brand}\n"
              f"━━━━━━━━━━━━━━━━━━\n"
              f"👤 **CHECKED BY:** {message.from_user.full_name}\n"
              f"🆔 **USER ID:** `{message.from_user.id}`\n"
              f"⏰ **TIME:** {datetime.now().strftime('%H:%M:%S')}")
    await message.reply(result, parse_mode="Markdown")

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
