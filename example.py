#!/usr/bin/env python3
"""
Example usage of the API Extractor
"""
import os
import json
from api_extractor import APIExtractor


def main():
    print("🚀 API Extractor - Example Usage")
    print("=" * 50)
    
    # Initialize the extractor
    extractor = APIExtractor()
    
    # Test API status
    print("\n📋 Checking API Status...")
    status = extractor.get_api_status()
    print(f"Stock APIs available: {len([k for k, v in status['stock_apis'].items() if 'available' in v or 'configured' in v])}")
    print(f"AI APIs available: {len([k for k, v in status['ai_apis'].items() if 'configured' in v or 'limited' in v])}")
    
    # Example 1: Get stock data
    print("\n📊 Example 1: Stock Data")
    print("-" * 30)
    
    stocks = ['AAPL', 'GOOGL', 'TSLA']
    for symbol in stocks:
        print(f"\nGetting data for {symbol}...")
        result = extractor.get_stock_price(symbol)
        
        if result.get('status') == 'success':
            price = result.get('regularMarketPrice', 'N/A')
            prev_close = result.get('previousClose', 'N/A')
            print(f"✅ {symbol}: ${price} (Previous: ${prev_close})")
        else:
            print(f"❌ {symbol}: {result.get('message', 'Error')}")
    
    # Example 2: Search stocks
    print("\n🔍 Example 2: Stock Search")
    print("-" * 30)
    search_results = extractor.search_stocks("Apple")
    if search_results:
        print(f"Found {len(search_results)} results for 'Apple':")
        for i, stock in enumerate(search_results[:3]):
            print(f"  {i+1}. {stock.get('symbol')} - {stock.get('shortname')}")
    
    # Example 3: AI Chat
    print("\n🤖 Example 3: AI Chat")
    print("-" * 30)
    
    questions = [
        "What is Python?",
        "Explain machine learning in simple terms",
        "What are the benefits of investing in stocks?"
    ]
    
    for question in questions:
        print(f"\nAsking: {question}")
        result = extractor.ask_ai(question)
        
        if result.get('status') == 'success':
            # Extract response based on provider format
            response = ""
            if 'result' in result:
                if isinstance(result['result'], list) and result['result']:
                    response = result['result'][0].get('generated_text', str(result['result'][0]))
                elif isinstance(result['result'], dict) and 'choices' in result['result']:
                    choice = result['result']['choices'][0]
                    response = choice.get('message', {}).get('content', choice.get('text', ''))
            
            provider = result.get('provider', 'unknown')
            print(f"✅ AI ({provider}): {response[:100]}...")
        else:
            print(f"❌ AI Error: {result.get('message', 'Unknown error')}")
        
        break  # Only try first question to avoid rate limits
    
    # Example 4: Combined Analysis
    print("\n📈 Example 4: Stock Analysis with AI")
    print("-" * 40)
    
    analysis_result = extractor.analyze_stock_with_ai('AAPL', 'summary')
    if analysis_result.get('status') == 'success':
        stock_data = analysis_result['stock_data']
        ai_analysis = analysis_result['ai_analysis']
        
        print(f"Stock: AAPL")
        print(f"Price: ${stock_data.get('regularMarketPrice', 'N/A')}")
        
        if ai_analysis.get('status') == 'success':
            print("AI Analysis available ✅")
        else:
            print(f"AI Analysis failed: {ai_analysis.get('message')}")
    
    # Example 5: Portfolio
    print("\n💼 Example 5: Portfolio Summary")
    print("-" * 35)
    
    portfolio = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    summary = extractor.get_portfolio_summary(portfolio)
    
    print(f"Portfolio: {portfolio}")
    print(f"Successful fetches: {summary['successful_fetches']}/{summary['total_stocks']}")
    
    for symbol, data in summary['stocks'].items():
        if 'error' not in data:
            price = data.get('price', 0)
            change = data.get('change', 0)
            status = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            print(f"  {symbol}: ${price:.2f} {status}")
    
    # Example 6: Trending Stocks
    print("\n📈 Example 6: Trending Stocks")
    print("-" * 35)
    
    trending = extractor.get_trending_stocks()
    print("Top trending stocks:")
    for i, stock in enumerate(trending[:5]):
        print(f"  {i+1}. {stock['symbol']} - {stock['name']}")
    
    # Example 7: Cryptocurrency
    print("\n💰 Example 7: Cryptocurrency Prices")
    print("-" * 40)
    
    crypto_result = extractor.get_crypto_prices(['bitcoin', 'ethereum', 'dogecoin'])
    if crypto_result.get('status') == 'success':
        for symbol, data in crypto_result['data'].items():
            if 'price' in data:
                print(f"  {symbol}: ${data['price']:.2f}")
    else:
        print(f"  Crypto data not available: {crypto_result.get('message', 'Network limited')}")
    
    # Example 8: Fallback System
    print("\n🔄 Example 8: Fallback System")
    print("-" * 35)
    
    fallback_result = extractor.get_stock_with_fallback('TSLA')
    if fallback_result.get('status') == 'success':
        method = fallback_result.get('method_used', 'Unknown')
        price = fallback_result.get('regularMarketPrice') or fallback_result.get('price', 'N/A')
        print(f"TSLA price: ${price}")
        print(f"Retrieved using: {method}")
    else:
        print(f"Fallback failed: {fallback_result.get('message')}")
    
    print("\n✨ Example completed! Use the CLI for interactive usage:")
    print("python cli.py --help")
    print("")
    print("🚀 New commands to try:")
    print("  python cli.py stock trending")
    print("  python cli.py stock crypto bitcoin ethereum")
    print("  python cli.py stock fallback AAPL --scraper")


if __name__ == '__main__':
    main()