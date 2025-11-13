import os
import asyncio
from polymarket import PolymarketFetcher
from discord import DiscordWebhook
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryBot:
    def __init__(self):
        self.poly_fetcher = PolymarketFetcher()
        self.discord = DiscordWebhook(os.getenv('DISCORD_WEBHOOK_URL'))
    
    async def find_stories(self):
        """Main pipeline to find and generate stories"""
        try:
            logger.info("Starting daily story scan...")
            
            # Get top traders
            traders = await self.poly_fetcher.get_top_traders(limit=50)
            
            # Get big markets
            markets = await self.poly_fetcher.get_active_markets()
            
            stories = []
            
            # Look for new whales (top traders with recent big gains)
            for trader in traders[:10]:  # Check top 10
                if self.is_interesting_trader(trader):
                    story = await self.generate_trader_story(trader)
                    if story:
                        stories.append(story)
            
            # Look for interesting market activity
            for market in markets:
                if self.is_interesting_market(market):
                    story = await self.generate_market_story(market)
                    if story:
                        stories.append(story)
            
            return stories[:3]  # Return top 3 stories max
            
        except Exception as e:
            logger.error(f"Error finding stories: {e}")
            return []
    
    def is_interesting_trader(self, trader):
        """Determine if a trader is story-worthy"""
        pnl = trader.get('pnl', 0)
        volume = trader.get('volume', 0)
        
        # Criteria for interesting trader
        return (pnl > 10000 or volume > 50000)  # $10k+ PNL or $50k+ volume
    
    def is_interesting_market(self, market):
        """Determine if a market is story-worthy"""
        volume = market.get('volume', 0)
        is_featured = market.get('featured', False)
        
        return volume > 100000 or is_featured  # $100k+ volume or featured
    
    async def generate_trader_story(self, trader):
        """Generate a story about an interesting trader"""
        username = trader.get('username', 'Anonymous')
        pnl = trader.get('pnl', 0)
        volume = trader.get('volume', 0)
        
        story = f"""🐋 **New Polymarket Whale Alert!** 🐋

Meet **{username}** - just entered the top traders with impressive stats:

• P&L: `${pnl:,.2f}`
• Volume: `${volume:,.2f}`
• Profile: https://polymarket.com/@{username}

This trader is making waves in prediction markets. Are they a savvy institutional player or a lucky retail trader?

#Polymarket #WhaleAlert #PredictionMarkets

*Generated at {self.get_current_time()}*"""
        
        return story
    
    async def generate_market_story(self, market):
        """Generate a story about an interesting market"""
        question = market.get('question', 'Unknown')
        volume = market.get('volume', 0)
        market_url = market.get('url', '')
        
        story = f"""📊 **Hot Market Alert!** 📊

Market: **{question}**

Trading volume: `${volume:,.2f}`

This market is seeing massive attention right now. Big money is moving - someone knows something?

Trade here: {market_url}

#Polymarket #Trading #MarketAlert

*Generated at {self.get_current_time()}*"""
        
        return story
    
    def get_current_time(self):
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    async def run(self):
        """Main execution function"""
        stories = await self.find_stories()
        
        if not stories:
            stories = [self.get_fallback_story()]
        
        for story in stories:
            await self.discord.send_message(story)
            await asyncio.sleep(1)  # Rate limiting
        
        logger.info(f"Sent {len(stories)} stories to Discord")
        return len(stories)
    
    def get_fallback_story(self):
        """Fallback story when no interesting activity found"""
        return """🔍 **Daily Polymarket Scan Complete**

No extraordinary whale activity detected today. 

The markets are relatively calm, but keep watching - big moves can happen anytime!

Check live markets: https://polymarket.com

#Polymarket #DailyUpdate #Trading

*Generated at {self.get_current_time()}*"""

async def main():
    bot = StoryBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
