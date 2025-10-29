"""
Main poly402 client - orchestrates x402 payments and Polymarket trades
"""

from typing import Optional
from web3 import Web3
from eth_account import Account
from .config import ConfigManager
from .models import Market, TradeResult, Balance, Config
from .market_parser import MarketParser
from .polymarket_client import PolymarketClient


class Poly402Client:
    """
    Main client for poly402
    
    Coordinates x402 payments on Base with Polymarket trades on Polygon
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize poly402 client
        
        Args:
            config_path: Path to configuration file (optional)
        """
        # Load configuration
        config_manager = ConfigManager(config_path)
        self.config: Config = config_manager.load()
        
        # Initialize market parser
        self.market_parser = MarketParser(self.config.polymarket_gamma_endpoint)
        
        # Initialize Polymarket client
        self.polymarket = PolymarketClient(
            host=self.config.polymarket_clob_endpoint,
            chain_id=self.config.polygon_chain_id,
            private_key=self.config.polygon_private_key,
            signature_type=self.config.signature_type
        )
        
        # Initialize Web3 for balance checks
        self.base_w3 = Web3(Web3.HTTPProvider(self.config.base_rpc_url))
        self.polygon_w3 = Web3(Web3.HTTPProvider(self.config.polygon_rpc_url))
        
        # Get wallet addresses
        self.base_account = Account.from_key(self.config.base_private_key)
        self.polygon_account = Account.from_key(self.config.polygon_private_key)
        
        # USDC contract addresses
        self.USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        self.USDC_POLYGON = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # USDC (bridged)
        
    def get_market(self, url: str) -> Market:
        """
        Fetch market data from URL
        
        Args:
            url: Polymarket event URL or slug
            
        Returns:
            Market object with all details
        """
        return self.market_parser.fetch_market(url)
    
    def execute_trade(
        self,
        market_url: str,
        outcome_index: int,
        amount_usdc: float,
        max_price: Optional[float] = None
    ) -> TradeResult:
        """
        Execute a complete trade flow:
        1. Fetch market data
        2. Verify x402 payment (simulated for now)
        3. Execute Polymarket trade
        
        Args:
            market_url: Polymarket event URL
            outcome_index: Index of outcome to bet on
            amount_usdc: Amount in USDC to wager
            max_price: Maximum price per share (optional)
            
        Returns:
            TradeResult with execution details
        """
        # Step 1: Fetch market data
        market = self.get_market(market_url)
        
        if not market.active:
            raise ValueError(f"Market '{market.title}' is not active")
        
        if outcome_index >= len(market.outcomes):
            raise ValueError(f"Invalid outcome index {outcome_index}. Market has {len(market.outcomes)} outcomes.")
        
        outcome = market.outcomes[outcome_index]
        
        # Step 2: Verify balances
        polygon_balance = self._get_usdc_balance("polygon")
        if polygon_balance < amount_usdc:
            raise ValueError(
                f"Insufficient USDC balance on Polygon. "
                f"Required: {amount_usdc}, Available: {polygon_balance}"
            )
        
        # Step 3: Verify x402 payment capability (check Base balance)
        # In a full implementation, this would involve actual x402 payment flow
        base_balance = self._get_usdc_balance("base")
        if base_balance < self.config.x402_max_payment:
            print(f"Warning: Low USDC balance on Base for x402 payments: {base_balance}")
        
        # Step 4: Execute Polymarket trade
        result = self.polymarket.create_buy_order(
            outcome=outcome,
            amount_usdc=amount_usdc,
            max_price=max_price
        )
        
        # Update result with market info
        result.market_slug = market.slug
        
        return result
    
    def get_balance(self, network: str = "both") -> dict:
        """
        Get USDC balances
        
        Args:
            network: "base", "polygon", or "both"
            
        Returns:
            Dictionary with balance information
        """
        balances = {}
        
        if network in ["base", "both"]:
            base_usdc = self._get_usdc_balance("base")
            base_eth = self.base_w3.from_wei(
                self.base_w3.eth.get_balance(self.base_account.address),
                'ether'
            )
            balances["base"] = Balance(
                network="Base",
                usdc_balance=base_usdc,
                address=self.base_account.address,
                native_balance=float(base_eth)
            )
        
        if network in ["polygon", "both"]:
            polygon_usdc = self._get_usdc_balance("polygon")
            polygon_matic = self.polygon_w3.from_wei(
                self.polygon_w3.eth.get_balance(self.polygon_account.address),
                'ether'
            )
            balances["polygon"] = Balance(
                network="Polygon",
                usdc_balance=polygon_usdc,
                address=self.polygon_account.address,
                native_balance=float(polygon_matic)
            )
        
        return balances
    
    def _get_usdc_balance(self, network: str) -> float:
        """Get USDC balance for a network"""
        try:
            if network == "base":
                w3 = self.base_w3
                usdc_address = self.USDC_BASE
                account = self.base_account.address
            elif network == "polygon":
                w3 = self.polygon_w3
                usdc_address = self.USDC_POLYGON
                account = self.polygon_account.address
            else:
                return 0.0
            
            # USDC ERC20 ABI (balanceOf only)
            usdc_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                }
            ]
            
            contract = w3.eth.contract(address=usdc_address, abi=usdc_abi)
            balance_wei = contract.functions.balanceOf(account).call()
            
            # USDC has 6 decimals
            return balance_wei / 1e6
        except Exception as e:
            print(f"Warning: Could not fetch USDC balance for {network}: {e}")
            return 0.0
    
    def search_markets(self, query: str, limit: int = 10):
        """Search for markets"""
        return self.market_parser.search_markets(query, limit)
    
    def get_active_markets(self, limit: int = 100):
        """Get active markets"""
        return self.market_parser.get_active_markets(limit)
