# ==============================================================================
# FILE NAME: media_pipeline.py
# DESCRIPTION: 100% Free Credit-Free Image & Voice Generation Pipeline
# ==============================================================================
import os
import io
import requests
import logging
from gtts import gTTS

logger = logging.getLogger("MediaPipeline")

class AdvancedMediaPipelineManager:
    def __init__(self, stability_key=None, elevenlabs_key=None):
        logger.info("Initializing Free AdvancedMediaPipelineManager...")

    def generate_aesthetic_image(self, aesthetic_prompt_modifier):
        try:
            full_prompt = f"Beautiful young woman, realistic human face, {aesthetic_prompt_modifier}, photorealistic, 4k"
            encoded_prompt = requests.utils.quote(full_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            logger.info(f"Fetching free image from Pollinations.ai...")
            response = requests.get(image_url, timeout=40)
            
            if response.status_code == 200:
                return io.BytesIO(response.content)
            return None

        except Exception as error:
            logger.error(f"Exception during free image generation: {error}")
            return None

    def generate_emotional_voice_note(self, spoken_text_script):
        try:
            logger.info("Generating free voice note via gTTS...")
            tts = gTTS(text=spoken_text_script, lang='hi', slow=False)
            
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_buffer.name = "voice_note.mp3"
            
            return audio_buffer

        except Exception as error:
            logger.error(f"Exception encountered during gTTS voice generation: {error}")
            return None
