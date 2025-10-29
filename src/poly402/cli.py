"""
CLI interface for poly402
"""

import click
from colorama import init, Fore, Style
from tabulate import tabulate
from typing import Optional
from .client import Poly402Client
from .config import ConfigManager

# Initialize colorama for cross-platform colored output
init(autoreset=True)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    poly402 - Programmatic Prediction Market Trading via HTTP Payment Protocol
    
    Execute prediction market trades using x402 payments on Base and Polymarket on Polygon.
    """
    pass


@cli.command()
@click.option('--base-key', prompt=True, hide_input=True, help='Base network private key')
@click.option('--polygon-key', prompt=True, hide_input=True, help='Polygon network private key')
def init(base_key: str, polygon_key: str):
    """Initialize poly402 configuration"""
    config_manager = ConfigManager()
    
    if config_manager.exists():
        click.confirm(
            f"{Fore.YELLOW}Configuration already exists at {config_manager.config_path}. Overwrite?{Style.RESET_ALL}",
            abort=True
        )
    
    # Create default config
    config_path = config_manager.create_default()
    
    # Load and update with keys
    import json
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    config['networks']['base']['wallet_private_key'] = base_key
    config['networks']['polygon']['wallet_private_key'] = polygon_key
    
    config_manager.save(config)
    
    click.echo(f"{Fore.GREEN}✓ Configuration created at {config_path}{Style.RESET_ALL}")
    click.echo(f"\n{Fore.CYAN}Next steps:{Style.RESET_ALL}")
    click.echo("  1. Fund your Base wallet with USDC for x402 payments")
    click.echo("  2. Fund your Polygon wallet with USDC for Polymarket trades")
    click.echo("  3. Run: poly402 balance")


@cli.command()
@click.option('--url', required=True, help='Polymarket event URL or slug')
def markets(url: str):
    """View market details and available outcomes"""
    try:
        client = Poly402Client()
        market = client.get_market(url)
        
        click.echo(f"\n{Fore.CYAN}Market: {market.title}{Style.RESET_ALL}")
        if market.description:
            click.echo(f"Description: {market.description[:100]}...")
        click.echo(f"Status: {'Active' if market.active else 'Closed'}")
        if market.end_date:
            click.echo(f"End Date: {market.end_date}")
        if market.volume:
            click.echo(f"Volume: ${market.volume:,.2f}")
        
        # Display outcomes table
        click.echo(f"\n{Fore.YELLOW}Outcomes:{Style.RESET_ALL}")
        table_data = []
        for outcome in market.outcomes:
            table_data.append([
                outcome.index,
                outcome.name,
                f"${outcome.price:.4f}",
                f"{outcome.probability:.2f}%"
            ])
        
        headers = ["Index", "Outcome", "Price (USDC)", "Probability"]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--url', required=True, help='Polymarket event URL')
@click.option('--outcome', required=True, type=int, help='Outcome index to bet on')
@click.option('--amount', required=True, type=float, help='Amount in USDC to wager')
@click.option('--max-price', type=float, help='Maximum price per share')
@click.option('--yes', is_flag=True, help='Skip confirmation prompt')
def trade(url: str, outcome: int, amount: float, max_price: Optional[float], yes: bool):
    """Execute a trade on a prediction market"""
    try:
        client = Poly402Client()
        
        # Fetch market info
        click.echo(f"{Fore.CYAN}Fetching market data...{Style.RESET_ALL}")
        market = client.get_market(url)
        
        if outcome >= len(market.outcomes):
            click.echo(f"{Fore.RED}Error: Invalid outcome index{Style.RESET_ALL}", err=True)
            raise click.Abort()
        
        outcome_obj = market.outcomes[outcome]
        
        # Display trade details
        click.echo(f"\n{Fore.YELLOW}Trade Details:{Style.RESET_ALL}")
        click.echo(f"Market: {market.title}")
        click.echo(f"Outcome: {outcome_obj.name}")
        click.echo(f"Current Price: ${outcome_obj.price:.4f} per share")
        click.echo(f"Amount: ${amount:.2f} USDC")
        
        estimated_shares = amount / outcome_obj.price if outcome_obj.price > 0 else 0
        click.echo(f"Estimated Shares: {estimated_shares:.2f}")
        
        if max_price:
            click.echo(f"Max Price: ${max_price:.4f}")
        
        # Confirm trade
        if not yes:
            click.confirm(
                f"\n{Fore.YELLOW}Execute this trade?{Style.RESET_ALL}",
                abort=True
            )
        
        # Execute trade
        click.echo(f"\n{Fore.CYAN}Executing trade...{Style.RESET_ALL}")
        
        with click.progressbar(length=3, label='Processing') as bar:
            bar.update(1)
            click.echo("  Verifying balances...")
            
            bar.update(1)
            click.echo("  Creating and signing order...")
            
            result = client.execute_trade(
                market_url=url,
                outcome_index=outcome,
                amount_usdc=amount,
                max_price=max_price
            )
            
            bar.update(1)
        
        # Display result
        if result.error:
            click.echo(f"\n{Fore.RED}✗ Trade Failed{Style.RESET_ALL}")
            click.echo(f"Error: {result.error}")
        else:
            click.echo(f"\n{Fore.GREEN}✓ Trade Executed Successfully!{Style.RESET_ALL}")
            click.echo(f"Order ID: {result.order_id}")
            click.echo(f"Shares Purchased: {result.shares_purchased:.2f} @ ${result.price_per_share:.4f}")
            click.echo(f"Status: {result.status.value}")
            click.echo(f"Network: Polygon")
        
    except Exception as e:
        click.echo(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
def balance():
    """Check wallet balances on Base and Polygon"""
    try:
        client = Poly402Client()
        balances = client.get_balance()
        
        click.echo(f"\n{Fore.CYAN}Wallet Balances:{Style.RESET_ALL}\n")
        
        for network, bal in balances.items():
            click.echo(f"{Fore.YELLOW}{bal.network} Network:{Style.RESET_ALL}")
            click.echo(f"  Address: {bal.address}")
            click.echo(f"  USDC: ${bal.usdc_balance:.2f}")
            if bal.native_balance:
                native_symbol = "ETH" if network == "base" else "MATIC"
                click.echo(f"  {native_symbol}: {bal.native_balance:.4f}")
            click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--query', required=True, help='Search query')
@click.option('--limit', default=10, help='Number of results')
def search(query: str, limit: int):
    """Search for prediction markets"""
    try:
        client = Poly402Client()
        markets = client.search_markets(query, limit)
        
        if not markets:
            click.echo(f"{Fore.YELLOW}No markets found{Style.RESET_ALL}")
            return
        
        click.echo(f"\n{Fore.CYAN}Found {len(markets)} market(s):{Style.RESET_ALL}\n")
        
        for market in markets:
            click.echo(f"{Fore.GREEN}• {market.title}{Style.RESET_ALL}")
            click.echo(f"  URL: https://polymarket.com/event/{market.slug}")
            if market.volume:
                click.echo(f"  Volume: ${market.volume:,.2f}")
            click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--limit', default=20, help='Number of markets to display')
def active(limit: int):
    """List active prediction markets"""
    try:
        client = Poly402Client()
        markets = client.get_active_markets(limit)
        
        click.echo(f"\n{Fore.CYAN}Active Markets ({len(markets)}):{Style.RESET_ALL}\n")
        
        table_data = []
        for market in markets[:limit]:
            volume_str = f"${market.volume:,.0f}" if market.volume else "N/A"
            table_data.append([
                market.title[:50] + "..." if len(market.title) > 50 else market.title,
                len(market.outcomes),
                volume_str,
                f"https://polymarket.com/event/{market.slug}"
            ])
        
        headers = ["Market", "Outcomes", "Volume", "URL"]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
def config_path():
    """Display configuration file path"""
    config_manager = ConfigManager()
    click.echo(f"Configuration: {config_manager.config_path}")
    click.echo(f"Exists: {config_manager.exists()}")


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
