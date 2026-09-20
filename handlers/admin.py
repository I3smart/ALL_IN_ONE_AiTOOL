from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_IDS
from database import add_credits

async def admin_give_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in OWNER_IDS:
        await update.message.reply_text("⛔ Unauthorized. Owner access only.")
        return

    try:
        target_user = int(context.args[0])
        amount = int(context.args[1])
        await add_credits(target_user, amount)
        await update.message.reply_text(f"✅ Added {amount} credits to user `{target_user}`.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: `/give_credits <user_id> <amount>`", parse_mode="Markdown")
