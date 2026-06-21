import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import Config
from database import db
from server import web_server
from aiohttp import web

# বট ক্লায়েন্ট সেটআপ
bot = Client(
    "FileStreamBot", 
    api_id=Config.API_ID, 
    api_hash=Config.API_HASH, 
    bot_token=Config.BOT_TOKEN
)

# অটো ডিলিট লজিক
async def auto_delete(msg):
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    try:
        await msg.delete()
        print("--- ফাইল অটো ডিলিট করা হয়েছে ---")
    except Exception as e:
        print(f"--- ডিলিট এরর: {e} ---")

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    await db.add_user(user.id)
    
    # Force Subscribe (বটকে চ্যানেলে অ্যাডমিন থাকতে হবে)
    try:
        await client.get_chat_member(Config.FSUB_CHANNEL, user.id)
    except UserNotParticipant:
        return await message.reply_text(
            "⛔ আগে আমাদের চ্যানেলে জয়েন করুন!", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 Join Channel", url=Config.CH1)]])
        )
    except Exception as e:
        print(f"Force Sub Error: {e}")

    # File Request Handling
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        f_id = int(message.command[1].split("_")[1])
        f_msg = await client.copy_message(user.id, Config.FILE_STORE_ID, f_id)
        reply = await f_msg.reply_text(f"⚠️ এই ফাইলটি {Config.AUTO_DELETE_TIME//60} মিনিট পর ডিলিট হয়ে যাবে।")
        asyncio.create_task(auto_delete(f_msg))
        asyncio.create_task(auto_delete(reply)) # ওয়ার্নিং মেসেজও ডিলিট হবে
        return

    # Start Message
    text = (f"👋 হ্যালো {user.first_name}!\n\n"
            f"👤 আইডি: `{user.id}`\n"
            f"🔗 ইউজারনেম: @{user.username}\n\n"
            "ফাইল পাঠান স্ট্রিমিং লিংক পেতে।")
    
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton("Channel 1", url=Config.CH1), InlineKeyboardButton("Channel 2", url=Config.CH2)],
        [InlineKeyboardButton("Channel 3", url=Config.CH3), InlineKeyboardButton("Channel 4", url=Config.CH4)]
    ])
    await message.reply_photo(Config.BOT_LOGO, caption=text, reply_markup=btns)

@bot.on_message(filters.command("set_watermark") & filters.user(Config.ADMINS))
async def set_wm(client, message):
    if len(message.command) < 2: 
        return await message.reply("ইউসেজ: `/set_watermark @YourName`")
    text = message.text.split(None, 1)[1]
    await db.set_watermark(text)
    await message.reply(f"✅ ওয়াটারমার্ক সেট হয়েছে: `{text}`")

@bot.on_message(filters.private & (filters.video | filters.document))
async def media_handler(client, message):
    try:
        stored = await message.forward(Config.FILE_STORE_ID)
        s_link = f"{Config.URL}/watch/{stored.id}"
        
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("• STREAM •", url=s_link), InlineKeyboardButton("• DOWNLOAD •", url=s_link)],
            [InlineKeyboardButton("• GET FILE •", url=f"https://t.me/{Config.BOT_USERNAME}?start=file_{stored.id}")]
        ])
        await message.reply_text(f"✅ আপনার ফাইল তৈরি!\n\n🖥️ লিংক: {s_link}", reply_markup=btn)
    except Exception as e:
        print(f"Error handling media: {e}")

async def main():
    print("--- বট স্টার্ট করা হচ্ছে... ---")
    try:
        await bot.start()
        print("--- বট সফলভাবে চালু হয়েছে! ---")
    except Exception as e:
        print(f"--- মংগোডিবি বা বট টোকেন এরর: {e} ---")
        return

    # ওয়েব সার্ভার সেটআপ
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    
    # রেন্ডারের জন্য পোর্ট হ্যান্ডেলিং (১০০০০ অথবা ৮০৮০)
    port = int(os.environ.get("PORT", Config.PORT))
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"--- ওয়েব সার্ভার চালু হয়েছে পোর্ট: {port} ---")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
