# Options Bot Guide for Lumibot

This guide provides comprehensive examples for setting up and running options trading bots using the Lumibot library.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Available Strategies](#available-strategies)
3. [Basic Concepts](#basic-concepts)
4. [Running the Examples](#running-the-examples)
5. [Live Trading Setup](#live-trading-setup)
6. [Backtesting Setup](#backtesting-setup)

## 🚀 Getting Started

### Prerequisites

```bash
pip install lumibot
```

For backtesting, you'll also need a data provider. We recommend [Polygon.io](https://polygon.io):

```bash
pip install polygon-api-client
```

### Quick Start

Run the options bot guide:

```bash
python examples/options_bot_guide.py
```

## 📊 Available Strategies

The guide includes 6 complete strategy examples:

### 1. **BasicOptionsBot** - Simple Call Option Purchase
- Buys a single call option
- Good for: Learning the basics
- Risk: Limited to premium paid

### 2. **CoveredCallBot** - Covered Call Strategy
- Buys stock + Sells call option
- Good for: Generating income on stock holdings
- Risk: Limited upside potential

### 3. **CreditSpreadBot** - Bull Put Credit Spread
- Sells put + Buys lower put
- Good for: Neutral to bullish outlook
- Risk: Limited to spread width minus premium

### 4. **IronCondorBot** - Iron Condor with OptionsHelper
- Combines call spread + put spread
- Good for: Low volatility, range-bound stocks
- Risk: Limited to wing width

### 5. **BullCallSpreadBot** - Bull Call Spread with OptionsHelper
- Buys call + Sells higher call
- Good for: Moderately bullish outlook
- Risk: Limited to premium paid (spread)

### 6. **StraddleBot** - Long Straddle with OptionsHelper
- Buys call + put at same strike
- Good for: Expecting large price movement
- Risk: Limited to total premium paid

## 📚 Basic Concepts

### Creating an Option Asset

```python
from lumibot.entities import Asset
from datetime import datetime, timedelta

# Define expiration (30 days from now)
expiry = datetime.now() + timedelta(days=30)

# Create a call option
option = Asset(
    symbol="SPY",
    asset_type="option",
    expiration=expiry,
    strike=450,
    right="call",  # or "put"
)
```

### Creating and Submitting Orders

```python
# Create an order
order = self.create_order(
    asset=option,
    quantity=1,
    side="buy"  # or "sell"
)

# Submit the order
self.submit_order(order)
```

### Using OptionsHelper for Complex Strategies

The `OptionsHelper` component simplifies multi-leg option strategies:

```python
from lumibot.components.options_helper import OptionsHelper

class MyStrategy(Strategy):
    def initialize(self):
        self.options_helper = OptionsHelper(self)
    
    def on_trading_iteration(self):
        # Execute a vertical spread
        success = self.options_helper.execute_vertical_spread(
            underlying_asset=underlying,
            expiry=expiry,
            upper_strike=455,
            lower_strike=450,
            quantity=1,
            limit_type="mid"  # Use mid-point pricing
        )
```

## 🏃 Running the Examples

### Choose a Strategy

Edit the `strategy_to_run` variable in `options_bot_guide.py`:

```python
strategy_to_run = "basic"  # Options: basic, covered_call, credit_spread, 
                           #          iron_condor, bull_call, straddle
```

### Run the Script

```bash
python examples/options_bot_guide.py
```

## 💼 Live Trading Setup

### Step 1: Install Broker Package

For Interactive Brokers:
```bash
pip install ib_insync
```

For Alpaca:
```bash
pip install alpaca-trade-api
```

### Step 2: Configure Broker Credentials

Create a `credentials.py` file:

```python
# For Interactive Brokers
INTERACTIVE_BROKERS_CONFIG = {
    "SOCKET_PORT": 7497,  # 7496 for live, 7497 for paper
    "CLIENT_ID": 1,
}

# For Alpaca
ALPACA_CONFIG = {
    "API_KEY": "your_api_key",
    "API_SECRET": "your_api_secret",
    "PAPER": True,  # Set to False for live trading
}
```

### Step 3: Update the Script

```python
from lumibot.brokers import InteractiveBrokers
from credentials import INTERACTIVE_BROKERS_CONFIG

# Create broker connection
broker = InteractiveBrokers(INTERACTIVE_BROKERS_CONFIG)

# Create strategy with broker
strategy = BasicOptionsBot(broker=broker)

# Run live
strategy.run_live()
```

## 📈 Backtesting Setup

### Step 1: Get Polygon.io API Key

1. Sign up at [Polygon.io](https://polygon.io)
2. Get your API key from the dashboard
3. Use coupon code 'LUMI10' for 10% off

### Step 2: Run Backtest

```python
from lumibot.backtesting import PolygonDataBacktesting
from datetime import datetime

# Define backtest period
backtesting_start = datetime(2024, 1, 1)
backtesting_end = datetime(2024, 1, 31)

# Run backtest
results = BasicOptionsBot.backtest(
    PolygonDataBacktesting,
    backtesting_start,
    backtesting_end,
    benchmark_asset="SPY",
    polygon_api_key="YOUR_POLYGON_API_KEY",
)
```

## 🎯 Strategy Parameters

Each strategy has configurable parameters:

### BasicOptionsBot Parameters
- `symbol`: Stock ticker (default: "SPY")
- `quantity`: Number of contracts (default: 1)
- `days_to_expiry`: Days until option expiration (default: 30)

### CoveredCallBot Parameters
- `symbol`: Stock ticker (default: "AAPL")
- `num_shares`: Number of shares to buy (default: 100)
- `strike_offset`: Strike above current price (default: 5)
- `days_to_expiry`: Days until expiration (default: 30)

### IronCondorBot Parameters
- `symbol`: Stock ticker (default: "SPY")
- `wing_width`: Width of each spread (default: 5)
- `distance_from_price`: Distance to sold strikes (default: 10)
- `days_to_expiry`: Days until expiration (default: 30)
- `contracts`: Number of contracts (default: 1)

## 📖 Additional Resources

### Lumibot Documentation
- Main Docs: http://lumibot.lumiwealth.com/
- Options Tutorial: See `options_tutorial.md` in the repository

### Example Strategies
- More examples in `lumibot/example_strategies/`
- Strangle strategy: `lumibot/example_strategies/strangle.py`
- Options hold to expiry: `lumibot/example_strategies/options_hold_to_expiry.py`

### Blog & Tutorials
- Lumibot Blog: https://lumiwealth.com/blog/
- Video Tutorials: Check the Lumiwealth YouTube channel

## ⚠️ Important Notes

### Risk Management
- Options trading involves significant risk
- Start with paper trading before going live
- Never risk more than you can afford to lose
- Use stop losses and position sizing

### Data Requirements
- Options backtesting requires historical options data
- Polygon.io is recommended (free tier available)
- Some strategies may not be fully backtestable

### Broker Compatibility
- Not all brokers support all option strategies
- Check with your broker for supported order types
- Multi-leg orders may have specific requirements

## 🤝 Contributing

Want to add more strategy examples? See the main [CONTRIBUTING.md](../CONTRIBUTING.md) guide.

## 📝 License

This code is part of the Lumibot library and follows the same license.

## 💡 Tips for Success

1. **Start Simple**: Begin with BasicOptionsBot to understand the fundamentals
2. **Paper Trade First**: Always test strategies in paper trading mode
3. **Understand Greeks**: Learn about delta, gamma, theta, and vega
4. **Monitor Positions**: Options require active management
5. **Use OptionsHelper**: For complex strategies, leverage the OptionsHelper component
6. **Set Alerts**: Monitor your positions and set up alerts for important events
7. **Keep Learning**: Options are complex - continuous education is key

## 🆘 Getting Help

- GitHub Issues: https://github.com/Lumiwealth/lumibot/issues
- Documentation: http://lumibot.lumiwealth.com/
- Discord Community: Join the Lumiwealth Discord server

---

**Happy Trading! 📈🚀**
