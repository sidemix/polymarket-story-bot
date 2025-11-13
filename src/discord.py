import aiohttp
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DiscordWebhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_message(self, content: str, username: str = "Polymarket Bot") -> bool:
        """Send message to Discord webhook"""
        if not self.webhook_url:
            logger.error("No Discord webhook URL provided")
            return False
        
        payload = {
            "content": content,
            "username": username,
            "avatar_url": "https://polymarket.com/favicon.ico"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info("Message sent to Discord successfully")
                        return True
                    else:
                        logger.error(f"Failed to send message: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Error sending to Discord: {e}")
            return False
