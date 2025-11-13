import aiohttp
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class PolymarketFetcher:
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
    
    async def get_top_traders(self, limit: int = 50) -> List[Dict]:
        """Fetch top traders from Polymarket leaderboard"""
        try:
            url = f"{self.base_url}/leaderboard"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('leaderboard', [])[:limit]
                    else:
                        logger.error(f"Failed to fetch traders: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching traders: {e}")
            return []
    
    async def get_active_markets(self, limit: int = 20) -> List[Dict]:
        """Fetch active markets with high volume"""
        try:
            url = f"{self.base_url}/markets"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        markets = data.get('markets', [])
                        
                        # Filter active markets and sort by volume
                        active_markets = [m for m in markets if m.get('active', False)]
                        active_markets.sort(key=lambda x: x.get('volume', 0), reverse=True)
                        
                        return active_markets[:limit]
                    else:
                        logger.error(f"Failed to fetch markets: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []
    
    async def get_big_trades(self, min_amount: float = 1000) -> List[Dict]:
        """Fetch recent large trades (mock - would need real API)"""
        # This would require websocket or specific trade API
        # For now, return mock data
        return [
            {
                "user": "BigTrader123",
                "amount": 5000,
                "market": "Will BTC hit $100k?",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        ]
