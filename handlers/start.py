from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import OWNER_USERNAMES, SUPPORT_GROUP, SUPPORT_CHANNEL, FREE_TRIAL_LIMIT
from database import get_or_create_user

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await get_or_create_user(user.id, user.username)

    used = db_user["free_generations"]
    remaining = max(0, FREE_TRIAL_LIMIT - used) if not db_user["is_paid"] else "Unlimited (Paid)"

    text = (
        f"🤖 **Welcome to AI Studio Bot!**\n\n"
        f"Create high-quality Images and Videos powered by multi-engine AI models.\n\n"
        f"📊 **Your Plan status:**\n"
        f"• Free Trial Remaining: `{remaining}`\n"
        f"• Paid Account: `{'Yes' if db_user['is_paid'] else 'No'}`\n\n"
        f"👥 **Owners:** {OWNER_USERNAMES}\n"
        f"💬 **Support Group:** {SUPPORT_GROUP}\n"
        f"📢 **Updates Channel:** {SUPPORT_CHANNEL}"
    )

    keyboard = [
        [InlineKeyboardButton("🎨 Generate Image", callback_data="btn_img"), InlineKeyboardButton("🎬 Create Video", callback_data="btn_vid")],
        [InlineKeyboardButton("👤 My Profile", callback_data="btn_profile"), InlineKeyboardButton("💎 Buy Credits / Pro", callback_data="btn_buy")],
        [InlineKeyboardButton("💬 Support Channel", url=f"https://t.me/{SUPPORT_CHANNEL.replace('@','')}")]
    ]

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"🛠️ **AI Studio Support**\n\n"
        f"• Owners: {OWNER_USERNAMES}\n"
        f"• Group: {SUPPORT_GROUP}\n"
        f"• Channel: {SUPPORT_CHANNEL}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")
