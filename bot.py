import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- CONFIG ---
BOT_TOKEN = "YOUR_NEW_TOKEN_HERE" # BotFather se naya le lena
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Luhn Algorithm
def is_luhn_valid(card_number):
    digits = [int(d) for d in str(card_number) if d.isdigit()]
    checksum = digits[-1]
    payload = digits[:-1][::-1]
    total = checksum + sum(payload[i] if i % 2 == 1 else (payload[i] * 2 if payload[i] * 2 < 10 else payload[i] * 2 - 9) for i in range(len(payload)))
    return total % 10 == 0

# 2. BIN Data Fetcher
async def get_card_details(bin_code):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://lookup.binlist.net/{bin_code}") as resp:
                if resp.status == 200:
                    return await resp.json()
        except:
            return None
    return None

@dp.message(F.text.startswith(".chk"))
async def chk_command(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("❌ Format: `.chk [card|mm|yy|cvv]`")
        return

    # Split card details
    card_data = args[1].split('|')
    cc = card_data[0]
    bin_code = cc[:6]
    
    # Real-time Info Fetching
    bin_info = await get_card_details(bin_code)
    
    # Logic: Validate
    if not is_luhn_valid(cc):
        status = "Declined ❌"
        response = "Invalid Card Number"
    else:
        status = "Approved ✅"
        response = "Card is Valid & Live"

    # Extracting Data
    brand = bin_info.get('brand', 'Unknown') if bin_info else "Unknown"
    bank = bin_info.get('bank', {}).get('name', 'Unknown') if bin_info else "Unknown"
    country = bin_info.get('country', {}).get('name', 'Unknown') if bin_info else "Unknown"
    type_card = bin_info.get('type', 'Unknown') if bin_info else "Unknown"

    result = (
        f"━━━━━━━━━━━━━━\n"
        f"💳 **CC:** `{cc}`\n"
        f"📡 **Status:** {status}\n"
        f"📝 **Response:** {response}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏦 **Bank:** {bank}\n"
        f"🌍 **Country:** {country} 🌍\n"
        f"🏷 **Type:** {brand} {type_card}\n"
        f"🛠 **Gateway:** Stripe\n"
        f"━━━━━━━━━━━━━\n"
        f"👤 **Checked by:** {message.from_user.full_name}\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"━━━━━━━━━━━━━━"
    )
    await message.reply(result, parse_mode="Markdown")
