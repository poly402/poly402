"""
Data models for poly402
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    """Trade order status"""
    PENDING = "pending"
    PAYING = "paying"
    TRADING = "trading"
    COMPLETED = "completed"
    FAILED = "failed"


class OrderType(Enum):
    """Polymarket order types"""
    GTC = "GTC"  # Good-Til-Cancelled
    GTD = "GTD"  # Good-Til-Date
    FOK = "FOK"  # Fill-Or-Kill
    FAK = "FAK"  # Fill-And-Kill


@dataclass
class Outcome:
    """Represents a market outcome option"""
    index: int
    name: str
    token_id: str
    price: float  # Current price in USDC (0-1)
    probability: float  # Implied probability (0-100%)


@dataclass
class Market:
    """Represents a Polymarket prediction market"""
    slug: str
    title: str
    description: str
    outcomes: List[Outcome]
    active: bool
    end_date: Optional[datetime]
    condition_id: str
    question_id: Optional[str]
    volume: Optional[float]
    liquidity: Optional[float]


@dataclass
class PaymentInfo:
    """x402 payment information"""
    amount: float
    network: str  # "base"
    token: str  # "USDC"
    tx_hash: Optional[str]
    status: str


@dataclass
class TradeResult:
    """Result of a trade execution"""
    order_id: str
    market_slug: str
    outcome_name: str
    amount_usdc: float
    shares_purchased: float
    price_per_share: float
    status: OrderStatus
    tx_hash: Optional[str]
    payment_info: PaymentInfo
    timestamp: datetime
    error: Optional[str] = None


@dataclass
class Balance:
    """Wallet balance information"""
    network: str
    usdc_balance: float
    address: str
    native_balance: Optional[float] = None


@dataclass
class Config:
    """poly402 configuration"""
    base_private_key: str
    base_rpc_url: str
    base_chain_id: int
    polygon_private_key: str
    polygon_rpc_url: str
    polygon_chain_id: int
    polymarket_clob_endpoint: str
    polymarket_gamma_endpoint: str
    polymarket_api_key: Optional[str]
    polymarket_api_secret: Optional[str]
    polymarket_api_passphrase: Optional[str]
    x402_facilitator: str
    x402_max_payment: float
    signature_type: int = 2  # Default to browser wallet signature type
