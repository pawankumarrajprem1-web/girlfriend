# ==============================================================================
# FILE NAME: media_pipeline.py
# DESCRIPTION: Stability AI Image Generation & ElevenLabs Neural TTS Pipeline
# ==============================================================================
import os
import random
import io
import base64
import requests
import logging

logger = logging.getLogger("MediaPipeline")

class AdvancedMediaPipelineManager:
    """
    Handles asynchronous external API calls to Stability AI for hyper-realistic visual rendering
    and ElevenLabs for human-like emotional voice note generation.
    """
    def __init__(self, stability_key, elevenlabs_key):
        logger.info("Initializing AdvancedMediaPipelineManager...")
        self.stability_api_key = stability_key
        self.elevenlabs_api_key = elevenlabs_key

    def generate_aesthetic_image(self, aesthetic_prompt_modifier):
        """Interacts with Stability AI SDXL endpoint to generate immersive visual photographs."""
        try:
            endpoint = "https://api.stability.v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "steps": 35,
                "width": 512,
                "height": 512,
                "seed": random.randint(10000, 999999),
                "cfg_scale": 8.0,
                "samples": 1,
                "text_prompts": [
                    {
                        "text": f"Beautiful young woman, realistic human face, highly detailed skin texture, {aesthetic_prompt_modifier}, photorealistic, masterpiece, 4k resolution, natural lighting, expressive eyes",
                        "weight": 1.0
                    },
                    {
                        "text": "bad anatomy, deformed, mutated, extra fingers, blurry, low quality, cartoon, anime, illustration, painting, 3d render",
                        "weight": -1.0
                    }
                ]
            }
            
            logger.info(f"Dispatching image rendering request to Stability AI with modifier: {aesthetic_prompt_modifier}")
            response = requests.post(endpoint, json=payload, headers=headers, timeout=40)
            
            if response.status_code == 200:
                data = response.json()
                if "artifacts" in data and len(data["artifacts"]) > 0:
                    base64_img = data["artifacts"][0]["base64"]
                    binary_data = base64.b64decode(base64_img)
                    logger.info("Image successfully generated and decoded into binary stream.")
                    return io.BytesIO(binary_data)
            
            logger.warning(f"Stability AI responded with non-200 status code: {response.status_code}")
            return None

        except Exception as error:
            logger.error(f"Exception encountered during image generation pipeline execution: {error}")
            return None

    def generate_emotional_voice_note(self, spoken_text_script):
        """Interacts with ElevenLabs REST API to render expressive voice clips."""
        try:
            # Default premium expressive female neural voice ID
            voice_id = "21m00Tcm4TlvDq8ikWAM"
            endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            payload = {
                "text": spoken_text_script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.45,
                    "similarity_boost": 0.80,
                    "style": 0.35,
                    "use_speaker_boost": True
                }
            }
            
            logger.info("Dispatching text-to-speech rendering payload to ElevenLabs API...")
            response = requests.post(endpoint, json=payload, headers=headers, timeout=40)
            
            if response.status_code == 200:
                audio_buffer = io.BytesIO(response.content)
                audio_buffer.name = "voice_note.mp3"
                logger.info("Voice note successfully generated and buffered.")
                return audio_buffer
            
            logger.warning(f"ElevenLabs TTS API responded with non-200 status: {response.status_code}")
            return None

        except Exception as error:
            logger.error(f"Exception encountered during voice note generation pipeline execution: {error}")
            return None
