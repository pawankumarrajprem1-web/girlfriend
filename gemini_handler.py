# ==============================================================================
# FILE NAME: gemini_handler.py
# DESCRIPTION: High-Performance Google Gemini Neural Processing Module
# ==============================================================================
import logging
import google.generativeai as genai
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
        genai.configure(api_key=self.api_key)
        
        self.persona_matrix = VirtualGirlfriendPersonaMatrix(partner_name=partner_name)
        self.system_prompt = self.persona_matrix.build_master_system_prompt()
        
        # Generation hyper-parameters for human-like creative variation
        self.generation_config = {
            "temperature": 0.95,
            "top_p": 0.95,
            "top_k": 50,
            "max_output_tokens": 550,
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction=self.system_prompt
        )
        
        # User session tracking maps
        self.active_sessions = {}

    def get_chat_response(self, user_id, user_message):
        """Processes incoming user text and fetches response via Google Gemini active session."""
        try:
            if user_id not in self.active_sessions:
                logger.info(f"Initializing new Gemini stateful session for user ID: {user_id}")
                self.active_sessions[user_id] = self.model.start_chat(history=[])
            
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
