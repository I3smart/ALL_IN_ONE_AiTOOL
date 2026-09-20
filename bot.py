import logging
from telegram.ext import ApplicationBuilder, CommandHandler, PreCheckoutQueryHandler, MessageHandler, filters

from config import BOT_TOKEN
from database import init_db
from handlers.start import start_handler, support_handler
from handlers.generation import image_gen_handler, video_gen_handler
from handlers.payments import send_invoice_handler, precheckout_handler, successful_payment_handler
from handlers.admin import admin_give_credits

logging.basicConfig(level=logging.INFO)

async def post_init(application):
    await init_db()

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing in .env file.")

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    # Commands
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("support", support_handler))
    app.add_handler(CommandHandler("generate_image", image_gen_handler))
    app.add_handler(CommandHandler("generate_video", video_gen_handler))
    app.add_handler(CommandHandler("plans", send_invoice_handler))
    app.add_handler(CommandHandler("give_credits", admin_give_credits))

    # Payment flow (Telegram Stars)
    app.add_handler(PreCheckoutQueryHandler(precheckout_handler))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))

    print("🤖 Telegram AI Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
