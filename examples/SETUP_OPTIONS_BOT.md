# Setting Up an Options Bot with Lumibot 🚀

This repository contains comprehensive resources for setting up options trading bots using Lumibot.

## 📁 Quick Navigation

| File | Description | Best For |
|------|-------------|----------|
| **[options_bot_quickstart.py](options_bot_quickstart.py)** | Simple guide with code structure | Complete beginners |
| **[options_bot_guide.py](options_bot_guide.py)** | 6 complete strategy examples | Learning by example |
| **[OPTIONS_BOT_README.md](OPTIONS_BOT_README.md)** | Detailed documentation | In-depth understanding |

## 🎯 Choose Your Starting Point

### 1. **Total Beginner?** Start Here: 
```bash
python examples/options_bot_quickstart.py
```
This will show you:
- Basic structure of an options bot
- Key concepts explained simply  
- Template code to get started
- No dependencies needed to run

### 2. **Want Complete Examples?** Use:
```bash
python examples/options_bot_guide.py
```
This includes 6 ready-to-use strategies:
- ✅ BasicOptionsBot - Simple call option
- ✅ CoveredCallBot - Covered call strategy
- ✅ CreditSpreadBot - Bull put spread
- ✅ IronCondorBot - Iron condor with OptionsHelper
- ✅ BullCallSpreadBot - Bull call spread
- ✅ StraddleBot - Long straddle

### 3. **Need Detailed Docs?** Read:
[OPTIONS_BOT_README.md](OPTIONS_BOT_README.md) - Complete guide with:
- Setup instructions
- Strategy explanations
- Live trading configuration
- Backtesting setup
- Risk management tips

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Lumibot
```bash
pip install lumibot
```

### Step 2: Choose Your Strategy
Edit `options_bot_guide.py`:
```python
strategy_to_run = "basic"  # Options: basic, covered_call, credit_spread, iron_condor, bull_call, straddle
```

### Step 3: Run It
```bash
python examples/options_bot_guide.py
```

## 📚 Learning Path

### For Beginners
1. Run `options_bot_quickstart.py` to see the basic structure
2. Read the concepts guide it prints
3. Copy the template and modify for your needs

### For Intermediate Users
1. Study `options_bot_guide.py` examples
2. Read `OPTIONS_BOT_README.md` for detailed docs
3. Customize parameters for your strategy

### For Advanced Users
1. Review `lumibot/example_strategies/strangle.py`
2. Study `lumibot/components/options_helper.py`
3. Read `options_tutorial.md` for deep dive

## 🔑 Key Concepts

### Creating an Option Asset
```python
from lumibot.entities import Asset
from datetime import datetime, timedelta

option = Asset(
    symbol="SPY",
    asset_type="option",
    expiration=datetime.now() + timedelta(days=30),
    strike=450,
    right="call",  # or "put"
)
```

### Placing an Order
```python
order = self.create_order(option, quantity=1, side="buy")
self.submit_order(order)
```

### Using OptionsHelper (for complex strategies)
```python
from lumibot.components.options_helper import OptionsHelper

class MyStrategy(Strategy):
    def initialize(self):
        self.options_helper = OptionsHelper(self)
    
    def on_trading_iteration(self):
        # Execute iron condor with one line!
        self.options_helper.execute_iron_condor(...)
```

## 🏃 Running Examples

### Paper Trading (Recommended for Testing)
```python
from lumibot.brokers import InteractiveBrokers

config = {
    "SOCKET_PORT": 7497,  # Paper trading port
    "CLIENT_ID": 1,
}

broker = InteractiveBrokers(config)
strategy = BasicOptionsBot(broker=broker)
strategy.run_live()
```

### Backtesting
```python
from lumibot.backtesting import PolygonDataBacktesting
from datetime import datetime

results = BasicOptionsBot.backtest(
    PolygonDataBacktesting,
    datetime(2024, 1, 1),
    datetime(2024, 1, 31),
    polygon_api_key="YOUR_KEY",
)
```

## 📊 Available Strategies

### 1. Basic Options (BasicOptionsBot)
- **What**: Buys a simple call option
- **Risk**: Limited to premium paid
- **Use**: Learning the basics

### 2. Covered Call (CoveredCallBot)  
- **What**: Own stock + sell call
- **Risk**: Limited upside
- **Use**: Generate income on holdings

### 3. Credit Spread (CreditSpreadBot)
- **What**: Sell put + buy lower put
- **Risk**: Limited to spread width
- **Use**: Bullish with limited risk

### 4. Iron Condor (IronCondorBot)
- **What**: Call spread + put spread
- **Risk**: Limited to wing width
- **Use**: Range-bound markets

### 5. Bull Call Spread (BullCallSpreadBot)
- **What**: Buy call + sell higher call
- **Risk**: Limited to premium
- **Use**: Moderately bullish

### 6. Straddle (StraddleBot)
- **What**: Buy call + put at same strike
- **Risk**: Limited to total premium
- **Use**: Expecting big move

## 🎓 Additional Resources

### Documentation
- [Lumibot Docs](http://lumibot.lumiwealth.com/) - Official documentation
- [options_tutorial.md](../options_tutorial.md) - In-depth options tutorial
- [Lumibot Blog](https://lumiwealth.com/blog/) - Tutorials and guides

### Example Strategies (in repository)
- `lumibot/example_strategies/strangle.py` - Complete strangle strategy
- `lumibot/example_strategies/options_hold_to_expiry.py` - Buy and hold example

### Data Providers
- [Polygon.io](https://polygon.io) - Recommended (use code 'LUMI10' for 10% off)
- Free tier available for testing

### Brokers
- **Interactive Brokers** - Full options support
- **Alpaca** - Good for stocks and some options
- **Tradier** - Options trading available

## ⚠️ Important Notes

### Before Trading Live
1. ✅ Test with paper trading first
2. ✅ Understand the max loss of each strategy
3. ✅ Start with small position sizes
4. ✅ Use stop losses
5. ✅ Never risk more than you can afford to lose

### Options Risks
- Options can expire worthless
- Time decay (theta) works against buyers
- Volatility can change quickly
- Spreads have limited profit potential
- Multi-leg orders may have partial fills

### Best Practices
- Monitor Greeks (delta, gamma, theta, vega)
- Close positions before expiration if needed
- Use limit orders for better fills
- Keep track of all positions
- Set up alerts for important price levels

## 🤝 Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/Lumiwealth/lumibot/issues)
- **Documentation**: [lumibot.lumiwealth.com](http://lumibot.lumiwealth.com/)
- **Community**: Join the Lumiwealth Discord
- **Blog**: [lumiwealth.com/blog](https://lumiwealth.com/blog/)

## 📝 File Structure

```
examples/
├── options_bot_quickstart.py    # Simple guide for beginners
├── options_bot_guide.py          # 6 complete strategy examples
├── OPTIONS_BOT_README.md         # Detailed documentation
└── SETUP_OPTIONS_BOT.md          # This file

lumibot/example_strategies/
├── strangle.py                   # Complete strangle implementation
└── options_hold_to_expiry.py     # Simple buy and hold

tests/
└── test_options_bot_guide.py     # Unit tests for examples

Root files:
└── options_tutorial.md           # In-depth tutorial
```

## 🚀 Next Steps

1. **Run the quickstart**: `python examples/options_bot_quickstart.py`
2. **Study an example**: Open `options_bot_guide.py` and read BasicOptionsBot
3. **Read the docs**: Open `OPTIONS_BOT_README.md` for detailed guide
4. **Customize**: Modify parameters to match your strategy
5. **Test**: Always test with paper trading first
6. **Learn more**: Review `options_tutorial.md` for deep understanding

## 💡 Pro Tips

1. **Start Simple**: Begin with BasicOptionsBot to understand the flow
2. **Paper Trade**: Test thoroughly before using real money
3. **Use OptionsHelper**: For complex strategies, it handles the details
4. **Monitor Positions**: Options require active management
5. **Learn Greeks**: Understanding delta, theta, vega is crucial
6. **Keep Learning**: Options trading is complex - continuous education helps

---

**Happy Trading! 📈🚀**

*Remember: Options trading involves significant risk. This code is for educational purposes. Always do your own research and consider consulting with a financial advisor.*
