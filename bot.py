import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from motor.motor_asyncio import AsyncIOMotorClient
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

# Variables
TOKEN = os.getenv("BOT_TOKEN")
MONGO = os.getenv("MONGO_URI")

bot = Bot(token=TOKEN)
dp = Dispatcher()
db = AsyncIOMotorClient(MONGO)['kushal_db']

# --- Web Server (Render ke liye zaroori) ---
async def handle(request):
    return web.Response(text="Kushal Bot is Alive 24/7")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()

# --- CC Logic ---
def is_luhn_valid(cc):
    digits = [int(d) for d in str(cc) if d.isdigit()]
    return sum(digits[::-2] + [sum(divmod(2 * d, 10)) for d in digits[-2::-2]]) % 10 == 0

@dp.message(F.text.startswith(".chk"))
async def chk(message: types.Message):
    args = message.text.split()
    if len(args) < 2: return await message.reply("Format: `.chk cc|mm|yy|cvv`")
    
    cc = args[1].split('|')[0]
    is_valid = is_luhn_valid(cc)
    
    status = "Approved ✅" if is_valid else "Declined ❌"
    await message.reply(f"💳 Card: {cc}\n📡 Status: {status}\n👤 User: {message.from_user.full_name}")

async def main():
    await start_web_server() # Web server start
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
