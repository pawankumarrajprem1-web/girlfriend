# ==============================================================================
# FILE NAME: config.py
# DESCRIPTION: Advanced Central Configuration & Security Vault Management Module
# ==============================================================================
import os
import sys
import logging
import json

# Configure robust system-wide logging mechanism
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ConfigVault")

class CoreSystemConfiguration:
    """
    Centralized configuration repository handling secure environment variables,
    API endpoints, model hyper-parameters, and persistent state schemas.
    """
    def __init__(self):
        logger.info("Initializing CoreSystemConfiguration vault...")
        
        # Core API Credentials with fallback placeholders
        self.TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
        self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
        self.STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY", "YOUR_STABILITY_API_KEY_HERE")
        self.ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY_HERE")
        
        # Bot Personality Parameters
        self.GIRLFRIEND_NAME = "Ananya"
        self.PORT = int(os.environ.get("PORT", 5000))
        self.ACTIVE_AI_ENGINE = os.environ.get("ACTIVE_AI_ENGINE", "openai") # Options: 'openai', 'gemini'
        
        # Validate critical credentials at startup
        self._validate_configurations()

    def _validate_configurations(self):
        """Performs rigorous security and availability checks on incoming environment variables."""
        missing_keys = []
        if self.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            missing_key_name = "TELEGRAM_BOT_TOKEN"
            missing_keys.append(missing_key_name)
        if self.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
            missing_keys.append("OPENAI_API_KEY")
        if self.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            missing_keys.append("GEMINI_API_KEY")
            
        if missing_keys:
            logger.warning(f"Configuration Warning: The following primary tokens are using default placeholders: {missing_keys}")
        else:
            logger.info("All primary security tokens successfully loaded into the config vault.")

    def export_summary(self):
        """Exports a masked configuration overview for debugging purposes."""
        return {
            "bot_name": self.GIRLFRIEND_NAME,
            "port": self.PORT,
            "active_engine": self.ACTIVE_AI_ENGINE,
            "token_status": "Loaded Securely via Environment Vault"
        }
