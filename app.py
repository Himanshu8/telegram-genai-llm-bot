from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from rag import rag_pipeline
from vision import caption_image

import sqlite3
import datetime
import asyncio

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# ================================
# 🗄️ DATABASE
# ================================
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    user_message TEXT,
    bot_response TEXT,
    timestamp TEXT
)
""")
conn.commit()


def save_chat(user_id, user_msg, bot_msg):
    cursor.execute(
        "INSERT INTO chats (user_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, user_msg, bot_msg, str(datetime.datetime.now()))
    )
    conn.commit()


# ================================
# 🔥 MEMORY
# ================================
user_memory = {}

def update_memory(user_id, message):
    user_memory.setdefault(user_id, []).append(message)
    user_memory[user_id] = user_memory[user_id][-3:]


# ================================
# ⌨️ TYPING EFFECT (BEST VERSION)
# ================================
async def send_typing(update, text):
    msg = await update.message.reply_text("⏳ Thinking...")

    words = text.split()
    current = ""

    for word in words:
        current += word + " "
        await msg.edit_text(current)
        await asyncio.sleep(0.05)   # 🔥 speed control


# ================================
# 🔹 START
# ================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to GenAI Bot!\n\n"
        "/ask <query>\n/image\n/help"
    )


# ================================
# 🔹 ASK
# ================================
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    user_id = update.effective_user.id

    update_memory(user_id, query)

    history = "\n".join(user_memory[user_id])
    full_query = f"{history}\n\n{query}"

    answer = rag_pipeline(full_query)

    save_chat(user_id, query, answer)

    # 🔥 typing effect instead of instant reply
    await send_typing(update, answer)


# ================================
# 🔹 HELP
# ================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/ask <query>\n/image\n/help")


# ================================
# 🔹 IMAGE
# ================================
async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Upload an image.")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    caption, tags = caption_image(file_path)

    response_text = f"Caption: {caption}\nTags: {', '.join(tags)}"

    user_id = update.effective_user.id
    save_chat(user_id, "IMAGE", response_text)

    await send_typing(update, response_text)


# ================================
# 🔹 MAIN
# ================================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("image", image_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()