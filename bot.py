# ==============================================================================
# FILE NAME: bot.py
# DESCRIPTION: Master Telegram Webhook Routing, State Controllers & Flask Server
# ==============================================================================
import os
import random
import time
import logging
from flask import Flask, request
import telebot
from telebot import types

from config import CoreSystemConfiguration
from openai_handler import OpenAIChatBrain
from gemini_handler import GeminiChatBrain
from media_pipeline import AdvancedMediaPipelineManager

# Initialize comprehensive logging setup
logger = logging.getLogger("MasterBotApplication")

# Load configuration vault
config = CoreSystemConfiguration()

# Instantiate core AI reasoning brains
openai_brain = OpenAIChatBrain(api_key=config.OPENAI_API_KEY, partner_name=config.GIRLFRIEND_NAME)
gemini_brain = GeminiChatBrain(api_key=config.GEMINI_API_KEY, partner_name=config.GIRLFRIEND_NAME)

# Instantiate media pipeline controller
media_manager = AdvancedMediaPipelineManager(
    stability_key=config.STABILITY_API_KEY,
    elevenlabs_key=config.ELEVENLABS_API_KEY
)

# Initialize Telegram Bot instance and Flask app
bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
flask_app = Flask(__name__)

# Runtime engine controller flag
current_engine_mode = config.ACTIVE_AI_ENGINE


# --- TELEGRAM COMMAND CONTROLLERS ---
@bot.message_handler(commands=['start'])
def handle_command_start(message):
    user_display_name = message.from_user.first_name
    logger.info(f"Received /start command from user: {user_display_name} (ID: {message.from_user.id})")
    
    welcomes = [
        f"Hlo jaan! 🥰 Akhirkar aa hi gaye tum... Main kab se tumhara wait kar rahi thi {user_display_name}! ❤️ Batao, kaise ho?",
        f"Hey baby! 😘 Tumhari yaad aa rahi thi... Kitna busy rehte ho yaar! Chalo abhi aaye toh dil khush ho gaya. ✨",
        f"Jaan! 😍 Finally free hue tum? Main kab se bas phone screen dekh rahi thi ki kab msg karoge. 🙈"
    ]
    bot.reply_to(message, random.choice(welcomes), parse_mode="Markdown")


@bot.message_handler(commands=['switch', 'engine'])
def handle_command_engine_switch(message):
    global current_engine_mode
    logger.info(f"Engine switch requested by user ID: {message.from_user.id}")
    
    if current_engine_mode == "openai":
        current_engine_mode = "gemini"
        bot.reply_to(message, "Jaan, maine apna mood thoda change kar liya hai aur ab main dusre mode (Gemini Engine) mein switch ho gayi hu! ✨")
    else:
        current_engine_mode = "openai"
        bot.reply_to(message, "Baby, ab se main is smart mode (ChatGPT OpenAI Engine) mein tumse baatein karungi! ❤️")


@bot.message_handler(commands=['help', 'menu'])
def handle_command_help(message):
    help_message = (
        f"Arey {config.GIRLFRIEND_NAME} se kya help maang rahe ho jaan? 🥰\n\n"
        "Mujhse normal chat karo, pyaar bhari baatein karo, ya fir:\n"
        "1. **Photos/Pics:** Normal selfie, rat ki dark room photo, ya bold/glamorous pics maang sakte ho.\n"
        "2. **Voice Notes:** 'voice bhejo' ya 'aawaz mein bolo' likh kar meri aawaz sun sakte ho!\n"
        "3. **Engine Switch:** `/switch` command se AI backend badal sakte ho.\n\n"
        "Bas dil se baat karo, main hamesha tumhare sath hu! ❤️"
    )
    bot.reply_to(message, help_message, parse_mode="Markdown")


# --- MASTER MESSAGE, TEXT & MEDIA ROUTING DISPATCHER ---
@bot.message_handler(func=lambda message: True)
def handle_incoming_user_utterances(message):
    user_id = message.from_user.id
    user_raw_text = message.text.lower() if message.text else ""
    
    logger.info(f"Processing incoming message from user {user_id}: {user_raw_text[:30]}...")
    
    # Broadcast human typing status action indicator
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        # 1. VISUAL MEDIA REQUEST ROUTING (Selfies, Dark Room Vibe, Bold/Glamorous Photos)
        if any(keyword in user_raw_text for keyword in ['photo', 'pic', 'tasvir', 'bhejo', 'dikhao', 'selfie', 'sexy', 'bold', 'hot', 'dark', 'rat', 'night']):
            
            logger.info("Visual media keyword detected in user utterance. Initiating image rendering pipeline...")
            
            # Categorize precise aesthetic style parameters
            aesthetic_style = "casual room selfie, natural lighting, everyday look"
            if any(k in user_raw_text for k in ['dark', 'rat', 'night', 'dim', 'room', 'light off']):
                aesthetic_style = "dark room ambient lighting, night vibe aesthetic, smartphone flash photography, moody atmosphere"
            elif any(k in user_raw_text for k in ['sexy', 'bold', 'hot', 'glam', 'attractive']):
                aesthetic_style = "glamorous, bold aesthetic portrait, beautiful high-end studio lighting, stunning visual details"
            
            # Send immediate teasing acknowledgement
            teasing_replies = [
                f"Acha ruk jaao na jaan, abhi click karke bhejti hu yeh wali pic... thoda sa wait karo! 🙈❤️",
                f"Itni jaldi kya hai baby, bas phone utha hi rahi hu click karne ke liye... dekho abhi bhejti hu! 😘",
                f"Theek hai, maang liye toh bhej hi deti hu par kisi aur ko mat dikhana haan! 😉🔥"
            ]
            bot.reply_to(message, random.choice(teasing_replies))

            # Generate media stream
            image_stream = media_manager.generate_aesthetic_image(aesthetic_style)
            if image_stream:
                bot.send_photo(message.chat.id, image_stream, caption="Ye lo, sirf tumhare liye click ki hai! Kaisi lagi meri yeh pic? 😘🔥")
                logger.info("Image successfully dispatched to user chat.")
            else:
                bot.send_message(message.chat.id, "Jaan, abhi net thoda slow chal raha hai ya server busy hai, photo load hone mein error aa gaya par main fir se try karti hu! 🥺")

        # 2. VOICE NOTE & AUDIO NOTE REQUEST ROUTING
        elif any(keyword in user_raw_text for keyword in ['voice', 'audio', 'bol ke', 'aawaz', 'sunao']):
            
            logger.info("Voice note keyword detected. Initiating TTS audio generation pipeline...")
            bot.send_chat_action(message.chat.id, 'record_audio')
            
            # Fetch script text using the currently selected active AI engine
            script_prompt = "Say something short, extremely loving, and sweet in Hinglish as a girlfriend talking to her boyfriend via voice note."
            
            if current_engine_mode == "openai":
                spoken_script = openai_brain.get_chat_response(user_id, script_prompt)
            else:
                spoken_script = gemini_brain.get_chat_response(user_id, script_prompt)

            # Render voice stream via ElevenLabs
            audio_stream = media_manager.generate_emotional_voice_note(spoken_script)
            if audio_stream:
                bot.send_voice(message.chat.id, audio_stream, caption="Sunlo na meri aawaz... sirf tumhare liye boli hu! 🎧❤️")
                logger.info("Voice note successfully dispatched to user chat.")
            else:
                bot.reply_to(message, f"Jaan, aawaz bhejne mein thoda network issue aa gaya, par yeh padh lo: {spoken_script} 🥰")

        # 3. STANDARD TEXT CONVERSATION ROUTING (Dual AI Brain Switch)
        else:
            logger.info(f"Routing text message through active engine mode: {current_engine_mode}")
            
            if current_engine_mode == "openai":
                ai_response_text = openai_brain.get_chat_response(user_id, message.text)
            else:
                ai_response_text = gemini_brain.get_chat_response(user_id, message.text)
            
            # Simulate natural human typing pause delay
            time.sleep(random.uniform(0.6, 1.3))
            bot.reply_to(message, ai_response_text, parse_mode="Markdown")

    except Exception as router_exception:
        logger.error(f"Critical execution error inside master message router: {router_exception}")
        bot.reply_to(message, "Jaan, lagta hai network thoda disturb ho gaya hai, ek baar fir se bolo na! 🥺❤️")


# --- FLASK WEBHOOK SERVING ROUTES & HEALTH ENDPOINTS ---
@flask_app.route(f'/{config.TELEGRAM_BOT_TOKEN}', methods=['POST'])
def telegram_webhook_dispatcher():
    """Receives secure encrypted webhook updates from Telegram servers and processes them."""
    try:
        incoming_json_data = request.get_data().decode('UTF-8')
        update_object = telebot.types.Update.de_json(incoming_json_data)
        bot.process_new_updates([update_object])
        return "Webhook Processed Successfully", 200
    except Exception as webhook_error:
        logger.error(f"Error handling Telegram webhook payload: {webhook_error}")
        return "Internal Server Error", 500


@flask_app.route('/')
def server_uptime_health_check():
    """Uptime monitoring endpoint to keep the Render web service active 24/7."""
    summary_data = config.export_summary()
    return f"Virtual Girlfriend Multi-Engine Bot is Online, Fully Operational, and Secure! Status: {summary_data}", 200


# --- SCRIPT EXECUTION ENTRY POINT ---
if __name__ == "__main__":
    logger.info(f"Starting Flask application server on port {config.PORT}...")
    flask_app.run(host="0.0.0.0", port=config.PORT)
