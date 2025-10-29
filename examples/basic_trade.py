"""
Basic Trading Example

This example demonstrates how to:
1. Initialize the poly402 client
2. Fetch market data
3. Execute a simple trade
"""

from poly402 import Poly402Client

def main():
    # Initialize client (uses ~/.poly402/config.json by default)
    client = Poly402Client()
    
    # Example Polymarket URL
    market_url = "https://polymarket.com/event/fed-decision-in-october"
    
    # Fetch market data
    print("Fetching market data...")
    market = client.get_market(market_url)
    
    print(f"\nMarket: {market.title}")
    print(f"Active: {market.active}")
    print(f"\nAvailable Outcomes:")
    for outcome in market.outcomes:
        print(f"  [{outcome.index}] {outcome.name}")
        print(f"      Price: ${outcome.price:.4f} ({outcome.probability:.2f}% probability)")
    
    # Check balances before trading
    print("\nChecking balances...")
    balances = client.get_balance()
    for network, balance in balances.items():
        print(f"  {balance.network}: ${balance.usdc_balance:.2f} USDC")
    
    # Execute a trade
    print("\nExecuting trade...")
    outcome_index = 0  # First outcome
    amount_usdc = 10.0  # Bet $10 USDC
    
    try:
        result = client.execute_trade(
            market_url=market_url,
            outcome_index=outcome_index,
            amount_usdc=amount_usdc
        )
        
        if result.error:
            print(f"\n❌ Trade failed: {result.error}")
        else:
            print(f"\n✅ Trade successful!")
            print(f"   Order ID: {result.order_id}")
            print(f"   Outcome: {result.outcome_name}")
            print(f"   Shares: {result.shares_purchased:.2f} @ ${result.price_per_share:.4f}")
            print(f"   Status: {result.status.value}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
