"""
Polymarket CLOB client wrapper
"""

from typing import Optional
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY
from .models import TradeResult, OrderStatus, PaymentInfo, Outcome
from datetime import datetime


class PolymarketClient:
    """Wrapper for Polymarket CLOB client"""
    
    def __init__(
        self,
        host: str,
        chain_id: int,
        private_key: str,
        signature_type: int = 2,
        proxy_address: Optional[str] = None
    ):
        """
        Initialize Polymarket client
        
        Args:
            host: CLOB API endpoint
            chain_id: Polygon chain ID (137 for mainnet)
            private_key: Polygon wallet private key
            signature_type: 1 for email/magic, 2 for browser wallet
            proxy_address: Optional proxy wallet address
        """
        self.host = host
        self.chain_id = chain_id
        
        # Initialize CLOB client
        if proxy_address:
            self.client = ClobClient(
                host,
                key=private_key,
                chain_id=chain_id,
                signature_type=signature_type,
                funder=proxy_address
            )
        else:
            self.client = ClobClient(
                host,
                key=private_key,
                chain_id=chain_id
            )
    
    def setup_credentials(self):
        """Create or derive API credentials"""
        try:
            creds = self.client.create_or_derive_api_creds()
            self.client.set_api_creds(creds)
            return creds
        except Exception as e:
            raise RuntimeError(f"Failed to setup API credentials: {e}")
    
    def create_buy_order(
        self,
        outcome: Outcome,
        amount_usdc: float,
        max_price: Optional[float] = None
    ) -> TradeResult:
        """
        Create and execute a buy order
        
        Args:
            outcome: The outcome to bet on
            amount_usdc: Amount in USDC to spend
            max_price: Maximum price per share (optional)
            
        Returns:
            TradeResult with order details
        """
        # Ensure credentials are set
        if not hasattr(self.client, 'api_creds') or not self.client.api_creds:
            self.setup_credentials()
        
        # Determine price - use current price or max_price if specified
        price = min(outcome.price, max_price) if max_price else outcome.price
        
        # Calculate size (number of shares)
        size = amount_usdc / price if price > 0 else 0
        
        # Create order arguments
        order_args = OrderArgs(
            price=price,
            size=size,
            side=BUY,
            token_id=outcome.token_id
        )
        
        try:
            # Create and sign order
            signed_order = self.client.create_order(order_args)
            
            # Post order as GTC (Good-Til-Cancelled)
            resp = self.client.post_order(signed_order, OrderType.GTC)
            
            # Parse response
            if resp.get('success'):
                order_id = resp.get('orderId', '')
                status = OrderStatus.COMPLETED if resp.get('status') == 'matched' else OrderStatus.TRADING
                
                # Create placeholder payment info (will be filled by orchestrator)
                payment_info = PaymentInfo(
                    amount=amount_usdc,
                    network="polygon",
                    token="USDC",
                    tx_hash=None,
                    status="completed"
                )
                
                return TradeResult(
                    order_id=order_id,
                    market_slug="",  # Will be filled by caller
                    outcome_name=outcome.name,
                    amount_usdc=amount_usdc,
                    shares_purchased=size,
                    price_per_share=price,
                    status=status,
                    tx_hash=None,
                    payment_info=payment_info,
                    timestamp=datetime.now()
                )
            else:
                error_msg = resp.get('errorMsg', 'Unknown error')
                payment_info = PaymentInfo(
                    amount=amount_usdc,
                    network="polygon",
                    token="USDC",
                    tx_hash=None,
                    status="failed"
                )
                
                return TradeResult(
                    order_id="",
                    market_slug="",
                    outcome_name=outcome.name,
                    amount_usdc=amount_usdc,
                    shares_purchased=0,
                    price_per_share=price,
                    status=OrderStatus.FAILED,
                    tx_hash=None,
                    payment_info=payment_info,
                    timestamp=datetime.now(),
                    error=error_msg
                )
        except Exception as e:
            payment_info = PaymentInfo(
                amount=amount_usdc,
                network="polygon",
                token="USDC",
                tx_hash=None,
                status="failed"
            )
            
            return TradeResult(
                order_id="",
                market_slug="",
                outcome_name=outcome.name,
                amount_usdc=amount_usdc,
                shares_purchased=0,
                price_per_share=price,
                status=OrderStatus.FAILED,
                tx_hash=None,
                payment_info=payment_info,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    def get_order(self, order_id: str) -> dict:
        """Get order details by ID"""
        try:
            return self.client.get_order(order_id)
        except Exception as e:
            raise RuntimeError(f"Failed to get order: {e}")
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an active order"""
        try:
            resp = self.client.cancel(order_id)
            return resp.get('success', False)
        except Exception as e:
            raise RuntimeError(f"Failed to cancel order: {e}")
    
    def get_balances(self) -> dict:
        """Get wallet balances"""
        try:
            return self.client.get_balances()
        except Exception:
            return {}
