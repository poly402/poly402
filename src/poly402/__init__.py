"""
poly402 - Programmatic Prediction Market Trading via HTTP Payment Protocol

Bridges Coinbase's x402 payment protocol with Polymarket's prediction market API.
"""

__version__ = "1.0.0"

from .client import Poly402Client
from .models import Market, Outcome, TradeResult

__all__ = ["Poly402Client", "Market", "Outcome", "TradeResult"]
