#!/usr/bin/env python
"""
Quick Start Options Bot - Minimal Example

This is a minimal, standalone example showing how to set up an options bot.
It's designed to be simple and easy to understand for beginners.

No external dependencies are needed to read and understand the code structure.
"""

# Step 1: Define what you need for options trading
# ================================================

EXAMPLE_BROKER_CONFIG = {
    # For Interactive Brokers (paper trading)
    "ib": {
        "SOCKET_PORT": 7497,  # 7496 for live, 7497 for paper
        "CLIENT_ID": 1,
    },
    
    # For Alpaca (paper trading) 
    "alpaca": {
        "API_KEY": "your_api_key_here",
        "API_SECRET": "your_api_secret_here",
        "PAPER": True,
    }
}


# Step 2: Simple Options Bot Class Structure
# ==========================================

class SimpleOptionsBot:
    """
    A minimal options bot template.
    
    This shows the basic structure needed for an options trading bot:
    1. Initialize parameters
    2. Create option assets
    3. Place orders
    """
    
    def __init__(self, broker=None):
        """Initialize the bot with a broker connection"""
        self.broker = broker
        self.symbol = "SPY"
        self.quantity = 1
        self.days_to_expiry = 30
        
    def initialize(self):
        """Set up the bot (called once at start)"""
        print(f"Initializing Options Bot for {self.symbol}")
        self.sleeptime = "1D"  # Run once per day
        
    def create_option_asset(self, symbol, strike, expiration, right="call"):
        """
        Create an option asset.
        
        Args:
            symbol: Stock ticker (e.g., "SPY")
            strike: Option strike price (e.g., 450)
            expiration: Expiration date
            right: "call" or "put"
        
        Returns:
            Option asset object (would be Asset object in real implementation)
        """
        return {
            "symbol": symbol,
            "asset_type": "option",
            "strike": strike,
            "expiration": expiration,
            "right": right,
        }
    
    def create_order(self, asset, quantity, side):
        """
        Create an order.
        
        Args:
            asset: The asset to trade
            quantity: Number of contracts
            side: "buy" or "sell"
        
        Returns:
            Order object (would be Order object in real implementation)
        """
        return {
            "asset": asset,
            "quantity": quantity,
            "side": side,
        }
    
    def on_trading_iteration(self):
        """
        Main trading logic (called each iteration).
        
        This is where you put your trading strategy.
        """
        # Get current stock price (in real implementation)
        current_price = 450.0  # Would use: self.get_last_price(self.symbol)
        
        # Calculate strike and expiration
        strike = round(current_price)
        
        # In real implementation, would calculate expiration date
        from datetime import datetime, timedelta
        expiration = datetime.now() + timedelta(days=self.days_to_expiry)
        
        # Create call option
        option = self.create_option_asset(
            symbol=self.symbol,
            strike=strike,
            expiration=expiration,
            right="call"
        )
        
        # Create buy order
        order = self.create_order(
            asset=option,
            quantity=self.quantity,
            side="buy"
        )
        
        # Submit order (in real implementation)
        print(f"Would buy {self.quantity} {self.symbol} ${strike} call option")
        print(f"Order details: {order}")


# Step 3: Real Implementation Template
# ====================================

REAL_IMPLEMENTATION_TEMPLATE = '''
# To create a real options bot, use this template:

from lumibot.strategies import Strategy
from lumibot.entities import Asset
from datetime import datetime, timedelta

class MyOptionsBot(Strategy):
    """Your custom options bot"""
    
    parameters = {
        "symbol": "SPY",
        "quantity": 1,
        "days_to_expiry": 30,
    }
    
    def initialize(self):
        """Initialize the strategy"""
        self.sleeptime = "1D"
    
    def on_trading_iteration(self):
        """Main trading logic"""
        # 1. Get parameters
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        days_to_expiry = self.parameters["days_to_expiry"]
        
        # 2. Get current price
        current_price = self.get_last_price(symbol)
        
        # 3. Calculate strike and expiration
        strike = round(current_price)
        expiration = datetime.now() + timedelta(days=days_to_expiry)
        
        # 4. Create option asset
        option = Asset(
            symbol=symbol,
            asset_type="option",
            expiration=expiration,
            strike=strike,
            right="call",
        )
        
        # 5. Create and submit order
        order = self.create_order(option, quantity, "buy")
        self.submit_order(order)
        
        self.log_message(f"Bought {quantity} {symbol} ${strike} call")

# To run with a broker:
if __name__ == "__main__":
    from lumibot.brokers import InteractiveBrokers
    
    # Configure broker
    config = {
        "SOCKET_PORT": 7497,  # Paper trading
        "CLIENT_ID": 1,
    }
    
    broker = InteractiveBrokers(config)
    strategy = MyOptionsBot(broker=broker)
    strategy.run_live()
'''


# Step 4: Key Concepts Guide
# ==========================

CONCEPTS_GUIDE = """
KEY CONCEPTS FOR OPTIONS BOTS
==============================

1. OPTION ASSET CREATION
   - symbol: Stock ticker (e.g., "SPY", "AAPL")
   - asset_type: Always "option" for options
   - expiration: Date when option expires
   - strike: Strike price
   - right: "call" or "put"

2. COMMON STRATEGIES
   
   a) Buy Call (Bullish):
      - Buy 1 call option
      - Profit if stock rises above strike + premium
   
   b) Covered Call (Income):
      - Own 100 shares
      - Sell 1 call option
      - Collect premium, limit upside
   
   c) Bull Put Spread (Bullish):
      - Sell put at higher strike (collect premium)
      - Buy put at lower strike (limit risk)
      - Profit if stock stays above sold put
   
   d) Iron Condor (Neutral):
      - Sell call spread above current price
      - Sell put spread below current price
      - Profit if stock stays in range
   
   e) Straddle (Volatility):
      - Buy call and put at same strike
      - Profit from large moves either direction

3. USING OPTIONS HELPER
   
   from lumibot.components.options_helper import OptionsHelper
   
   def initialize(self):
       self.options_helper = OptionsHelper(self)
   
   # Execute complex strategies easily:
   self.options_helper.execute_vertical_spread(...)
   self.options_helper.execute_iron_condor(...)
   self.options_helper.execute_straddle(...)

4. BROKER SETUP
   
   Interactive Brokers:
   - Install TWS or IB Gateway
   - Enable API connections
   - Use port 7497 for paper, 7496 for live
   
   Alpaca:
   - Get API keys from alpaca.markets
   - Set PAPER=True for paper trading
   
5. BACKTESTING
   
   # Requires Polygon.io API key
   from lumibot.backtesting import PolygonDataBacktesting
   
   results = MyOptionsBot.backtest(
       PolygonDataBacktesting,
       backtesting_start,
       backtesting_end,
       polygon_api_key="YOUR_KEY",
   )

6. RISK MANAGEMENT
   
   - Start with paper trading
   - Use position sizing (don't risk too much)
   - Understand max loss before entering
   - Monitor Greeks (delta, gamma, theta, vega)
   - Set stop losses
   - Close positions before expiration if needed

7. RESOURCES
   
   - Full guide: examples/OPTIONS_BOT_README.md
   - Complete examples: examples/options_bot_guide.py
   - Original tutorial: options_tutorial.md
   - Documentation: lumibot.lumiwealth.com
   - Example strategies: lumibot/example_strategies/
"""


# Step 5: Print Guide
# ===================

if __name__ == "__main__":
    print("=" * 70)
    print("LUMIBOT OPTIONS BOT - QUICK START GUIDE")
    print("=" * 70)
    print()
    
    print("This file shows the basic structure of an options bot.")
    print()
    
    print("STEP 1: Understand the Basic Structure")
    print("-" * 70)
    bot = SimpleOptionsBot()
    bot.initialize()
    print()
    
    print("STEP 2: See the Trading Logic")
    print("-" * 70)
    bot.on_trading_iteration()
    print()
    
    print("STEP 3: Review Key Concepts")
    print("-" * 70)
    print(CONCEPTS_GUIDE)
    print()
    
    print("STEP 4: Use the Real Implementation Template")
    print("-" * 70)
    print(REAL_IMPLEMENTATION_TEMPLATE)
    print()
    
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Read examples/OPTIONS_BOT_README.md for detailed guide")
    print("2. Check examples/options_bot_guide.py for 6 complete strategies")
    print("3. Review options_tutorial.md for in-depth tutorial")
    print("4. Join the community for support")
    print()
    print("Happy Trading! 📈")
    print("=" * 70)
