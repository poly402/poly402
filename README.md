<p align="center">
  <img src="poly402banner.png" alt="poly402 Banner">
</p>

# poly402

**Programmatic Prediction Market Trading via HTTP Payment Protocol**

## Abstract

poly402 is a self-hosted CLI tool that bridges Coinbase's x402 payment protocol with Polymarket's prediction market API, enabling programmatic, payment-gated access to prediction market trading. The system leverages x402's HTTP 402 Payment Required mechanism for fee-free USDC payments on Base network, while executing trades on Polymarket's Polygon-based CLOB (Central Limit Order Book).

This implementation demonstrates a novel cross-chain payment verification model where payment authorization on one network (Base) triggers trade execution on another (Polygon), creating a non-custodial, programmatic trading experience suitable for both human operators and autonomous agents.

## Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                          poly402 CLI                             │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │
│  │   Market     │      │     x402     │      │  Polymarket  │    │
│  │   Parser     │──────│   Payment    │──────│    Client    │    │
│  │              │      │   Handler    │      │              │    │
│  └──────────────┘      └──────────────┘      └──────────────┘    │
│         │                     │                      │           │
└─────────┼─────────────────────┼──────────────────────┼───────────┘
          │                     │                      │
          │                     │                      │
     ┌────▼────┐          ┌─────▼─────┐         ┌─────▼─────┐
     │ Gamma   │          │   Base    │         │  Polygon  │
     │   API   │          │  Network  │         │  Network  │
     │         │          │  (x402)   │         │  (CLOB)   │
     └─────────┘          └───────────┘         └───────────┘
```

### Multi-Network Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       User's Execution Context                   │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
         ┌─────────────────────────────────────┐
         │         poly402 Orchestrator        │
         └─────────────────────────────────────┘
                  │                    │
         ┌────────▼────────┐  ┌────────▼────────┐
         │  Payment Layer  │  │  Trading Layer  │
         │    (x402)       │  │  (Polymarket)   │
         └─────────────────┘  └─────────────────┘
                  │                    │
         ┌────────▼────────┐  ┌────────▼────────┐
         │  Base Network   │  │ Polygon Network │
         │  USDC Balance   │  │  USDC Balance   │
         │  Wallet Signer  │  │  Wallet Signer  │
         └─────────────────┘  └─────────────────┘
```

## Payment Flow Sequence

```
User              poly402            x402           Polymarket
 │                  │                 │                  │
 │──trade cmd──────▶│                 │                  │
 │                  │                 │                  │
 │                  │──fetch data────────────────────────▶│
 │                  │◀───market info─────────────────────│
 │                  │                 │                  │
 │                  │──pay request───▶│                  │
 │                  │                 │                  │
 │                  │◀─402 Required──│                  │
 │                  │                 │                  │
 │                  │──create pay────▶│                  │
 │                  │                 │                  │
 │                  │◀─pay confirm───│                  │
 │                  │                 │                  │
 │                  │──execute trade─────────────────────▶│
 │                  │                 │                  │
 │                  │◀─confirmation──────────────────────│
 │◀─success────────│                 │                  │
```

## Trade Execution Flow

```
┌──────────────────┐
│  Input URL       │
│  polymarket.com/ │
│  event/xyz       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Extract Slug    │
│  Parse Event ID  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Fetch Market    │
│  Data (Gamma)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Display         │
│  Outcomes &      │
│  Prices          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  User Selects    │
│  Outcome +       │
│  Amount          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Calculate       │
│  x402 Payment    │
│  Requirement     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Verify Balance  │
│  on Base         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Execute x402    │
│  Payment         │
│  (Base Network)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Create & Sign   │
│  Polymarket      │
│  Order           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Submit to CLOB  │
│  (Polygon)       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Confirm Trade   │
│  Execution       │
└──────────────────┘
```

## Network Topology

```
┌───────────────────────────────────────────────────────────────┐
│                      Base Network (EVM)                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  x402 Protocol Layer                                    │  │
│  │  - CDP Facilitator                                      │  │
│  │  - Fee-free USDC settlements                            │  │
│  │  - HTTP 402 Payment Required mechanism                 │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  User Wallet (USDC Balance)                            │  │
│  │  - Signs payment authorizations                         │  │
│  │  - Maintains USDC for x402 payments                    │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              │
                              │ Cross-chain coordination
                              │ (orchestrated by poly402)
                              │
┌───────────────────────────────────────────────────────────────┐
│                     Polygon Network (EVM)                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Polymarket CLOB                                        │  │
│  │  - Central Limit Order Book                             │  │
│  │  - Conditional Token Framework (CTF)                    │  │
│  │  - Order matching and settlement                        │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  User Wallet/Proxy (USDC Balance)                      │  │
│  │  - Signs trade orders                                   │  │
│  │  - Holds position tokens                                │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## Features

- **HTTP Payment Protocol Integration**: Leverages x402 for programmatic USDC payments on Base
- **Prediction Market Trading**: Direct integration with Polymarket CLOB API
- **CLI Interface**: Simple command-line tool for market discovery and trade execution
- **Self-Hosted**: Users maintain control of wallets and private keys
- **Multi-Chain**: Coordinates operations across Base (payments) and Polygon (trades)
- **Non-Custodial**: All transactions signed by user's private keys
- **Autonomous-Ready**: Designed for both human and AI agent usage

## Installation

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- USDC balance on Base network (for x402 payments)
- USDC balance on Polygon network (for Polymarket trades)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/poly402.git
cd poly402

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Install the CLI tool
pip install -e .
```

## Configuration

### Initialize Configuration

```bash
poly402 init
```

This will create a configuration file at `~/.poly402/config.json` and prompt for:

1. **Base Network Wallet**
   - Private key for x402 payments on Base
   - Will be used to sign payment authorizations

2. **Polygon Network Wallet**
   - Private key for Polymarket trades on Polygon
   - Will be used to sign trade orders

3. **Polymarket API Credentials**
   - Can be generated after wallet setup
   - Used for authenticated CLOB API access

4. **Network RPC Endpoints** (optional)
   - Base RPC URL (defaults to public endpoint)
   - Polygon RPC URL (defaults to public endpoint)

### Configuration File Structure

```json
{
  "networks": {
    "base": {
      "rpc_url": "https://mainnet.base.org",
      "chain_id": 8453,
      "wallet_private_key": "0x..."
    },
    "polygon": {
      "rpc_url": "https://polygon-rpc.com",
      "chain_id": 137,
      "wallet_private_key": "0x..."
    }
  },
  "polymarket": {
    "clob_endpoint": "https://clob.polymarket.com",
    "gamma_endpoint": "https://gamma-api.polymarket.com",
    "api_key": "generated-after-setup",
    "api_secret": "generated-after-setup",
    "api_passphrase": "generated-after-setup"
  },
  "x402": {
    "facilitator": "https://x402.coinbase.com",
    "max_payment_amount": "100.00"
  }
}
```

### Security Considerations

- Configuration file contains private keys - store securely
- Use environment variables in production: `POLY402_BASE_KEY`, `POLY402_POLYGON_KEY`
- Never commit configuration files to version control
- Consider using hardware wallets for high-value operations

## Usage

### View Available Markets

```bash
# Fetch market details from Polymarket URL
poly402 markets --url https://polymarket.com/event/fed-decision-in-october

# Output:
# Market: Fed Decision in October
# Outcomes:
#   [0] Cut 25 basis points - Price: 0.65 USDC (65% probability)
#   [1] Cut 50 basis points - Price: 0.30 USDC (30% probability)
#   [2] No change - Price: 0.05 USDC (5% probability)
```

### Execute a Trade

```bash
# Place a bet on outcome 0 with 10 USDC
poly402 trade \
  --url https://polymarket.com/event/fed-decision-in-october \
  --outcome 0 \
  --amount 10

# Process:
# 1. Parsing market data...
# 2. Verifying x402 payment requirement (10.00 USDC on Base)...
# 3. Executing payment on Base network...
# 4. Payment confirmed: 0x123abc...
# 5. Creating Polymarket order...
# 6. Signing order with Polygon wallet...
# 7. Submitting to CLOB...
# 8. Trade executed successfully!
#    Order ID: 0x456def...
#    Shares purchased: 15.38 @ 0.65 USDC
#    Network: Polygon
#    Status: Filled
```

### Check Balances

```bash
poly402 balance

# Output:
# Base Network (x402 Payments):
#   USDC: 250.00
#   Address: 0x1234...5678
#
# Polygon Network (Polymarket):
#   USDC: 180.00
#   Position Tokens: 3 markets
#   Address: 0xabcd...ef01
```

### View Trade History

```bash
poly402 history --limit 10

# Output:
# Recent Trades:
# 1. 2025-10-28 21:00 - Fed Decision in October
#    Outcome: Cut 25 basis points
#    Amount: 10.00 USDC → 15.38 shares
#    Status: Filled
#    Tx: 0x456def...
#
# 2. 2025-10-27 14:30 - NYC Mayoral Election
#    Outcome: Eric Adams
#    Amount: 25.00 USDC → 50.00 shares
#    Status: Filled
#    Tx: 0x789ghi...
```

### Advanced Usage

#### Custom Price Limits

```bash
# Set maximum price willing to pay per share
poly402 trade \
  --url https://polymarket.com/event/btc-100k \
  --outcome "Yes" \
  --amount 50 \
  --max-price 0.75
```

#### Batch Trading

```bash
# Trade on multiple outcomes in a single session
poly402 batch-trade --config trades.json
```

trades.json:
```json
[
  {
    "url": "https://polymarket.com/event/event-1",
    "outcome": 0,
    "amount": 10
  },
  {
    "url": "https://polymarket.com/event/event-2",
    "outcome": "Yes",
    "amount": 20
  }
]
```

## Technical Deep Dive

### x402 Payment Protocol

x402 revives the HTTP 402 Payment Required status code for programmatic payments:

1. **Initial Request**: Client attempts to access a paid resource
2. **402 Response**: Server responds with payment requirements in headers
3. **Payment Creation**: Client signs a payment authorization onchain
4. **Payment Verification**: Facilitator verifies and settles the payment
5. **Resource Access**: Client retries request with payment proof, gains access

poly402 acts as both an x402 buyer (for hypothetical paid Polymarket services) and could expose x402-gated trading endpoints.

### Polymarket CLOB Integration

Polymarket uses a Central Limit Order Book (CLOB) model:

**Authentication Levels:**
- **L1 (Private Key)**: Signs orders and creates API credentials
- **L2 (API Key)**: Authenticates API requests via HMAC signatures

**Order Types:**
- **GTC (Good-Til-Cancelled)**: Limit order active until filled or cancelled
- **GTD (Good-Til-Date)**: Limit order with expiration timestamp
- **FOK (Fill-Or-Kill)**: Market order that must fill completely immediately
- **FAK (Fill-And-Kill)**: Market order that fills partial amounts

**Order Structure:**
```typescript
{
  salt: number,              // Random nonce for uniqueness
  maker: string,             // Maker address (funder)
  signer: string,            // Signing address
  taker: string,             // Taker address (operator)
  tokenId: string,           // ERC1155 token ID
  makerAmount: string,       // Max maker spend
  takerAmount: string,       // Min taker payment
  expiration: string,        // Unix timestamp
  nonce: string,             // Maker's exchange nonce
  feeRateBps: string,        // Fee in basis points
  side: "BUY" | "SELL",      // Order side
  signatureType: number,     // Signature type enum
  signature: string          // Hex encoded signature
}
```

### Market Data Fetching

Markets are retrieved via the Gamma API:

```bash
# By Slug (direct URL mapping)
GET https://gamma-api.polymarket.com/events/slug/{slug}

# By Tags (category filtering)
GET https://gamma-api.polymarket.com/events?tag_id=100381&closed=false

# All Active Markets
GET https://gamma-api.polymarket.com/events?order=id&ascending=false&closed=false
```

### Signing and Security

**Payment Signatures (x402 on Base):**
```typescript
// EIP-712 typed data signing
domain = {
  name: "ClobAuthDomain",
  version: "1",
  chainId: 8453  // Base
}

types = {
  ClobAuth: [
    { name: "address", type: "address" },
    { name: "timestamp", type: "string" },
    { name: "nonce", type: "uint256" },
    { name: "message", type: "string" }
  ]
}
```

**Trade Signatures (Polymarket on Polygon):**
```python
# Order signing for CLOB submission
from eth_account import Account
from eth_account.messages import encode_structured_data

order_data = {...}  # Order structure
message = encode_structured_data(order_data)
signed = Account.sign_message(message, private_key)
```

### Error Handling

**x402 Payment Errors:**
- `INSUFFICIENT_BALANCE`: Not enough USDC on Base
- `PAYMENT_REJECTED`: Facilitator rejected payment
- `AMOUNT_EXCEEDED`: Payment exceeds configured maximum

**Polymarket Trading Errors:**
- `INVALID_ORDER_MIN_SIZE`: Order below minimum size
- `NOT_ENOUGH_BALANCE`: Insufficient USDC on Polygon
- `FOK_ORDER_NOT_FILLED`: Fill-or-kill order couldn't fill completely
- `MARKET_NOT_READY`: Market not accepting orders yet

### State Management

```
┌─────────────┐
│   PENDING   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     Payment Failed
│  PAYING     │────────────────────┐
└──────┬──────┘                    │
       │                           │
       │ Payment Confirmed         ▼
       ▼                    ┌─────────────┐
┌─────────────┐             │   FAILED    │
│  TRADING    │             └─────────────┘
└──────┬──────┘
       │
       │ Trade Confirmed
       ▼
┌─────────────┐
│  COMPLETED  │
└─────────────┘
```

## API Reference

### Python API

```python
from poly402 import Poly402Client

# Initialize client
client = Poly402Client(config_path="~/.poly402/config.json")

# Fetch market data
market = client.get_market("https://polymarket.com/event/xyz")
print(f"Outcomes: {market.outcomes}")
print(f"Prices: {market.prices}")

# Execute trade
result = client.execute_trade(
    market_url="https://polymarket.com/event/xyz",
    outcome_index=0,
    amount_usdc=10.0,
    max_price=0.75  # Optional
)

print(f"Order ID: {result.order_id}")
print(f"Status: {result.status}")
print(f"Shares: {result.shares_purchased}")
```

### TypeScript x402 Integration

```typescript
import { wrapFetchWithPayment } from 'x402-fetch';
import { privateKeyToAccount } from 'viem/accounts';

// Create wallet client
const account = privateKeyToAccount(process.env.BASE_PRIVATE_KEY);

// Wrap fetch with payment handling
const fetchWithPayment = wrapFetchWithPayment(fetch, account);

// Make paid request (402 handled automatically)
const response = await fetchWithPayment('https://api.service.com/data', {
  method: 'GET'
});

const data = await response.json();
```

## Development

### Project Structure

```
poly402/
├── cli.py                      # Main CLI entry point
├── setup.py                    # Python package configuration
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
├── src/
│   ├── python/
│   │   ├── __init__.py
│   │   ├── polymarket_client.py    # Polymarket API wrapper
│   │   ├── market_parser.py        # URL parsing and data extraction
│   │   ├── wallet_manager.py       # Multi-chain wallet handling
│   │   ├── config.py               # Configuration management
│   │   └── orchestrator.py         # Payment + trade coordination
│   ├── typescript/
│   │   ├── x402_handler.ts         # x402 payment logic
│   │   ├── bridge.ts               # Python-TS interop
│   │   └── types.ts                # TypeScript definitions
│   └── core/
│       ├── validator.py            # Input validation
│       └── logger.py               # Logging utilities
├── tests/
│   ├── test_polymarket.py
│   ├── test_x402.py
│   ├── test_orchestrator.py
│   └── integration/
│       └── test_full_flow.py
├── examples/
│   ├── basic_trade.py
│   ├── batch_trading.py
│   └── custom_strategies.py
└── docs/
    ├── INSTALLATION.md
    ├── API_REFERENCE.md
    ├── SECURITY.md
    └── TROUBLESHOOTING.md
```

### Running Tests

```bash
# Python tests
pytest tests/

# Integration tests (requires testnet funds)
pytest tests/integration/ --testnet

# TypeScript tests
npm test
```

### Building Documentation

```bash
# Generate API documentation
pdoc src/python --html --output-dir docs/api

# Generate diagrams from source
python scripts/generate_diagrams.py
```

## Deployment

### Self-Hosted Deployment

1. **Server Setup**
```bash
# Install on Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.9 python3-pip nodejs npm

# Clone and install
git clone https://github.com/yourusername/poly402.git
cd poly402
pip install -r requirements.txt
npm install
pip install -e .
```

2. **Configuration**
```bash
# Create config directory
mkdir -p ~/.poly402

# Copy and edit config template
cp config.template.json ~/.poly402/config.json
nano ~/.poly402/config.json
```

3. **Environment Variables**
```bash
export POLY402_BASE_KEY="your-base-private-key"
export POLY402_POLYGON_KEY="your-polygon-private-key"
export POLY402_CONFIG_PATH="~/.poly402/config.json"
```

4. **Run as Service** (systemd)
```ini
[Unit]
Description=poly402 Trading Service
After=network.target

[Service]
Type=simple
User=poly402
WorkingDirectory=/opt/poly402
ExecStart=/usr/local/bin/poly402 daemon
Restart=always
Environment="POLY402_CONFIG_PATH=/etc/poly402/config.json"

[Install]
WantedBy=multi-user.target
```

### Docker Deployment

```bash
# Build image
docker build -t poly402 .

# Run container
docker run -d \
  -v ~/.poly402:/root/.poly402 \
  -e POLY402_BASE_KEY=$BASE_KEY \
  -e POLY402_POLYGON_KEY=$POLYGON_KEY \
  poly402
```

## Troubleshooting

### Common Issues

**Issue: "Insufficient balance on Base network"**
- Ensure your Base wallet has enough USDC for x402 payments
- Check balance: `poly402 balance`
- Bridge USDC to Base: Use official Base bridge

**Issue: "Polymarket API authentication failed"**
- Regenerate API credentials: `poly402 init --reset-api-keys`
- Verify wallet address matches Polymarket account
- Check API key expiration

**Issue: "Order rejected: INVALID_ORDER_MIN_SIZE"**
- Polymarket has minimum order sizes (typically 1 USDC)
- Increase your trade amount
- Check market-specific requirements

**Issue: "Cross-chain coordination timeout"**
- Payment confirmed on Base but trade failed on Polygon
- Check Polygon network status
- Verify USDC balance on Polygon
- Review transaction logs: `poly402 logs --level debug`

### Debug Mode

```bash
# Enable verbose logging
poly402 --debug trade --url <url> --outcome 0 --amount 10

# View detailed logs
poly402 logs --tail 100 --level debug

# Export logs for support
poly402 logs --export support_request.log
```

## Security Best Practices

1. **Private Key Management**
   - Use hardware wallets for large balances
   - Never share private keys or commit to version control
   - Rotate keys periodically
   - Use separate wallets for testing vs production

2. **Transaction Limits**
   - Set `max_payment_amount` in config to limit x402 exposure
   - Configure per-trade limits
   - Enable transaction confirmations for large amounts

3. **Network Security**
   - Use trusted RPC endpoints
   - Verify SSL certificates
   - Monitor for abnormal transaction patterns

4. **Operational Security**
   - Run in isolated environment
   - Keep dependencies updated
   - Monitor wallet balances regularly
   - Enable 2FA where possible

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/poly402.git
cd poly402

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -r requirements-dev.txt
npm install

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
npm test
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- [Coinbase x402 Protocol](https://docs.cdp.coinbase.com/x402/welcome) - Payment protocol implementation
- [Polymarket](https://polymarket.com) - Prediction market platform
- [Polymarket CLOB API](https://docs.polymarket.com) - Trading infrastructure

## Disclaimer

This software is provided as-is for educational and research purposes. Users are responsible for:
- Understanding the risks of prediction market trading
- Complying with local regulations regarding prediction markets
- Securing their private keys and funds
- Any financial losses incurred through usage

poly402 is not affiliated with, endorsed by, or sponsored by Coinbase or Polymarket.

---

Built with x402 payment protocol and Polymarket API
