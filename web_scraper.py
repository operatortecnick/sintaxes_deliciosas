"""
Web scraper for additional stock data sources
Uses web scraping as a fallback when APIs are not available
"""
import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Dict, List, Optional, Any
from config import APIConfig


class StockScraper:
    """Web scraper for stock data from public websites"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_yahoo_finance_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Scrape stock quote from Yahoo Finance website
        Fallback method when API fails
        """
        try:
            url = f'https://finance.yahoo.com/quote/{symbol}'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract price from the page
            price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if not price_element:
                # Try alternative selector
                price_element = soup.find('span', {'data-reactid': re.compile(r'.*')})
            
            price = None
            if price_element:
                price_text = price_element.get_text().strip()
                try:
                    price = float(price_text.replace(',', ''))
                except ValueError:
                    pass
            
            # Extract additional data
            change_element = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
            change = None
            if change_element:
                change_text = change_element.get_text().strip()
                try:
                    change = float(change_text.replace(',', '').replace('+', ''))
                except ValueError:
                    pass
            
            # Extract volume
            volume_element = soup.find('td', {'data-test': 'VOLUME-value'})
            volume = None
            if volume_element:
                volume_text = volume_element.get_text().strip()
                try:
                    # Handle volume formatting (e.g., "1.2M" -> 1200000)
                    if 'M' in volume_text:
                        volume = float(volume_text.replace('M', '').replace(',', '')) * 1000000
                    elif 'K' in volume_text:
                        volume = float(volume_text.replace('K', '').replace(',', '')) * 1000
                    else:
                        volume = float(volume_text.replace(',', ''))
                except ValueError:
                    pass
            
            return {
                'status': 'success',
                'symbol': symbol,
                'price': price,
                'change': change,
                'volume': volume,
                'source': 'yahoo_scraper'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Scraping failed: {str(e)}',
                'source': 'yahoo_scraper'
            }
    
    def scrape_google_finance(self, symbol: str) -> Dict[str, Any]:
        """
        Scrape stock data from Google Finance
        Alternative data source
        """
        try:
            # Google Finance uses a different URL format
            url = f'https://www.google.com/finance/quote/{symbol}:NASDAQ'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract price
            price_element = soup.find('div', {'class': re.compile(r'.*YMlKec.*')})
            price = None
            if price_element:
                price_text = price_element.get_text().strip().replace('$', '').replace(',', '')
                try:
                    price = float(price_text)
                except ValueError:
                    pass
            
            return {
                'status': 'success' if price else 'partial',
                'symbol': symbol,
                'price': price,
                'source': 'google_scraper'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Google Finance scraping failed: {str(e)}',
                'source': 'google_scraper'
            }
    
    def scrape_marketwatch(self, symbol: str) -> Dict[str, Any]:
        """
        Scrape stock data from MarketWatch
        Another alternative source
        """
        try:
            url = f'https://www.marketwatch.com/investing/stock/{symbol}'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract price
            price_element = soup.find('bg-quote', {'field': 'Last'})
            if not price_element:
                price_element = soup.find('span', {'class': 'value'})
            
            price = None
            if price_element:
                price_text = price_element.get_text().strip().replace('$', '').replace(',', '')
                try:
                    price = float(price_text)
                except ValueError:
                    pass
            
            return {
                'status': 'success' if price else 'partial',
                'symbol': symbol,
                'price': price,
                'source': 'marketwatch_scraper'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'MarketWatch scraping failed: {str(e)}',
                'source': 'marketwatch_scraper'
            }
    
    def multi_source_scrape(self, symbol: str) -> Dict[str, Any]:
        """
        Try multiple scraping sources for redundancy
        Returns the first successful result
        """
        sources = [
            self.scrape_yahoo_finance_quote,
            self.scrape_google_finance,
            self.scrape_marketwatch
        ]
        
        results = []
        
        for scraper in sources:
            try:
                result = scraper(symbol)
                results.append(result)
                
                if result.get('status') == 'success' and result.get('price'):
                    return result
                
                # Add delay between requests to be respectful
                time.sleep(1)
                
            except Exception as e:
                results.append({
                    'status': 'error',
                    'message': str(e),
                    'source': scraper.__name__
                })
        
        # If no successful result, return the best partial result or first error
        for result in results:
            if result.get('status') == 'partial':
                return result
        
        return results[0] if results else {
            'status': 'error',
            'message': 'All scraping sources failed'
        }
    
    def scrape_crypto_prices(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Scrape cryptocurrency prices from CoinGecko (public data)
        Bonus feature for crypto enthusiasts
        """
        try:
            # CoinGecko has a public API that doesn't require keys
            symbols_str = ','.join(symbols).lower()
            url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbols_str}&vs_currencies=usd'
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = {}
            for symbol in symbols:
                if symbol.lower() in data:
                    results[symbol.upper()] = {
                        'price': data[symbol.lower()].get('usd'),
                        'currency': 'USD',
                        'source': 'coingecko_api'
                    }
                else:
                    results[symbol.upper()] = {
                        'status': 'error',
                        'message': 'Symbol not found'
                    }
            
            return {
                'status': 'success',
                'data': results,
                'source': 'coingecko_api'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Crypto scraping failed: {str(e)}',
                'source': 'coingecko_api'
            }
    
    def get_trending_stocks(self) -> List[Dict[str, Any]]:
        """
        Scrape trending/popular stocks from financial websites
        """
        try:
            # Try to get trending from Yahoo Finance
            url = 'https://finance.yahoo.com/trending-tickers'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            trending = []
            # Look for stock symbol links
            links = soup.find_all('a', href=re.compile(r'/quote/[A-Z]+'))
            
            for link in links[:10]:  # Limit to top 10
                href = link.get('href', '')
                symbol_match = re.search(r'/quote/([A-Z]+)', href)
                if symbol_match:
                    symbol = symbol_match.group(1)
                    name = link.get_text().strip()
                    trending.append({
                        'symbol': symbol,
                        'name': name,
                        'source': 'yahoo_trending'
                    })
            
            return trending
            
        except Exception as e:
            # Return some popular stocks as fallback
            return [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'source': 'fallback'},
                {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'source': 'fallback'},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'source': 'fallback'},
                {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'source': 'fallback'},
                {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'source': 'fallback'}
            ]