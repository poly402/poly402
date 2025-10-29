"""
Configuration management for poly402
"""

import json
import os
from pathlib import Path
from typing import Optional
from .models import Config


class ConfigManager:
    """Manages poly402 configuration"""
    
    DEFAULT_CONFIG_PATH = Path.home() / ".poly402" / "config.json"
    
    DEFAULT_CONFIG = {
        "networks": {
            "base": {
                "rpc_url": "https://mainnet.base.org",
                "chain_id": 8453,
                "wallet_private_key": ""
            },
            "polygon": {
                "rpc_url": "https://polygon-rpc.com",
                "chain_id": 137,
                "wallet_private_key": ""
            }
        },
        "polymarket": {
            "clob_endpoint": "https://clob.polymarket.com",
            "gamma_endpoint": "https://gamma-api.polymarket.com",
            "api_key": "",
            "api_secret": "",
            "api_passphrase": ""
        },
        "x402": {
            "facilitator": "https://x402.coinbase.com",
            "max_payment_amount": "100.00"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATH
        
    def load(self) -> Config:
        """Load configuration from file"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {self.config_path}. "
                "Run 'poly402 init' to create it."
            )
        
        with open(self.config_path, 'r') as f:
            data = json.load(f)
        
        # Support environment variables override
        base_key = os.getenv('POLY402_BASE_KEY') or data['networks']['base']['wallet_private_key']
        polygon_key = os.getenv('POLY402_POLYGON_KEY') or data['networks']['polygon']['wallet_private_key']
        
        return Config(
            base_private_key=base_key,
            base_rpc_url=data['networks']['base']['rpc_url'],
            base_chain_id=data['networks']['base']['chain_id'],
            polygon_private_key=polygon_key,
            polygon_rpc_url=data['networks']['polygon']['rpc_url'],
            polygon_chain_id=data['networks']['polygon']['chain_id'],
            polymarket_clob_endpoint=data['polymarket']['clob_endpoint'],
            polymarket_gamma_endpoint=data['polymarket']['gamma_endpoint'],
            polymarket_api_key=data['polymarket'].get('api_key'),
            polymarket_api_secret=data['polymarket'].get('api_secret'),
            polymarket_api_passphrase=data['polymarket'].get('api_passphrase'),
            x402_facilitator=data['x402']['facilitator'],
            x402_max_payment=float(data['x402']['max_payment_amount'])
        )
    
    def save(self, config: dict):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def create_default(self):
        """Create default configuration file"""
        self.save(self.DEFAULT_CONFIG)
        return self.config_path
    
    def exists(self) -> bool:
        """Check if configuration file exists"""
        return self.config_path.exists()
    
    def update_polymarket_credentials(self, api_key: str, api_secret: str, api_passphrase: str):
        """Update Polymarket API credentials"""
        with open(self.config_path, 'r') as f:
            data = json.load(f)
        
        data['polymarket']['api_key'] = api_key
        data['polymarket']['api_secret'] = api_secret
        data['polymarket']['api_passphrase'] = api_passphrase
        
        self.save(data)
