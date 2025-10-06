# 🚀 Start Here: Options Bot Setup Guide

**Welcome!** This guide will help you set up an options trading bot using Lumibot.

## 📍 Choose Your Path

### 🔰 Complete Beginner? 
**→ Start with:** [`options_bot_quickstart.py`](options_bot_quickstart.py)

Run this first:
```bash
python examples/options_bot_quickstart.py
```

This will:
- Show you the basic structure of an options bot
- Explain key concepts in simple terms
- Provide a template you can copy and modify
- No dependencies needed - runs immediately!

### 📚 Want to Learn by Example?
**→ Use:** [`options_bot_guide.py`](options_bot_guide.py)

This file contains **6 complete, ready-to-use strategies**:

| Strategy | What It Does | Good For |
|----------|-------------|----------|
| **BasicOptionsBot** | Buys a simple call option | Learning basics |
| **CoveredCallBot** | Owns stock + sells call | Generating income |
| **CreditSpreadBot** | Bull put spread | Limited risk bullish play |
| **IronCondorBot** | Neutral range strategy | Low volatility markets |
| **BullCallSpreadBot** | Bullish spread | Moderate bullish outlook |
| **StraddleBot** | Volatility play | Expecting big moves |

Each strategy is complete and can run independently!

### 📖 Need Full Documentation?
**→ Read:** [`OPTIONS_BOT_README.md`](OPTIONS_BOT_README.md)

Comprehensive guide including:
- ✅ Setup instructions (step-by-step)
- ✅ Strategy explanations with risk profiles
- ✅ Live trading configuration
- ✅ Backtesting setup
- ✅ Tips for success

### 🗺️ Want Overview?
**→ See:** [`SETUP_OPTIONS_BOT.md`](SETUP_OPTIONS_BOT.md)

Navigation guide with:
- Quick start (5 minutes)
- Learning paths
- File structure
- Resources

## ⚡ Quick Start (Under 5 Minutes)

### 1. Install Lumibot
```bash
pip install lumibot
```

### 2. Run the Quickstart
```bash
python examples/options_bot_quickstart.py
```

### 3. Study an Example
Open `options_bot_guide.py` and read the `BasicOptionsBot` class.

### 4. Try It!
Modify the parameters in `options_bot_guide.py`:
```python
strategy_to_run = "basic"  # Choose your strategy
```

Then run:
```bash
python examples/options_bot_guide.py
```

## 📊 What You'll Learn

### Core Concepts
- ✅ Creating option assets
- ✅ Placing option orders
- ✅ Using OptionsHelper for complex strategies
- ✅ Managing risk
- ✅ Backtesting strategies

### Strategies Covered
- ✅ Single options (calls/puts)
- ✅ Covered calls
- ✅ Credit/debit spreads
- ✅ Iron condors
- ✅ Straddles/strangles
- ✅ And more!

## 🎯 Recommended Learning Order

1. **Day 1**: Run `options_bot_quickstart.py` and read the output
2. **Day 2**: Study `BasicOptionsBot` in `options_bot_guide.py`
3. **Day 3**: Read `OPTIONS_BOT_README.md` thoroughly
4. **Day 4**: Try modifying parameters in `options_bot_guide.py`
5. **Day 5**: Set up paper trading with your broker
6. **Week 2**: Study more complex strategies (Iron Condor, Straddle)
7. **Week 3**: Backtest strategies
8. **Week 4+**: Start paper trading your custom strategy

## ⚠️ Important Reminders

1. **Always start with paper trading**
2. **Understand the max loss before entering any trade**
3. **Options can expire worthless**
4. **Use position sizing - don't risk too much**
5. **Learn about Greeks (delta, theta, gamma, vega)**

## 🆘 Need Help?

- **Questions?** Check the [OPTIONS_BOT_README.md](OPTIONS_BOT_README.md)
- **Bugs?** [Report on GitHub](https://github.com/Lumiwealth/lumibot/issues)
- **Docs?** [lumibot.lumiwealth.com](http://lumibot.lumiwealth.com/)
- **Community?** Join Lumiwealth Discord

## 📁 All Files

| File | Lines | Purpose |
|------|-------|---------|
| `options_bot_quickstart.py` | 333 | Beginner-friendly guide |
| `options_bot_guide.py` | 495 | 6 complete strategies |
| `OPTIONS_BOT_README.md` | 303 | Full documentation |
| `SETUP_OPTIONS_BOT.md` | 268 | Navigation guide |
| `OPTIONS_BOT_START_HERE.md` | This file | Quick start |

## 🚀 Your First Bot in 3 Steps

### Step 1: Copy This Template
```python
from lumibot.strategies import Strategy
from lumibot.entities import Asset
from datetime import datetime, timedelta

class MyFirstOptionsBot(Strategy):
    parameters = {
        "symbol": "SPY",
        "quantity": 1,
    }
    
    def initialize(self):
        self.sleeptime = "1D"
    
    def on_trading_iteration(self):
        # Get current price
        price = self.get_last_price(self.parameters["symbol"])
        
        # Create option
        option = Asset(
            symbol=self.parameters["symbol"],
            asset_type="option",
            expiration=datetime.now() + timedelta(days=30),
            strike=round(price),
            right="call",
        )
        
        # Buy it
        order = self.create_order(option, self.parameters["quantity"], "buy")
        self.submit_order(order)
```

### Step 2: Set Up Broker (Paper Trading)
```python
from lumibot.brokers import InteractiveBrokers

config = {
    "SOCKET_PORT": 7497,  # Paper trading
    "CLIENT_ID": 1,
}

broker = InteractiveBrokers(config)
strategy = MyFirstOptionsBot(broker=broker)
```

### Step 3: Run It!
```python
strategy.run_live()
```

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Understand options bot structure
- ✅ Run complete example strategies
- ✅ Customize for your needs
- ✅ Test with paper trading
- ✅ Deploy your own strategies

**Happy Trading! 📈🚀**

---

*Start with [`options_bot_quickstart.py`](options_bot_quickstart.py) - it's the easiest way to begin!*
