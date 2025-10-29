# poly402 Quick Start Guide

Get up and running with poly402 in minutes.

## 1. Installation (5 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/poly402.git
cd poly402

# Install
pip install -r requirements.txt
npm install
pip install -e .
```

## 2. Configuration (2 minutes)

```bash
# Initialize configuration
poly402 init
```

Enter your private keys when prompted:
- Base network private key (for x402 payments)
- Polygon network private key (for Polymarket trades)

## 3. Fund Wallets (varies)

Transfer USDC to your wallets:

**Base Network:**
- Use [Official Base Bridge](https://bridge.base.org)
- Recommended: 50-100 USDC

**Polygon Network:**
- Use [Polygon Bridge](https://wallet.polygon.technology/bridge)
- Recommended: 100-500 USDC

Verify:
```bash
poly402 balance
```

## 4. Your First Trade (1 minute)

```bash
# View a market
poly402 markets --url https://polymarket.com/event/fed-decision-in-october

# Execute a trade
poly402 trade \
  --url https://polymarket.com/event/fed-decision-in-october \
  --outcome 0 \
  --amount 10
```

## Common Commands

```bash
# Check balances
poly402 balance

# Search markets
poly402 search --query "election"

# View active markets
poly402 active --limit 10

# View market details
poly402 markets --url <polymarket-url>

# Execute trade
poly402 trade --url <url> --outcome <index> --amount <usdc>
```

## Python API Usage

```python
from poly402 import Poly402Client

# Initialize
client = Poly402Client()

# Get market
market = client.get_market("https://polymarket.com/event/xyz")

# Execute trade
result = client.execute_trade(
    market_url="https://polymarket.com/event/xyz",
    outcome_index=0,
    amount_usdc=10.0
)

print(f"Order ID: {result.order_id}")
print(f"Shares: {result.shares_purchased}")
```

## What's Next?

- Read the [full documentation](README.md)
- Review [installation guide](docs/INSTALLATION.md)
- Check [security best practices](README.md#security-best-practices)
- Explore [examples](examples/)

## Need Help?

- GitHub Issues: https://github.com/yourusername/poly402/issues
- Documentation: README.md
- Examples: examples/basic_trade.py

## Important Notes

- This is educational software - understand the risks
- Never commit private keys to version control
- Start with small amounts to test
- Comply with local regulations regarding prediction markets

---

**Ready to trade?** Run `poly402 --help` to see all available commands.
