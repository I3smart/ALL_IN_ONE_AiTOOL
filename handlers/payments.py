from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes
from database import record_payment

async def send_invoice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    title = "AI Studio Unlimited Membership"
    description = "Get unlimited access to AI Image and Script-to-Video generation."
    payload = "ai_studio_pro_subscription"
    currency = "XTR"  # Telegram Stars
    prices = [LabeledPrice("Pro Access", 250)]  # 250 Telegram Stars

    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",  # Blank for Telegram Stars (XTR)
        currency=currency,
        prices=prices
    )

async def precheckout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != "ai_studio_pro_subscription":
        await query.answer(ok=False, error_message="Unknown order payload.")
    else:
        await query.answer(ok=True)

async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    user_id = update.effective_user.id

    await record_payment(
        user_id=user_id,
        charge_id=payment.telegram_payment_charge_id,
        amount=payment.total_amount,
        currency=payment.currency
    )

    await update.message.reply_text("🎉 **Payment Successful!** You now have Pro Access to AI Studio.")
