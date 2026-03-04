from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import sqlite3

TOKEN = "8276142355:AAFOkAxeWUmHzMXfE49eM3Jl86pYoILALmY"

db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
referrals INTEGER
)
""")

# 👇 तुम्हारा course link
COURSE_LINK = "https://docs.google.com/document/d/133FcsRV5DztkE5HRp9vQzSKJiNElnW7_0DsTfZgkhc4/edit?usp=sharing"

WELCOME_TEXT = """
🚀 Free AI Tools Hub

Here you can access powerful AI tools for FREE.

✨ Generate unlimited AI images
🎬 Create AI videos
💻 Build websites and code with AI
🧠 Use advanced AI models
⚡ Explore multiple AI platforms in one place

👇 Choose a platform below to start using AI tools.

🎓 Want to learn Prompt Engineering?
Unlock the full course by inviting 3 friends.
"""

async def start(update, context):

    user_id = update.effective_user.id

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute("INSERT INTO users (user_id, referrals) VALUES (?, ?)", (user_id, 0))
        db.commit()

        if context.args and context.args[0].isdigit():
            referrer_id = int(context.args[0])
            if referrer_id != user_id:
                cursor.execute("UPDATE users SET referrals = referrals + 1 WHERE user_id=?", (referrer_id,))
                db.commit()

    keyboard = [
        [InlineKeyboardButton("Chatbot Arena", url="https://lmarena.ai")],
        [InlineKeyboardButton("Hugging Face", url="https://huggingface.co")],
        [InlineKeyboardButton("Replicate", url="https://replicate.com")],
        [InlineKeyboardButton("Poe AI", url="https://poe.com")],
        [InlineKeyboardButton("Yupp AI", url="https://yupp.ai")],
        [InlineKeyboardButton("🎓 Full Prompt Engineering Course", callback_data="course")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=reply_markup
    )

async def course(update, context):

    query = update.callback_query
    user_id = query.from_user.id

    cursor.execute("SELECT referrals FROM users WHERE user_id=?",(user_id,))
    refs = cursor.fetchone()[0]

    if refs >= 3:

        await query.message.reply_text(
            f"✅ Congratulations!\n\nHere is your Prompt Engineering Course:\n\n{COURSE_LINK}"
        )

    else:

        # Make sure to replace YOUR_BOT_USERNAME with your actual bot's username!
        invite_link = f"https://t.me/free5ai_bot?start={user_id}"

        await query.message.reply_text(
            f"""
🎓 Prompt Engineering Course

Unlock the full Prompt Engineering course for FREE.

📢 Invite 3 friends using your personal link below.

Once 3 friends join the bot using your link,
the full course will be unlocked instantly.

Your progress: {refs}/3

Invite Link:
{invite_link}
"""
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(course, pattern="course"))

app.run_polling()
