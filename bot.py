import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from datetime import datetime

TOKEN = "8878551213:AAEuXkfq8ZLkBZYZ7umIhrePCWKyinJObDw"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_latest_key():
    with open("keys.txt", "r") as f:
        return f.readline().strip()

@dp.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    mention = f"[{user.full_name}](tg://user?id={user.id})"
    text = f"🔥 **KUSHAL PRO BOT ACTIVE** 🔥\n👤 {mention}\n🆔 `{user.id}`"
    await message.reply(text, parse_mode="Markdown")

@dp.message(F.text.startswith(".chk"))
async def chk(message: types.Message):
    cc = message.text.split()[1]
    key = get_latest_key() # Scraper ki nikaali hui key use karega
    
    # Yahan tumhara heavy validation logic (Gateway hit)
    await message.reply(f"🚀 Checking with Key: `{key[:10]}...`")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
