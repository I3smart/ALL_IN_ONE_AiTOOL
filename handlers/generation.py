from telegram import Update
from telegram.ext import ContextTypes
from database import check_and_consume_credit
from providers.gemini_provider import GeminiProvider
from providers.video_provider import CustomVideoProvider

gemini_engine = GeminiProvider()
video_engine = CustomVideoProvider()

async def image_gen_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text("Usage: `/generate_image <your description>`", parse_mode="Markdown")
        return

    allowed = await check_and_consume_credit(user_id)
    if not allowed:
        await update.message.reply_text("❌ You have reached your 3 free trials. Use `/plans` to purchase Stars access!")
        return

    msg = await update.message.reply_text("⏳ Generating image via AI model...")
    try:
        img_url = await gemini_engine.generate_image(prompt)
        await update.message.reply_photo(photo=img_url, caption=f"✨ **Prompt:** {prompt}")
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"⚠️ Error generating image: {str(e)}")

async def video_gen_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text("Usage: `/generate_video <your script / prompt>`", parse_mode="Markdown")
        return

    allowed = await check_and_consume_credit(user_id)
    if not allowed:
        await update.message.reply_text("❌ You have reached your 3 free trials limit. Use `/plans` to purchase Stars access!")
        return

    msg = await update.message.reply_text("⏳ Processing script to video engine...")
    try:
        video_url = await video_engine.generate_video(prompt)
        await update.message.reply_video(video=video_url, caption=f"🎬 **Script:** {prompt}")
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"⚠️ Error creating video: {str(e)}")
