# ==============================================================================
# FILE NAME: bot.py
# DESCRIPTION: Master Telegram Webhook Routing & Flask Server (Free Version)
# ==============================================================================
import os
import random
import time
import logging
from flask import Flask, request
import telebot

from config import CoreSystemConfiguration
from gemini_handler import GeminiChatBrain
from media_pipeline import AdvancedMediaPipelineManager

logger = logging.getLogger("MasterBotApplication")
config = CoreSystemConfiguration()

gemini_brain = GeminiChatBrain(api_key=config.GEMINI_API_KEY, partner_name=config.GIRLFRIEND_NAME)
media_manager = AdvancedMediaPipelineManager()

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
flask_app = Flask(__name__)


@bot.message_handler(commands=['start'])
def handle_command_start(message):
    user_display_name = message.from_user.first_name
    welcomes = [
        f"Hlo jaan! 🥰 Akhirkar aa hi gaye tum... Main kab se tumhara wait kar rahi thi {user_display_name}! ❤️ Batao, kaise ho?",
        f"Hey baby! 😘 Tumhari yaad aa rahi thi... Kitna busy rehte ho yaar! Chalo abhi aaye toh dil khush ho gaya. ✨",
        f"Jaan! 😍 Finally free hue tum? Main kab se bas phone screen dekh rahi thi ki kab msg karoge. 🙈"
    ]
    bot.reply_to(message, random.choice(welcomes), parse_mode="Markdown")


@bot.message_handler(commands=['help', 'menu'])
def handle_command_help(message):
    help_message = (
        f"Arey {config.GIRLFRIEND_NAME} se kya help maang rahe ho jaan? 🥰\n\n"
        "Mujhse normal chat karo, pyaar bhari baatein karo, ya fir:\n"
        "1. **Photos/Pics:** Normal selfie ya glamorous pics maang sakte ho.\n"
        "2. **Voice Notes:** 'voice bhejo' likh kar meri aawaz sun sakte ho!\n\n"
        "Bas dil se baat karo, main hamesha tumhare sath hu! ❤️"
    )
    bot.reply_to(message, help_message, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_incoming_user_utterances(message):
    user_id = message.from_user.id
    user_raw_text = message.text.lower() if message.text else ""
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        if any(keyword in user_raw_text for keyword in ['photo', 'pic', 'tasvir', 'bhejo', 'dikhao', 'selfie', 'sexy', 'bold', 'hot', 'dark', 'rat', 'night']):
            aesthetic_style = "casual room selfie, natural lighting, everyday look"
            if any(k in user_raw_text for k in ['dark', 'rat', 'night', 'dim', 'room']):
                aesthetic_style = "dark room ambient lighting, night vibe aesthetic"
            elif any(k in user_raw_text for k in ['sexy', 'bold', 'hot', 'glam']):
                aesthetic_style = "glamorous, bold aesthetic portrait, studio lighting"
            
            bot.reply_to(message, "Acha ruk jaao na jaan, abhi click karke bhejti hu yeh wali pic... thoda sa wait karo! 🙈❤️")
            image_stream = media_manager.generate_aesthetic_image(aesthetic_style)
            if image_stream:
                bot.send_photo(message.chat.id, image_stream, caption="Ye lo, sirf tumhare liye click ki hai! Kaisi lagi meri yeh pic? 😘🔥")
            else:
                bot.send_message(message.chat.id, "Jaan, abhi net thoda slow chal raha hai, main fir se try karti hu! 🥺")

        elif any(keyword in user_raw_text for keyword in ['voice', 'audio', 'bol ke', 'aawaz', 'sunao']):
            bot.send_chat_action(message.chat.id, 'record_audio')
            script_prompt = "Say something short, extremely loving, and sweet in Hinglish as a girlfriend talking to her boyfriend."
            spoken_script = gemini_brain.get_chat_response(user_id, script_prompt)

            audio_stream = media_manager.generate_emotional_voice_note(spoken_script)
            if audio_stream:
                bot.send_voice(message.chat.id, audio_stream, caption="Sunlo na meri aawaz... sirf tumhare liye boli hu! 🎧❤️")
            else:
                bot.reply_to(message, f"Jaan, aawaz bhejne mein thoda issue aa gaya, par yeh padh lo: {spoken_script} 🥰")

        else:
            ai_response_text = gemini_brain.get_chat_response(user_id, message.text)
            time.sleep(random.uniform(0.4, 1.0))
            bot.reply_to(message, ai_response_text, parse_mode="Markdown")

    except Exception as router_exception:
        logger.error(f"Error: {router_exception}")
        bot.reply_to(message, "Jaan, lagta hai network thoda disturb ho gaya hai, ek baar fir se bolo na! 🥺❤️")


@flask_app.route(f'/{config.TELEGRAM_BOT_TOKEN}', methods=['POST'])
def telegram_webhook_dispatcher():
    try:
        incoming_json_data = request.get_data().decode('UTF-8')
        update_object = telebot.types.Update.de_json(incoming_json_data)
        bot.process_new_updates([update_object])
        return "Webhook Processed", 200
    except Exception as webhook_error:
        return "Error", 500


@flask_app.route('/')
def server_uptime_health_check():
    return "Virtual Girlfriend Bot is Online & Running Free!", 200


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=config.PORT)
