# Installation Guide

Complete installation instructions for poly402.

## Prerequisites

### System Requirements

- Python 3.9 or higher
- Node.js 18 or higher
- Git
- USDC on Base network (for x402 payments)
- USDC on Polygon network (for Polymarket trades)

### Wallet Requirements

You'll need two Ethereum-compatible wallets:
1. **Base Network Wallet**: For x402 payment authorizations
2. **Polygon Network Wallet**: For Polymarket trade execution

You can use:
- The same private key for both networks (simplest)
- Different private keys for separation of concerns
- Hardware wallet integration (advanced)

## Installation Methods

### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/poly402.git
cd poly402

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Install poly402 CLI
pip install -e .

# Verify installation
poly402 --version
```

### Method 2: Install via pip (Future)

```bash
pip install poly402
```

### Method 3: Docker

```bash
# Build Docker image
docker build -t poly402 .

# Run with config volume
docker run -v ~/.poly402:/root/.poly402 poly402 balance
```

## Configuration

### Initial Setup

```bash
poly402 init
```

You'll be prompted for:
1. Base network private key
2. Polygon network private key

The configuration will be saved to `~/.poly402/config.json`.

### Environment Variables (Alternative)

Instead of storing keys in the config file, you can use environment variables:

```bash
export POLY402_BASE_KEY="0x..."
export POLY402_POLYGON_KEY="0x..."
```

### Configuration File Location

Default: `~/.poly402/config.json`

Custom location:
```python
from poly402 import Poly402Client

client = Poly402Client(config_path="/custom/path/config.json")
```

## Funding Your Wallets

### Base Network (for x402 payments)

1. Bridge USDC to Base network using:
   - [Official Base Bridge](https://bridge.base.org)
   - [Coinbase](https://www.coinbase.com) (direct Base withdrawal)

2. Verify balance:
```bash
poly402 balance
```

### Polygon Network (for Polymarket trades)

1. Get USDC on Polygon:
   - Bridge from Ethereum using [Polygon Bridge](https://wallet.polygon.technology/bridge)
   - Use Polymarket's built-in deposit methods
   - Exchange services that support Polygon withdrawals

2. Verify balance:
```bash
poly402 balance
```

### Recommended Starting Amounts

- **Base**: 50-100 USDC (for x402 payment authorizations)
- **Polygon**: 100-500 USDC (for actual trades)

## Verification

### Test Installation

```bash
# Check version
poly402 --version

# View configuration
poly402 config-path

# Check balances
poly402 balance

# List active markets
poly402 active --limit 5
```

### Test Market Lookup

```bash
poly402 markets --url https://polymarket.com/event/fed-decision-in-october
```

## Troubleshooting

### Issue: "poly402 command not found"

Solution:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall in development mode
pip install -e .
```

### Issue: "Configuration file not found"

Solution:
```bash
# Run init to create config
poly402 init
```

### Issue: "Failed to connect to RPC"

Solution:
- Check your internet connection
- Try alternative RPC endpoints in config.json
- Use custom RPC providers (Alchemy, Infura)

### Issue: "Insufficient balance"

Solution:
- Verify you have USDC on the correct networks
- Check balances: `poly402 balance`
- Fund wallets as described above

## Upgrading

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt
npm install

# Reinstall CLI
pip install -e .
```

## Uninstalling

```bash
# Remove poly402
pip uninstall poly402

# Remove configuration (optional)
rm -rf ~/.poly402

# Remove virtual environment
rm -rf venv
```

## Next Steps

After installation:
1. Fund your wallets with USDC
2. Review the [API Reference](API_REFERENCE.md)
3. Try the [basic trading example](../examples/basic_trade.py)
4. Read the [Security Best Practices](SECURITY.md)
