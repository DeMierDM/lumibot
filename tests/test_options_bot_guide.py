"""
Unit tests for the Options Bot Guide examples.

These tests verify that the option bot strategies can be instantiated
and their basic functionality works correctly.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch

# Import the strategy classes
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

from options_bot_guide import (
    BasicOptionsBot,
    CoveredCallBot,
    CreditSpreadBot,
    IronCondorBot,
    BullCallSpreadBot,
    StraddleBot
)

from lumibot.entities import Asset


class TestBasicOptionsBot:
    """Test the BasicOptionsBot strategy"""
    
    def test_initialization(self):
        """Test that BasicOptionsBot initializes correctly"""
        strategy = BasicOptionsBot()
        strategy.initialize()
        
        assert strategy.sleeptime == "1D"
        assert "symbol" in strategy.parameters
        assert "quantity" in strategy.parameters
        assert "days_to_expiry" in strategy.parameters
    
    def test_parameters_defaults(self):
        """Test default parameters"""
        strategy = BasicOptionsBot()
        
        assert strategy.parameters["symbol"] == "SPY"
        assert strategy.parameters["quantity"] == 1
        assert strategy.parameters["days_to_expiry"] == 30
    
    @patch('options_bot_guide.BasicOptionsBot.get_last_price')
    @patch('options_bot_guide.BasicOptionsBot.create_order')
    @patch('options_bot_guide.BasicOptionsBot.submit_order')
    @patch('options_bot_guide.BasicOptionsBot.log_message')
    def test_on_trading_iteration_first_iteration(self, mock_log, mock_submit, mock_create, mock_price):
        """Test the trading iteration on first run"""
        # Setup mocks
        mock_price.return_value = 450.0
        mock_order = Mock()
        mock_create.return_value = mock_order
        
        # Create and initialize strategy
        strategy = BasicOptionsBot()
        strategy.initialize()
        strategy.first_iteration = True
        
        # Run iteration
        strategy.on_trading_iteration()
        
        # Verify price was fetched
        mock_price.assert_called_once_with("SPY")
        
        # Verify order was created with an option asset
        assert mock_create.called
        call_args = mock_create.call_args
        option_asset = call_args[0][0]
        
        assert isinstance(option_asset, Asset)
        assert option_asset.symbol == "SPY"
        assert option_asset.asset_type == "option"
        assert option_asset.strike == 450  # Rounded price
        assert option_asset.right == "call"
        
        # Verify order was submitted
        mock_submit.assert_called_once_with(mock_order)
        
        # Verify logging
        assert mock_log.call_count >= 1


class TestCoveredCallBot:
    """Test the CoveredCallBot strategy"""
    
    def test_initialization(self):
        """Test that CoveredCallBot initializes correctly"""
        strategy = CoveredCallBot()
        strategy.initialize()
        
        assert strategy.sleeptime == "1D"
        assert strategy.covered_call_active == False
    
    def test_parameters(self):
        """Test parameters"""
        strategy = CoveredCallBot()
        
        assert strategy.parameters["symbol"] == "AAPL"
        assert strategy.parameters["num_shares"] == 100
        assert strategy.parameters["strike_offset"] == 5
    
    @patch('options_bot_guide.CoveredCallBot.get_last_price')
    @patch('options_bot_guide.CoveredCallBot.create_order')
    @patch('options_bot_guide.CoveredCallBot.submit_order')
    @patch('options_bot_guide.CoveredCallBot.log_message')
    def test_executes_covered_call(self, mock_log, mock_submit, mock_create, mock_price):
        """Test that covered call executes both stock and option orders"""
        mock_price.return_value = 175.0
        mock_create.return_value = Mock()
        
        strategy = CoveredCallBot()
        strategy.initialize()
        strategy.first_iteration = True
        
        strategy.on_trading_iteration()
        
        # Should create 2 orders: stock buy and option sell
        assert mock_create.call_count == 2
        assert mock_submit.call_count == 2
        
        # Verify the stock order (first call)
        stock_call = mock_create.call_args_list[0]
        stock_asset = stock_call[0][0]
        assert stock_asset.symbol == "AAPL"
        assert stock_asset.asset_type == "stock"
        assert stock_call[0][1] == 100  # num_shares
        assert stock_call[0][2] == "buy"
        
        # Verify the option order (second call)
        option_call = mock_create.call_args_list[1]
        option_asset = option_call[0][0]
        assert option_asset.symbol == "AAPL"
        assert option_asset.asset_type == "option"
        assert option_asset.strike == 180  # 175 + 5 offset
        assert option_asset.right == "call"
        assert option_call[0][1] == 1  # 1 contract
        assert option_call[0][2] == "sell"


class TestCreditSpreadBot:
    """Test the CreditSpreadBot strategy"""
    
    def test_initialization(self):
        """Test initialization"""
        strategy = CreditSpreadBot()
        strategy.initialize()
        
        assert strategy.sleeptime == "1D"
        assert strategy.spread_active == False
    
    @patch('options_bot_guide.CreditSpreadBot.get_last_price')
    @patch('options_bot_guide.CreditSpreadBot.create_order')
    @patch('options_bot_guide.CreditSpreadBot.submit_order')
    @patch('options_bot_guide.CreditSpreadBot.log_message')
    def test_creates_put_spread(self, mock_log, mock_submit, mock_create, mock_price):
        """Test that credit spread creates sell and buy put orders"""
        mock_price.return_value = 450.0
        mock_create.return_value = Mock()
        
        strategy = CreditSpreadBot()
        strategy.initialize()
        strategy.first_iteration = True
        
        strategy.on_trading_iteration()
        
        # Should create 2 put orders
        assert mock_create.call_count == 2
        
        # First order: sell put at 440 (450 - 10)
        sell_call = mock_create.call_args_list[0]
        sell_put = sell_call[0][0]
        assert sell_put.asset_type == "option"
        assert sell_put.strike == 440
        assert sell_put.right == "put"
        
        # Second order: buy put at 435 (440 - 5 spread width)
        buy_call = mock_create.call_args_list[1]
        buy_put = buy_call[0][0]
        assert buy_put.asset_type == "option"
        assert buy_put.strike == 435
        assert buy_put.right == "put"


class TestIronCondorBot:
    """Test the IronCondorBot strategy"""
    
    def test_initialization(self):
        """Test initialization with OptionsHelper"""
        strategy = IronCondorBot()
        strategy.initialize()
        
        assert strategy.sleeptime == "1D"
        assert hasattr(strategy, 'options_helper')
        assert strategy.condor_active == False
    
    @patch('options_bot_guide.OptionsHelper')
    @patch('options_bot_guide.IronCondorBot.get_last_price')
    @patch('options_bot_guide.IronCondorBot.log_message')
    def test_builds_iron_condor_orders(self, mock_log, mock_price, mock_helper_class):
        """Test that iron condor builds correct orders"""
        mock_price.return_value = 450.0
        
        # Mock the OptionsHelper methods
        mock_helper = Mock()
        mock_helper.build_iron_condor_orders.return_value = [Mock(), Mock(), Mock(), Mock()]
        mock_helper.execute_orders.return_value = True
        mock_helper_class.return_value = mock_helper
        
        strategy = IronCondorBot()
        strategy.initialize()
        strategy.first_iteration = True
        
        strategy.on_trading_iteration()
        
        # Verify iron condor was built with correct strikes
        assert mock_helper.build_iron_condor_orders.called
        call_args = mock_helper.build_iron_condor_orders.call_args
        
        # Verify strikes are calculated correctly
        assert call_args[1]['call_sell_strike'] == 460  # 450 + 10
        assert call_args[1]['call_buy_strike'] == 465   # 460 + 5
        assert call_args[1]['put_sell_strike'] == 440   # 450 - 10
        assert call_args[1]['put_buy_strike'] == 435    # 440 - 5
        
        # Verify execute_orders was called
        assert mock_helper.execute_orders.called


class TestBullCallSpreadBot:
    """Test the BullCallSpreadBot strategy"""
    
    def test_initialization(self):
        """Test initialization"""
        strategy = BullCallSpreadBot()
        strategy.initialize()
        
        assert hasattr(strategy, 'options_helper')
        assert strategy.spread_active == False
    
    @patch('options_bot_guide.OptionsHelper')
    @patch('options_bot_guide.BullCallSpreadBot.get_last_price')
    @patch('options_bot_guide.BullCallSpreadBot.log_message')
    def test_executes_vertical_spread(self, mock_log, mock_price, mock_helper_class):
        """Test that bull call spread executes vertical spread"""
        mock_price.return_value = 175.0
        
        mock_helper = Mock()
        mock_helper.execute_vertical_spread.return_value = True
        mock_helper_class.return_value = mock_helper
        
        strategy = BullCallSpreadBot()
        strategy.initialize()
        strategy.first_iteration = True
        
        strategy.on_trading_iteration()
        
        # Verify vertical spread was executed
        assert mock_helper.execute_vertical_spread.called
        call_args = mock_helper.execute_vertical_spread.call_args
        
        # Check strikes
        assert call_args[1]['lower_strike'] == 175  # ATM
        assert call_args[1]['upper_strike'] == 180  # ATM + 5
        assert call_args[1]['limit_type'] == "mid"


class TestStraddleBot:
    """Test the StraddleBot strategy"""
    
    def test_initialization(self):
        """Test initialization"""
        strategy = StraddleBot()
        strategy.initialize()
        
        assert hasattr(strategy, 'options_helper')
        assert strategy.straddle_active == False
    
    @patch('options_bot_guide.OptionsHelper')
    @patch('options_bot_guide.StraddleBot.get_last_price')
    @patch('options_bot_guide.StraddleBot.log_message')
    def test_executes_straddle(self, mock_log, mock_price, mock_helper_class):
        """Test that straddle strategy executes correctly"""
        mock_price.return_value = 250.0
        
        mock_helper = Mock()
        mock_helper.execute_straddle.return_value = True
        mock_helper_class.return_value = mock_helper
        
        strategy = StraddleBot()
        strategy.initialize()
        strategy.first_iteration = True
        
        strategy.on_trading_iteration()
        
        # Verify straddle was executed
        assert mock_helper.execute_straddle.called
        call_args = mock_helper.execute_straddle.call_args
        
        # Check ATM strike
        assert call_args[1]['strike'] == 250
        assert call_args[1]['limit_type'] == "mid"


class TestStrategyParameters:
    """Test that strategies accept custom parameters"""
    
    def test_basic_options_custom_params(self):
        """Test BasicOptionsBot with custom parameters"""
        custom_params = {
            "symbol": "AAPL",
            "quantity": 5,
            "days_to_expiry": 45
        }
        
        strategy = BasicOptionsBot(parameters=custom_params)
        
        assert strategy.parameters["symbol"] == "AAPL"
        assert strategy.parameters["quantity"] == 5
        assert strategy.parameters["days_to_expiry"] == 45
    
    def test_iron_condor_custom_params(self):
        """Test IronCondorBot with custom parameters"""
        custom_params = {
            "symbol": "QQQ",
            "wing_width": 10,
            "distance_from_price": 20,
            "contracts": 2
        }
        
        strategy = IronCondorBot(parameters=custom_params)
        
        assert strategy.parameters["symbol"] == "QQQ"
        assert strategy.parameters["wing_width"] == 10
        assert strategy.parameters["distance_from_price"] == 20
        assert strategy.parameters["contracts"] == 2


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
