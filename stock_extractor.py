"""
Stock Market API Extractor
Supports multiple free APIs for stock data extraction
"""
import requests
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from config import APIConfig, FREE_STOCK_APIS


class StockExtractor:
    """Extract stock market data from various free APIs"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_yahoo_stock_data(self, symbol: str, period: str = '1d') -> Dict[str, Any]:
        """
        Get stock data from Yahoo Finance (free, no API key required)
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            Dict containing stock data
        """
        try:
            url = FREE_STOCK_APIS['yahoo_finance'] + symbol
            params = {
                'period1': self._get_period_timestamp(period)[0],
                'period2': self._get_period_timestamp(period)[1],
                'interval': '1d',
                'includePrePost': 'true',
                'events': 'div,splits'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'chart' in data and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result['meta']
                timestamps = result['timestamp']
                indicators = result['indicators']['quote'][0]
                
                return {
                    'symbol': symbol,
                    'currency': meta.get('currency'),
                    'exchangeName': meta.get('exchangeName'),
                    'regularMarketPrice': meta.get('regularMarketPrice'),
                    'previousClose': meta.get('previousClose'),
                    'regularMarketDayHigh': meta.get('regularMarketDayHigh'),
                    'regularMarketDayLow': meta.get('regularMarketDayLow'),
                    'regularMarketVolume': meta.get('regularMarketVolume'),
                    'timestamps': timestamps,
                    'open': indicators.get('open'),
                    'high': indicators.get('high'),
                    'low': indicators.get('low'),
                    'close': indicators.get('close'),
                    'volume': indicators.get('volume'),
                    'status': 'success'
                }
            else:
                return {'status': 'error', 'message': 'No data found for symbol'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def search_stocks(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for stocks by name or symbol using Yahoo Finance
        
        Args:
            query: Search term (company name or symbol)
            
        Returns:
            List of matching stocks
        """
        try:
            url = FREE_STOCK_APIS['yahoo_search']
            params = {'q': query}
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            quotes = data.get('quotes', [])
            
            results = []
            for quote in quotes[:10]:  # Limit to top 10 results
                results.append({
                    'symbol': quote.get('symbol'),
                    'shortname': quote.get('shortname'),
                    'longname': quote.get('longname'),
                    'exchDisp': quote.get('exchDisp'),
                    'typeDisp': quote.get('typeDisp'),
                    'sector': quote.get('sector'),
                    'industry': quote.get('industry'),
                })
            
            return results
            
        except Exception as e:
            return [{'status': 'error', 'message': str(e)}]
    
    def get_alpha_vantage_data(self, symbol: str, function: str = 'TIME_SERIES_DAILY') -> Dict[str, Any]:
        """
        Get data from Alpha Vantage API (requires free API key)
        
        Args:
            symbol: Stock symbol
            function: API function (TIME_SERIES_DAILY, TIME_SERIES_INTRADAY, etc.)
            
        Returns:
            Dict containing stock data
        """
        if not self.config.alpha_vantage_key:
            return {'status': 'error', 'message': 'Alpha Vantage API key required'}
        
        try:
            url = 'https://www.alphavantage.co/query'
            params = {
                'function': function,
                'symbol': symbol,
                'apikey': self.config.alpha_vantage_key,
                'outputsize': 'compact'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Error Message' in data:
                return {'status': 'error', 'message': data['Error Message']}
            
            if 'Note' in data:
                return {'status': 'error', 'message': 'API rate limit exceeded'}
            
            return {'status': 'success', 'data': data}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_finnhub_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get data from Finnhub API (requires free API key)
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dict containing stock data
        """
        if not self.config.finnhub_key:
            return {'status': 'error', 'message': 'Finnhub API key required'}
        
        try:
            # Get quote data
            quote_url = 'https://finnhub.io/api/v1/quote'
            params = {'symbol': symbol, 'token': self.config.finnhub_key}
            
            response = self.session.get(quote_url, params=params, timeout=30)
            response.raise_for_status()
            
            quote_data = response.json()
            
            # Get company profile
            profile_url = 'https://finnhub.io/api/v1/stock/profile2'
            response = self.session.get(profile_url, params=params, timeout=30)
            profile_data = response.json() if response.ok else {}
            
            return {
                'status': 'success',
                'symbol': symbol,
                'quote': quote_data,
                'profile': profile_data
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get data for multiple stocks using Yahoo Finance
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dict containing data for all symbols
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_yahoo_stock_data(symbol)
            time.sleep(0.1)  # Rate limiting
        
        return results
    
    def _get_period_timestamp(self, period: str) -> tuple:
        """Convert period string to timestamp range"""
        end_time = int(time.time())
        
        period_map = {
            '1d': 1,
            '5d': 5,
            '1mo': 30,
            '3mo': 90,
            '6mo': 180,
            '1y': 365,
            '2y': 730,
            '5y': 1825,
            '10y': 3650,
        }
        
        if period == 'ytd':
            # Year to date
            start_time = int(datetime(datetime.now().year, 1, 1).timestamp())
        elif period == 'max':
            # Maximum available data (10 years)
            start_time = end_time - (3650 * 24 * 60 * 60)
        else:
            days = period_map.get(period, 1)
            start_time = end_time - (days * 24 * 60 * 60)
        
        return start_time, end_time