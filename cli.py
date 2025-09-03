#!/usr/bin/env python3
"""
CLI interface for the API Extractor
Provides command-line access to stock and AI APIs
"""
import click
import json
import os
from typing import List
from api_extractor import APIExtractor


@click.group()
@click.option('--config-file', help='Path to configuration file')
@click.pass_context
def cli(ctx, config_file):
    """API Extractor - Extract data from stock and AI APIs"""
    ctx.ensure_object(dict)
    ctx.obj['extractor'] = APIExtractor()


@cli.group()
def stock():
    """Stock market data commands"""
    pass


@cli.group()
def ai():
    """AI/GPT commands"""
    pass


# Stock Commands
@stock.command()
@click.argument('symbol')
@click.option('--period', default='1d', help='Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
@click.option('--output', default='json', type=click.Choice(['json', 'table']), help='Output format')
@click.pass_context
def price(ctx, symbol, period, output):
    """Get stock price and data for a symbol"""
    extractor = ctx.obj['extractor']
    result = extractor.get_stock_price(symbol.upper(), period)
    
    if output == 'json':
        click.echo(json.dumps(result, indent=2))
    else:
        if result.get('status') == 'success':
            click.echo(f"\n📊 Stock Data for {symbol.upper()}")
            click.echo("─" * 40)
            click.echo(f"Current Price: ${result.get('regularMarketPrice', 'N/A')}")
            click.echo(f"Previous Close: ${result.get('previousClose', 'N/A')}")
            click.echo(f"Day High: ${result.get('regularMarketDayHigh', 'N/A')}")
            click.echo(f"Day Low: ${result.get('regularMarketDayLow', 'N/A')}")
            click.echo(f"Volume: {result.get('regularMarketVolume', 'N/A'):,}")
            click.echo(f"Currency: {result.get('currency', 'N/A')}")
            click.echo(f"Exchange: {result.get('exchangeName', 'N/A')}")
        else:
            click.echo(f"❌ Error: {result.get('message', 'Unknown error')}")


@stock.command()
@click.argument('query')
@click.option('--limit', default=5, help='Maximum number of results')
@click.pass_context
def search(ctx, query, limit):
    """Search for stocks by name or symbol"""
    extractor = ctx.obj['extractor']
    results = extractor.search_stocks(query)
    
    if results and not results[0].get('status') == 'error':
        click.echo(f"\n🔍 Search Results for '{query}'")
        click.echo("─" * 50)
        for i, stock in enumerate(results[:limit]):
            click.echo(f"{i+1}. {stock.get('symbol', 'N/A')} - {stock.get('shortname', 'N/A')}")
            if stock.get('exchDisp'):
                click.echo(f"   Exchange: {stock.get('exchDisp')}")
            if stock.get('sector'):
                click.echo(f"   Sector: {stock.get('sector')}")
            click.echo()
    else:
        click.echo(f"❌ No results found for '{query}'")


@stock.command()
@click.argument('symbols', nargs=-1, required=True)
@click.pass_context
def portfolio(ctx, symbols):
    """Get portfolio summary for multiple stocks"""
    extractor = ctx.obj['extractor']
    result = extractor.get_portfolio_summary(list(symbols))
    
    click.echo(f"\n📈 Portfolio Summary")
    click.echo("─" * 40)
    click.echo(f"Total Stocks: {result['total_stocks']}")
    click.echo(f"Successful: {result['successful_fetches']}")
    click.echo(f"Failed: {result['failed_fetches']}")
    click.echo()
    
    for symbol, data in result['stocks'].items():
        if 'error' not in data:
            price = data.get('price', 0)
            change = data.get('change', 0)
            change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            click.echo(f"{symbol}: ${price:.2f} {change_symbol} ({change:+.2f})")
        else:
            click.echo(f"{symbol}: ❌ {data['error']}")


@stock.command()
@click.argument('symbols', nargs=-1, required=True)
@click.pass_context
def crypto(ctx, symbols):
    """Get cryptocurrency prices"""
    extractor = ctx.obj['extractor']
    result = extractor.get_crypto_prices(list(symbols))
    
    if result.get('status') == 'success':
        click.echo(f"\n💰 Cryptocurrency Prices")
        click.echo("─" * 30)
        for symbol, data in result['data'].items():
            if 'price' in data:
                click.echo(f"{symbol}: ${data['price']:.2f}")
            else:
                click.echo(f"{symbol}: ❌ {data.get('message', 'Error')}")
    else:
        click.echo(f"❌ Error: {result.get('message', 'Unknown error')}")


@stock.command()
@click.pass_context
def trending(ctx):
    """Get trending stocks"""
    extractor = ctx.obj['extractor']
    trending = extractor.get_trending_stocks()
    
    click.echo(f"\n📈 Trending Stocks")
    click.echo("─" * 25)
    for i, stock in enumerate(trending[:10]):
        symbol = stock.get('symbol', 'N/A')
        name = stock.get('name', 'N/A')
        source = stock.get('source', '')
        click.echo(f"{i+1:2d}. {symbol:6s} - {name}")


@stock.command()
@click.argument('symbol')
@click.option('--scraper', is_flag=True, help='Force use of web scraper')
@click.pass_context
def fallback(ctx, symbol, scraper):
    """Get stock data with comprehensive fallback"""
    extractor = ctx.obj['extractor']
    
    if scraper:
        result = extractor.get_stock_price(symbol.upper(), use_scraper=True)
    else:
        result = extractor.get_stock_with_fallback(symbol.upper())
    
    if result.get('status') == 'success':
        # Handle different result formats
        price = result.get('regularMarketPrice') or result.get('price', 'N/A')
        method = result.get('method_used', result.get('source', 'Unknown'))
        
        click.echo(f"\n📊 Stock Data for {symbol.upper()}")
        click.echo("─" * 40)
        click.echo(f"Price: ${price}")
        click.echo(f"Method: {method}")
        
        if result.get('change'):
            change = result.get('change')
            change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            click.echo(f"Change: {change_symbol} {change:+.2f}")
    else:
        click.echo(f"❌ Error: {result.get('message', 'Unknown error')}")


# AI Commands
@ai.command()
@click.argument('question')
@click.option('--provider', default='auto', help='AI provider (auto, huggingface, openrouter, together)')
@click.pass_context
def ask(ctx, question, provider):
    """Ask a question to AI"""
    extractor = ctx.obj['extractor']
    result = extractor.ask_ai(question, provider)
    
    if result.get('status') == 'success':
        # Extract response text from different provider formats
        response_text = ""
        if 'result' in result:
            if isinstance(result['result'], list) and len(result['result']) > 0:
                # Hugging Face format
                if 'generated_text' in result['result'][0]:
                    response_text = result['result'][0]['generated_text']
                else:
                    response_text = str(result['result'][0])
            elif isinstance(result['result'], dict):
                # OpenRouter/Together format
                if 'choices' in result['result'] and len(result['result']['choices']) > 0:
                    choice = result['result']['choices'][0]
                    if 'message' in choice:
                        response_text = choice['message'].get('content', '')
                    else:
                        response_text = choice.get('text', '')
        
        if not response_text:
            response_text = str(result.get('result', 'No response'))
        
        click.echo(f"\n🤖 AI Response ({result.get('provider', provider)}):")
        click.echo("─" * 50)
        click.echo(response_text)
    else:
        click.echo(f"❌ Error: {result.get('message', 'Unknown error')}")


@ai.command()
@click.argument('prompt')
@click.option('--max-tokens', default=100, help='Maximum tokens to generate')
@click.pass_context
def generate(ctx, prompt, max_tokens):
    """Generate text completion"""
    extractor = ctx.obj['extractor']
    result = extractor.generate_text(prompt, max_tokens)
    
    if result.get('status') == 'success':
        if 'result' in result and isinstance(result['result'], list):
            generated = result['result'][0].get('generated_text', '')
            click.echo(f"\n✨ Generated Text:")
            click.echo("─" * 30)
            click.echo(generated)
    else:
        click.echo(f"❌ Error: {result.get('message', 'Unknown error')}")


@ai.command()
@click.pass_context
def models(ctx):
    """List available free AI models"""
    extractor = ctx.obj['extractor']
    models = extractor.ai_extractor.get_free_models()
    
    click.echo("\n🤖 Available Free AI Models")
    click.echo("─" * 40)
    
    for provider, model_list in models.items():
        click.echo(f"\n{provider.upper()}:")
        for model in model_list:
            click.echo(f"  • {model}")


# Combined Commands
@cli.command()
@click.argument('symbol')
@click.option('--analysis', default='summary', type=click.Choice(['summary', 'prediction', 'risk']), 
              help='Type of analysis')
@click.pass_context
def analyze(ctx, symbol, analysis):
    """Analyze stock with AI"""
    extractor = ctx.obj['extractor']
    result = extractor.analyze_stock_with_ai(symbol.upper(), analysis)
    
    if result.get('status') == 'success':
        stock_data = result['stock_data']
        ai_analysis = result['ai_analysis']
        
        click.echo(f"\n📊 Stock Analysis for {symbol.upper()}")
        click.echo("─" * 50)
        click.echo(f"Current Price: ${stock_data.get('regularMarketPrice', 'N/A')}")
        click.echo(f"Previous Close: ${stock_data.get('previousClose', 'N/A')}")
        
        if ai_analysis.get('status') == 'success':
            # Extract AI response
            ai_text = ""
            if 'result' in ai_analysis:
                if isinstance(ai_analysis['result'], list):
                    ai_text = ai_analysis['result'][0].get('generated_text', '')
                elif isinstance(ai_analysis['result'], dict) and 'choices' in ai_analysis['result']:
                    ai_text = ai_analysis['result']['choices'][0]['message'].get('content', '')
            
            click.echo(f"\n🤖 AI Analysis ({analysis}):")
            click.echo("─" * 30)
            click.echo(ai_text)
        else:
            click.echo(f"\n❌ AI Analysis failed: {ai_analysis.get('message', 'Unknown error')}")
    else:
        click.echo(f"❌ Error: {result.get('message', 'Unknown error')}")


@cli.command()
@click.pass_context
def status(ctx):
    """Check API status and configuration"""
    extractor = ctx.obj['extractor']
    status = extractor.get_api_status()
    
    click.echo("\n🔧 API Status")
    click.echo("─" * 30)
    
    click.echo("\nStock APIs:")
    for api, status_text in status['stock_apis'].items():
        status_icon = "✅" if "configured" in status_text or "available" in status_text else "⚠️"
        click.echo(f"  {status_icon} {api}: {status_text}")
    
    click.echo("\nAI APIs:")
    for api, status_text in status['ai_apis'].items():
        status_icon = "✅" if "configured" in status_text else "⚠️"
        click.echo(f"  {status_icon} {api}: {status_text}")
    
    click.echo(f"\nConfiguration:")
    click.echo(f"  • Requests per minute: {status['config']['requests_per_minute']}")
    click.echo(f"  • Retry attempts: {status['config']['retry_attempts']}")


@cli.command()
@click.pass_context
def test(ctx):
    """Test all APIs"""
    extractor = ctx.obj['extractor']
    
    click.echo("\n🧪 Testing APIs...")
    results = extractor.test_apis()
    
    click.echo("\nTest Results:")
    click.echo("─" * 20)
    for api, status in results.items():
        status_icon = "✅" if status == "working" else "❌"
        click.echo(f"  {status_icon} {api}: {status}")


if __name__ == '__main__':
    cli()