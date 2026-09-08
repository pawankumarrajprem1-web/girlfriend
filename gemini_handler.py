# ==============================================================================
# FILE NAME: gemini_handler.py
# DESCRIPTION: High-Performance Google Gemini Neural Processing Module
# ==============================================================================
import logging
import os
from google import genai
from persona_engine import VirtualGirlfriendPersonaMatrix

logger = logging.getLogger("GeminiEngine")

class GeminiChatBrain:
    """
    Manages stateful conversational chat sessions via Google's generative AI SDK,
    providing lightning-fast secondary reasoning and fallback intelligence.
    """
    def __init__(self, api_key, partner_name="Ananya"):
        logger.info("Initializing GeminiChatBrain subsystem...")
        self.api_key = api_key
        
        # Initialize Google GenAI client using the new SDK standard
        self.client = genai.Client(api_key=self.api_key)
        
        self.persona_matrix = VirtualGirlfriendPersonaMatrix(partner_name=partner_name)
        self.system_prompt = self.persona_matrix.build_master_system_prompt()
        
        # Generation hyper-parameters for human-like creative variation
        self.generation_config = {
            "temperature": 0.95,
            "top_p": 0.95,
            "top_k": 50,
            "max_output_tokens": 550,
        }
        
        # User session tracking maps
        self.active_sessions = {}

    def get_chat_response(self, user_id, user_message):
        """Processes incoming user text and fetches response via Google Gemini active session."""
        try:
            if user_id not in self.active_sessions:
                logger.info(f"Initializing new Gemini stateful session for user ID: {user_id}")
                # Create stateful chat session using the new client api with system instructions and config
                self.active_sessions[user_id] = self.client.chats.create(
                    model="gemini-2.5-flash",
                    config={
                        "system_instruction": self.system_prompt,
                        "temperature": self.generation_config["temperature"],
                        "top_p": self.generation_config["top_p"],
                        "top_k": self.generation_config["top_k"],
                        "max_output_tokens": self.generation_config["max_output_tokens"],
                    }
                )
            
            chat_session = self.active_sessions[user_id]
            logger.debug(f"Sending prompt to Gemini API for user {user_id}...")
            response = chat_session.send_message(user_message)
            
            logger.info(f"Successfully retrieved Gemini response for user ID: {user_id}")
            return response.text

        except Exception as api_error:
            logger.error(f"Critical exception inside GeminiChatBrain for user {user_id}: {api_error}")
            fallbacks = self.persona_matrix.get_emotional_fallback_phrases()
            import random
            return random.choice(fallbacks)
