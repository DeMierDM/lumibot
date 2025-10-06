"""
Options Bot Guide for Lumibot

This comprehensive guide demonstrates how to set up and run various options trading strategies
using the Lumibot library. It includes examples of:

1. Basic Options Trading (single option buy/sell)
2. Covered Call Strategy
3. Credit Spread Strategy
4. Iron Condor Strategy using OptionsHelper
5. Bull Call Spread using OptionsHelper
6. Straddle Strategy using OptionsHelper

Each strategy is self-contained and can be run independently.
"""

from datetime import datetime, timedelta
from lumibot.strategies.strategy import Strategy
from lumibot.entities import Asset
from lumibot.components.options_helper import OptionsHelper


# ============================================================================
# EXAMPLE 1: Basic Options Trading
# ============================================================================

class BasicOptionsBot(Strategy):
    """
    A simple options bot that buys a call option and holds it.
    
    This demonstrates the basic workflow:
    1. Create an option asset
    2. Create an order
    3. Submit the order
    """
    
    parameters = {
        "symbol": "SPY",
        "quantity": 1,
        "days_to_expiry": 30,
    }

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        days_to_expiry = self.parameters["days_to_expiry"]
        
        # Get current price of underlying
        underlying_price = self.get_last_price(symbol)
        self.log_message(f"Current price of {symbol}: ${underlying_price}")
        
        # Only trade on first iteration
        if self.first_iteration:
            # Calculate expiration date (30 days from now)
            expiry = datetime.now() + timedelta(days=days_to_expiry)
            
            # Round strike to nearest dollar
            strike = round(underlying_price)
            
            # Create call option asset
            option_asset = Asset(
                symbol=symbol,
                asset_type="option",
                expiration=expiry,
                strike=strike,
                right="call",
            )
            
            # Create and submit buy order
            order = self.create_order(option_asset, quantity, "buy")
            self.submit_order(order)
            
            self.log_message(
                f"Bought {quantity} {symbol} ${strike} call option expiring {expiry.date()}"
            )


# ============================================================================
# EXAMPLE 2: Covered Call Strategy
# ============================================================================

class CoveredCallBot(Strategy):
    """
    Covered Call Strategy:
    - Buy 100 shares of stock
    - Sell 1 call option (at strike above current price)
    
    This generates income from the option premium while holding the stock.
    """
    
    parameters = {
        "symbol": "AAPL",
        "num_shares": 100,
        "strike_offset": 5,  # Strike will be current_price + 5
        "days_to_expiry": 30,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.covered_call_active = False

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        num_shares = self.parameters["num_shares"]
        strike_offset = self.parameters["strike_offset"]
        days_to_expiry = self.parameters["days_to_expiry"]
        
        # Get current price
        current_price = self.get_last_price(symbol)
        
        # Only execute on first iteration
        if self.first_iteration and not self.covered_call_active:
            # Step 1: Buy the stock
            stock_asset = Asset(symbol=symbol, asset_type="stock")
            stock_order = self.create_order(stock_asset, num_shares, "buy")
            self.submit_order(stock_order)
            
            self.log_message(f"Bought {num_shares} shares of {symbol} at ${current_price}")
            
            # Step 2: Sell a call option
            expiry = datetime.now() + timedelta(days=days_to_expiry)
            strike = round(current_price + strike_offset)
            
            call_option = Asset(
                symbol=symbol,
                asset_type="option",
                expiration=expiry,
                strike=strike,
                right="call",
            )
            
            # Sell 1 contract (100 shares per contract)
            call_order = self.create_order(call_option, 1, "sell")
            self.submit_order(call_order)
            
            self.log_message(
                f"Sold 1 {symbol} ${strike} call option expiring {expiry.date()}"
            )
            
            self.covered_call_active = True


# ============================================================================
# EXAMPLE 3: Credit Spread Strategy
# ============================================================================

class CreditSpreadBot(Strategy):
    """
    Bull Put Credit Spread:
    - Sell a put at higher strike (collect premium)
    - Buy a put at lower strike (limit risk)
    
    Profits if stock stays above the sold put strike.
    """
    
    parameters = {
        "symbol": "SPY",
        "spread_width": 5,  # Difference between strikes
        "days_to_expiry": 30,
        "contracts": 1,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.spread_active = False

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        spread_width = self.parameters["spread_width"]
        days_to_expiry = self.parameters["days_to_expiry"]
        contracts = self.parameters["contracts"]
        
        current_price = self.get_last_price(symbol)
        
        if self.first_iteration and not self.spread_active:
            expiry = datetime.now() + timedelta(days=days_to_expiry)
            
            # Sell put at strike below current price (collect premium)
            sell_strike = round(current_price - 10)
            sell_put = Asset(
                symbol=symbol,
                asset_type="option",
                expiration=expiry,
                strike=sell_strike,
                right="put",
            )
            
            # Buy put at lower strike (limit risk)
            buy_strike = sell_strike - spread_width
            buy_put = Asset(
                symbol=symbol,
                asset_type="option",
                expiration=expiry,
                strike=buy_strike,
                right="put",
            )
            
            # Execute the spread
            self.submit_order(self.create_order(sell_put, contracts, "sell"))
            self.submit_order(self.create_order(buy_put, contracts, "buy"))
            
            self.log_message(
                f"Bull Put Spread: Sold ${sell_strike} put, Bought ${buy_strike} put"
            )
            
            self.spread_active = True


# ============================================================================
# EXAMPLE 4: Iron Condor using OptionsHelper
# ============================================================================

class IronCondorBot(Strategy):
    """
    Iron Condor using OptionsHelper:
    - Sell OTM call spread (above current price)
    - Sell OTM put spread (below current price)
    
    Profits if stock stays within the sold strikes.
    """
    
    parameters = {
        "symbol": "SPY",
        "wing_width": 5,  # Width of each spread
        "distance_from_price": 10,  # Distance from current price to sold strikes
        "days_to_expiry": 30,
        "contracts": 1,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.options_helper = OptionsHelper(self)
        self.condor_active = False

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        wing_width = self.parameters["wing_width"]
        distance = self.parameters["distance_from_price"]
        days_to_expiry = self.parameters["days_to_expiry"]
        contracts = self.parameters["contracts"]
        
        if self.first_iteration and not self.condor_active:
            # Get underlying asset and price
            underlying = Asset(symbol=symbol, asset_type="stock")
            current_price = self.get_last_price(underlying)
            
            # Calculate expiry date
            expiry = (datetime.now() + timedelta(days=days_to_expiry)).date()
            
            # Calculate strikes for iron condor
            # Call spread: sell at current_price + distance, buy at current_price + distance + wing_width
            call_sell_strike = round(current_price + distance)
            call_buy_strike = call_sell_strike + wing_width
            
            # Put spread: sell at current_price - distance, buy at current_price - distance - wing_width  
            put_sell_strike = round(current_price - distance)
            put_buy_strike = put_sell_strike - wing_width
            
            # Build Iron Condor orders using OptionsHelper
            orders = self.options_helper.build_iron_condor_orders(
                underlying_asset=underlying,
                expiry=expiry,
                call_sell_strike=call_sell_strike,
                call_buy_strike=call_buy_strike,
                put_sell_strike=put_sell_strike,
                put_buy_strike=put_buy_strike,
                quantity=contracts
            )
            
            # Execute the orders with limit pricing
            success = self.options_helper.execute_orders(orders, limit_type="mid")
            
            if success:
                self.log_message(
                    f"Iron Condor executed: Call spread {call_sell_strike}/{call_buy_strike}, "
                    f"Put spread {put_sell_strike}/{put_buy_strike}"
                )
                self.condor_active = True
            else:
                self.log_message("Failed to execute Iron Condor", color="red")


# ============================================================================
# EXAMPLE 5: Bull Call Spread using OptionsHelper
# ============================================================================

class BullCallSpreadBot(Strategy):
    """
    Bull Call Spread using OptionsHelper:
    - Buy call at lower strike
    - Sell call at higher strike
    
    Profits if stock rises (but capped at higher strike).
    """
    
    parameters = {
        "symbol": "AAPL",
        "spread_width": 5,
        "days_to_expiry": 30,
        "contracts": 1,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.options_helper = OptionsHelper(self)
        self.spread_active = False

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        spread_width = self.parameters["spread_width"]
        days_to_expiry = self.parameters["days_to_expiry"]
        contracts = self.parameters["contracts"]
        
        if self.first_iteration and not self.spread_active:
            # Get underlying
            underlying = Asset(symbol=symbol, asset_type="stock")
            current_price = self.get_last_price(underlying)
            
            # Calculate strikes - ATM to slightly OTM
            buy_strike = round(current_price)
            sell_strike = buy_strike + spread_width
            
            expiry = (datetime.now() + timedelta(days=days_to_expiry)).date()
            
            # Execute vertical call spread
            success = self.options_helper.execute_vertical_spread(
                underlying_asset=underlying,
                expiry=expiry,
                upper_strike=sell_strike,
                lower_strike=buy_strike,
                quantity=contracts,
                limit_type="mid"
            )
            
            if success:
                self.log_message(
                    f"Bull Call Spread executed: Buy ${buy_strike}, Sell ${sell_strike}"
                )
                self.spread_active = True


# ============================================================================
# EXAMPLE 6: Straddle Strategy using OptionsHelper
# ============================================================================

class StraddleBot(Strategy):
    """
    Straddle Strategy using OptionsHelper:
    - Buy call and put at same strike (usually ATM)
    
    Profits from large price movements in either direction.
    """
    
    parameters = {
        "symbol": "TSLA",
        "days_to_expiry": 30,
        "contracts": 1,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.options_helper = OptionsHelper(self)
        self.straddle_active = False

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        days_to_expiry = self.parameters["days_to_expiry"]
        contracts = self.parameters["contracts"]
        
        if self.first_iteration and not self.straddle_active:
            # Get underlying
            underlying = Asset(symbol=symbol, asset_type="stock")
            current_price = self.get_last_price(underlying)
            
            # ATM strike
            strike = round(current_price)
            expiry = (datetime.now() + timedelta(days=days_to_expiry)).date()
            
            # Execute straddle
            success = self.options_helper.execute_straddle(
                underlying_asset=underlying,
                expiry=expiry,
                strike=strike,
                quantity=contracts,
                limit_type="mid"
            )
            
            if success:
                self.log_message(f"Straddle executed at ${strike} strike")
                self.straddle_active = True


# ============================================================================
# Main execution section
# ============================================================================

if __name__ == "__main__":
    """
    This section shows how to run each strategy.
    Uncomment the strategy you want to run.
    """
    
    # Choose which strategy to run
    strategy_to_run = "basic"  # Options: basic, covered_call, credit_spread, iron_condor, bull_call, straddle
    
    # Set to True for live trading, False for backtesting
    is_live = False
    
    if is_live:
        # Live trading setup (requires broker credentials)
        print("Live trading mode")
        print("Note: You need to set up your broker credentials")
        print("Example for Interactive Brokers:")
        print("""
        from lumibot.brokers import InteractiveBrokers
        
        INTERACTIVE_BROKERS_CONFIG = {
            "SOCKET_PORT": 7497,  # 7496 for live, 7497 for paper
            "CLIENT_ID": 1,
        }
        
        broker = InteractiveBrokers(INTERACTIVE_BROKERS_CONFIG)
        """)
        
        # Choose strategy
        if strategy_to_run == "basic":
            strategy = BasicOptionsBot(name="BasicOptionsBot")
        elif strategy_to_run == "covered_call":
            strategy = CoveredCallBot(name="CoveredCallBot")
        elif strategy_to_run == "credit_spread":
            strategy = CreditSpreadBot(name="CreditSpreadBot")
        elif strategy_to_run == "iron_condor":
            strategy = IronCondorBot(name="IronCondorBot")
        elif strategy_to_run == "bull_call":
            strategy = BullCallSpreadBot(name="BullCallBot")
        elif strategy_to_run == "straddle":
            strategy = StraddleBot(name="StraddleBot")
        else:
            print(f"Unknown strategy: {strategy_to_run}")
            exit(1)
        
        # Run live (uncomment when broker is configured)
        # strategy.run_live()
        print("\nTo run live trading:")
        print("1. Set up your broker credentials")
        print("2. Pass broker to strategy: strategy = BasicOptionsBot(broker=broker)")
        print("3. Uncomment strategy.run_live()")
        
    else:
        # Backtesting mode
        print("Backtesting mode")
        print("Note: Backtesting options requires a data provider like Polygon.io")
        
        from lumibot.backtesting import PolygonDataBacktesting
        
        # Backtest dates
        backtesting_start = datetime(2024, 1, 1)
        backtesting_end = datetime(2024, 1, 31)
        
        # Choose strategy
        if strategy_to_run == "basic":
            StrategyClass = BasicOptionsBot
        elif strategy_to_run == "covered_call":
            StrategyClass = CoveredCallBot
        elif strategy_to_run == "credit_spread":
            StrategyClass = CreditSpreadBot
        elif strategy_to_run == "iron_condor":
            StrategyClass = IronCondorBot
        elif strategy_to_run == "bull_call":
            StrategyClass = BullCallSpreadBot
        elif strategy_to_run == "straddle":
            StrategyClass = StraddleBot
        else:
            print(f"Unknown strategy: {strategy_to_run}")
            exit(1)
        
        print(f"\nRunning backtest for {StrategyClass.__name__}...")
        print("Note: Replace 'YOUR_POLYGON_API_KEY' with your actual API key")
        
        # Uncomment to run backtest (requires Polygon API key)
        # results = StrategyClass.backtest(
        #     PolygonDataBacktesting,
        #     backtesting_start,
        #     backtesting_end,
        #     benchmark_asset="SPY",
        #     polygon_api_key="YOUR_POLYGON_API_KEY",
        # )
        
        print("\nTo run backtest:")
        print("1. Get a Polygon.io API key from https://polygon.io")
        print("2. Replace 'YOUR_POLYGON_API_KEY' with your key")
        print("3. Uncomment the backtest code above")
