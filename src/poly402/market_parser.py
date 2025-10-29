"""
Polymarket market URL parser and data fetcher
"""

import re
import requests
from typing import Optional
from datetime import datetime
from .models import Market, Outcome


class MarketParser:
    """Parse Polymarket URLs and fetch market data"""
    
    def __init__(self, gamma_endpoint: str):
        """Initialize market parser"""
        self.gamma_endpoint = gamma_endpoint
    
    def extract_slug(self, url: str) -> str:
        """
        Extract market slug from Polymarket URL
        
        Examples:
            https://polymarket.com/event/fed-decision-in-october -> fed-decision-in-october
            https://polymarket.com/event/nyc-mayoral-election?tid=123 -> nyc-mayoral-election
        """
        # Remove query parameters
        url = url.split('?')[0]
        
        # Extract slug from URL path
        patterns = [
            r'polymarket\.com/event/([^/]+)',
            r'polymarket\.com/market/([^/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume the input is already a slug
        if '/' not in url and 'polymarket.com' not in url:
            return url
        
        raise ValueError(f"Could not extract slug from URL: {url}")
    
    def fetch_market(self, url_or_slug: str) -> Market:
        """
        Fetch market data from Polymarket Gamma API
        
        Args:
            url_or_slug: Full Polymarket URL or just the slug
            
        Returns:
            Market object with all details
        """
        slug = self.extract_slug(url_or_slug)
        
        # Fetch event data from Gamma API
        endpoint = f"{self.gamma_endpoint}/events/slug/{slug}"
        
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch market data: {e}")
        
        # Parse market data
        return self._parse_market_data(data, slug)
    
    def _parse_market_data(self, data: dict, slug: str) -> Market:
        """Parse Gamma API response into Market object"""
        
        # Extract outcomes from markets array
        outcomes = []
        markets_data = data.get('markets', [])
        
        for idx, market in enumerate(markets_data):
            outcome = Outcome(
                index=idx,
                name=market.get('outcome', f"Outcome {idx}"),
                token_id=market.get('clobTokenIds', [''])[0],
                price=float(market.get('outcomePrices', [0.5])[0]),
                probability=float(market.get('outcomePrices', [0.5])[0]) * 100
            )
            outcomes.append(outcome)
        
        # Parse end date
        end_date = None
        end_date_iso = data.get('endDate')
        if end_date_iso:
            try:
                end_date = datetime.fromisoformat(end_date_iso.replace('Z', '+00:00'))
            except ValueError:
                pass
        
        return Market(
            slug=slug,
            title=data.get('title', ''),
            description=data.get('description', ''),
            outcomes=outcomes,
            active=data.get('active', True),
            end_date=end_date,
            condition_id=data.get('conditionId', ''),
            question_id=data.get('questionID'),
            volume=data.get('volume'),
            liquidity=data.get('liquidity')
        )
    
    def search_markets(self, query: str, limit: int = 10) -> list[Market]:
        """
        Search for markets by query string
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of Market objects
        """
        endpoint = f"{self.gamma_endpoint}/search"
        params = {
            'query': query,
            'limit': limit
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to search markets: {e}")
        
        markets = []
        for event_data in data:
            try:
                slug = event_data.get('slug', '')
                market = self._parse_market_data(event_data, slug)
                markets.append(market)
            except Exception:
                continue
        
        return markets
    
    def get_active_markets(self, limit: int = 100, offset: int = 0) -> list[Market]:
        """
        Get all active markets
        
        Args:
            limit: Number of markets to fetch
            offset: Offset for pagination
            
        Returns:
            List of Market objects
        """
        endpoint = f"{self.gamma_endpoint}/events"
        params = {
            'closed': 'false',
            'limit': limit,
            'offset': offset,
            'order': 'id',
            'ascending': 'false'
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch active markets: {e}")
        
        markets = []
        for event_data in data:
            try:
                slug = event_data.get('slug', '')
                market = self._parse_market_data(event_data, slug)
                markets.append(market)
            except Exception:
                continue
        
        return markets
