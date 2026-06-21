import asyncio
import os
import sys
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, FloodWait
from config import Config
from database import db
from server import web_server
from aiohttp import web

bot = Client("FileStreamBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

async def auto_delete(file_msg, info_msg):
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    try:
        await file_msg.delete()
        await info_msg.delete()
    except: pass

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    await db.add_user(user.id)
    
    # Force Subscribe
    try:
        await client.get_chat_member(Config.FSUB_CHANNEL, user.id)
    except UserNotParticipant:
        return await message.reply_text(
            "❌ **বট ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 জয়েন চ্যানেল", url=Config.CH1)]])
        )
    except Exception: pass

    # Deep link file request
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        f_id = int(message.command[1].split("_")[1])
        try:
            f_msg = await client.copy_message(user.id, Config.FILE_STORE_ID, f_id)
            info = await f_msg.reply_text(f"⚠️ এই ফাইলটি {Config.AUTO_DELETE_TIME//60} মিনিট পর অটো ডিলিট হবে।")
            asyncio.create_task(auto_delete(f_msg, info))
            return
        except:
            return await message.reply_text("দুঃখিত, ফাইলটি পাওয়া যায়নি!")

    # Normal Start
    text = (f"👋 হ্যালো {user.first_name}!\n\n"
            f"👤 **ইউজার ডিটেইলস:**\n"
            f"├ 🆔 আইডি: `{user.id}`\n"
            f"└ 🔗 ইউজারনেম: @{user.username}\n\n"
            "যেকোনো ফাইল পাঠান লিংক তৈরি করতে।")
    
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton("Channel 1", url=Config.CH1), InlineKeyboardButton("Channel 2", url=Config.CH2)],
        [InlineKeyboardButton("Channel 3", url=Config.CH3), InlineKeyboardButton("Channel 4", url=Config.CH4)]
    ])
    await message.reply_photo(Config.BOT_LOGO, caption=text, reply_markup=btns)

@bot.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats_handler(client, message):
    total = await db.total_users()
    await message.reply_text(f"📊 **বট স্ট্যাটাস:**\n\nমোট ইউজার: {total}")

@bot.on_message(filters.command("broadcast") & filters.user(Config.ADMINS) & filters.reply)
async def broadcast_handler(client, message):
    users = await db.get_all_users()
    msg = message.reply_to_message
    sent = 0
    await message.reply_text("🚀 ব্রডকাস্ট শুরু হয়েছে...")
    async for user in users:
        try:
            await msg.copy(user["id"])
            sent += 1
            await asyncio.sleep(0.3)
        except Exception: pass
    await message.reply_text(f"✅ ব্রডকাস্ট শেষ! মোট পাঠানো হয়েছে: {sent}")

@bot.on_message(filters.command("set_watermark") & filters.user(Config.ADMINS))
async def set_wm(client, message):
    if len(message.command) < 2: return await message.reply("`/set_watermark @আপনারনাম` এভাবে লিখুন।")
    text = message.text.split(None, 1)[1]
    await db.set_watermark(text)
    await message.reply(f"✅ ওয়াটারমার্ক সেট হয়েছে: `{text}`")

@bot.on_message(filters.private & (filters.video | filters.document | filters.audio))
async def media_handler(client, message):
    stored = await message.forward(Config.FILE_STORE_ID)
    s_link = f"{Config.URL}/watch/{stored.id}"
    d_link = f"{Config.URL}/dl/{stored.id}"
    
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("• STREAM •", url=s_link), InlineKeyboardButton("• DOWNLOAD •", url=d_link)],
        [InlineKeyboardButton("• GET FILE •", url=f"https://t.me/{Config.BOT_USERNAME}?start=file_{stored.id}")]
    ])
    await message.reply_text(f"✅ ফাইল লিংক তৈরি হয়েছে!\n\n🖥️ স্ট্রিম লিংক: {s_link}", reply_markup=btn)

async def start_bot():
    print("--- বট স্টার্ট হচ্ছে... ---")
    try:
        await bot.start()
    except FloodWait as e:
        print(f"FLOOD WAIT: {e.value} seconds")
        await asyncio.sleep(e.value)
        await bot.start()
    
    print("--- বট লাইভ! সার্ভার চালু হচ্ছে... ---")
    app = await web_server(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", Config.PORT))
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"--- সার্ভার চালু পোর্ট: {port} ---")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
