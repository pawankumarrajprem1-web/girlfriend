# ==============================================================================
# FILE NAME: config.py
# DESCRIPTION: Free & Secure Central Configuration Vault
# ==============================================================================
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ConfigVault")

class CoreSystemConfiguration:
    def __init__(self):
        logger.info("Initializing CoreSystemConfiguration vault...")
        
        self.TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
        self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
        
        self.GIRLFRIEND_NAME = "Ananya"
        self.PORT = int(os.environ.get("PORT", 5000))
        self.ACTIVE_AI_ENGINE = "gemini"

    def export_summary(self):
        return {
            "bot_name": self.GIRLFRIEND_NAME,
            "port": self.PORT,
            "active_engine": self.ACTIVE_AI_ENGINE,
            "status": "Running 100% Free & Credit-Free Mode"
        }
