# ==============================================================================
# FILE NAME: media_pipeline.py
# DESCRIPTION: 100% Free Credit-Free Image & Voice Generation Pipeline
# ==============================================================================
import os
import random
import io
import requests
import logging
from gtts import gTTS

logger = logging.getLogger("MediaPipeline")

class AdvancedMediaPipelineManager:
    def __init__(self, stability_key=None, elevenlabs_key=None):
        logger.info("Initializing Free AdvancedMediaPipelineManager...")

    def generate_aesthetic_image(self, aesthetic_prompt_modifier):
        """Generates images completely free using Pollinations.ai (No API key or credits needed)."""
        try:
            full_prompt = f"Beautiful young woman, realistic human face, {aesthetic_prompt_modifier}, photorealistic, 4k"
            encoded_prompt = requests.utils.quote(full_prompt)
            # Pollinations provides free, keyless AI image generation
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            logger.info(f"Fetching free image from Pollinations.ai with prompt: {aesthetic_prompt_modifier}")
            response = requests.get(image_url, timeout=40)
            
            if response.status_code == 200:
                logger.info("Free image successfully generated and buffered.")
                return io.BytesIO(response.content)
            
            logger.warning(f"Pollinations API responded with non-200 status: {response.status_code}")
            return None

        except Exception as error:
            logger.error(f"Exception during free image generation: {error}")
            return None

    def generate_emotional_voice_note(self, spoken_text_script):
        """Generates voice notes completely free using gTTS (Google Text-to-Speech)."""
        try:
            logger.info("Generating free voice note via gTTS...")
            # gTTS works completely free without any credits or API subscription
            tts = gTTS(text=spoken_text_script, lang='hi', slow=False)
            
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_buffer.name = "voice_note.mp3"
            
            logger.info("Voice note successfully generated via gTTS.")
            return audio_buffer

        except Exception as error:
            logger.error(f"Exception encountered during gTTS voice generation: {error}")
            return None
