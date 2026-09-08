# ==============================================================================
# FILE NAME: openai_handler.py
# DESCRIPTION: Enterprise-Grade OpenAI ChatGPT Neural Processing Module
# ==============================================================================
import logging
from openai import OpenAI
from persona_engine import VirtualGirlfriendPersonaMatrix

logger = logging.getLogger("OpenAIEngine")

class OpenAIChatBrain:
    """
    Handles context retention, session history management, and token optimization
    using OpenAI's high-intelligence conversational endpoints.
    """
    def __init__(self, api_key, partner_name="Ananya"):
        logger.info("Initializing OpenAIChatBrain subsystem...")
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.persona_matrix = VirtualGirlfriendPersonaMatrix(partner_name=partner_name)
        self.system_prompt = self.persona_matrix.build_master_system_prompt()
        
        # User session history tracking dictionary
        self.chat_histories = {}

    def get_chat_response(self, user_id, user_message):
        """Processes incoming user text and fetches high-empathy neural responses from OpenAI."""
        try:
            if user_id not in self.chat_histories:
                logger.info(f"Creating new OpenAI conversational history context for user ID: {user_id}")
                self.chat_histories[user_id] = [
                    {"role": "system", "content": self.system_prompt}
                ]
            
            # Append user utterance to active context window
            self.chat_histories[user_id].append({"role": "user", "content": user_message})
            
            # Trim history length if it grows too large to optimize token limits
            if len(self.chat_histories[user_id]) > 25:
                # Keep system prompt index 0 and last 24 entries
                self.chat_histories[user_id] = [self.chat_histories[user_id][0]] + self.chat_histories[user_id][-24:]

            logger.debug(f"Dispatching API request to OpenAI for user {user_id}...")
            completion_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.chat_histories[user_id],
                temperature=0.92,
                max_tokens=550,
                presence_penalty=0.6,
                frequency_penalty=0.5
            )
            
            assistant_reply = completion_response.choices[0].message.content
            
            # Append assistant response to history
            self.chat_histories[user_id].append({"role": "assistant", "content": assistant_reply})
            logger.info(f"Successfully retrieved OpenAI response for user ID: {user_id}")
            return assistant_reply

        except Exception as api_error:
            logger.error(f"Critical exception inside OpenAIChatBrain for user {user_id}: {api_error}")
            fallbacks = self.persona_matrix.get_emotional_fallback_phrases()
            import random
            return random.choice(fallbacks)
