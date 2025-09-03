"""
Main API Extractor
Combines stock market and AI API extraction capabilities
"""
import os
from typing import Dict, List, Optional, Any, Union
from dotenv import load_dotenv

from config import APIConfig
from stock_extractor import StockExtractor
from ai_extractor import AIExtractor
from web_scraper import StockScraper


class APIExtractor:
    """
    Main API extractor class that provides unified access to:
    - Stock market data from various free APIs
    - AI/GPT capabilities from free providers
    """
    
    def __init__(self, config: Optional[APIConfig] = None):
        """
        Initialize the API extractor
        
        Args:
            config: APIConfig instance, if None will load from environment
        """
        # Load environment variables
        load_dotenv()
        
        if config is None:
            config = APIConfig.from_env()
        
        self.config = config
        self.stock_extractor = StockExtractor(config)
        self.ai_extractor = AIExtractor(config)
        self.web_scraper = StockScraper(config)
    
    # Stock Market API Methods
    def get_stock_price(self, symbol: str, period: str = '1d', use_scraper: bool = False) -> Dict[str, Any]:
        """
        Get current stock price and data with fallback to web scraping
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Time period for historical data
            use_scraper: Force use of web scraper instead of API
            
        Returns:
            Dict containing stock data
        """
        if use_scraper:
            return self.web_scraper.multi_source_scrape(symbol)
        
        # Try API first
        result = self.stock_extractor.get_yahoo_stock_data(symbol, period)
        
        # If API fails, try web scraping as fallback
        if result.get('status') != 'success':
            scraper_result = self.web_scraper.multi_source_scrape(symbol)
            if scraper_result.get('status') == 'success':
                return scraper_result
        
        return result
    
    def search_stocks(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for stocks by name or symbol
        
        Args:
            query: Search term
            
        Returns:
            List of matching stocks
        """
        return self.stock_extractor.search_stocks(query)
    
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get data for multiple stocks
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dict containing data for all symbols
        """
        return self.stock_extractor.get_multiple_stocks(symbols)
    
    def get_portfolio_summary(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get a summary of a stock portfolio
        
        Args:
            symbols: List of stock symbols in portfolio
            
        Returns:
            Dict containing portfolio summary
        """
        stocks_data = self.get_multiple_stocks(symbols)
        
        summary = {
            'total_stocks': len(symbols),
            'successful_fetches': 0,
            'failed_fetches': 0,
            'stocks': {},
            'market_cap_info': []
        }
        
        for symbol, data in stocks_data.items():
            if data.get('status') == 'success':
                summary['successful_fetches'] += 1
                summary['stocks'][symbol] = {
                    'price': data.get('regularMarketPrice'),
                    'change': data.get('regularMarketPrice', 0) - data.get('previousClose', 0),
                    'volume': data.get('regularMarketVolume'),
                    'currency': data.get('currency')
                }
            else:
                summary['failed_fetches'] += 1
                summary['stocks'][symbol] = {'error': data.get('message')}
        
        return summary
    
    # AI/GPT API Methods
    def ask_ai(self, question: str, provider: str = 'auto') -> Dict[str, Any]:
        """
        Ask a question to AI using available free providers
        
        Args:
            question: The question to ask
            provider: Specific provider or 'auto' for fallback
            
        Returns:
            Dict containing AI response
        """
        if provider == 'auto':
            return self.ai_extractor.multi_provider_chat(question)
        elif provider == 'huggingface':
            messages = [{'role': 'user', 'content': question}]
            return self.ai_extractor.huggingface_chat(messages)
        elif provider == 'openrouter':
            messages = [{'role': 'user', 'content': question}]
            return self.ai_extractor.openrouter_chat(messages)
        elif provider == 'together':
            messages = [{'role': 'user', 'content': question}]
            return self.ai_extractor.together_chat(messages)
        else:
            return {'status': 'error', 'message': f'Unknown provider: {provider}'}
    
    def generate_text(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        """
        Generate text completion
        
        Args:
            prompt: Text prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dict containing generated text
        """
        return self.ai_extractor.text_completion(prompt, max_tokens=max_tokens)
    
    def chat_conversation(self, messages: List[Dict[str, str]], provider: str = 'auto') -> Dict[str, Any]:
        """
        Have a conversation with AI
        
        Args:
            messages: List of messages in conversation
            provider: AI provider to use
            
        Returns:
            Dict containing AI response
        """
        if provider == 'auto':
            # Convert to simple message for multi-provider
            last_message = messages[-1].get('content', '') if messages else ''
            return self.ai_extractor.multi_provider_chat(last_message)
        elif provider == 'huggingface':
            return self.ai_extractor.huggingface_chat(messages)
        elif provider == 'openrouter':
            return self.ai_extractor.openrouter_chat(messages)
        elif provider == 'together':
            return self.ai_extractor.together_chat(messages)
        else:
            return {'status': 'error', 'message': f'Unknown provider: {provider}'}
    
    # Combined Methods
    def analyze_stock_with_ai(self, symbol: str, analysis_type: str = 'summary') -> Dict[str, Any]:
        """
        Get stock data and analyze it using AI
        
        Args:
            symbol: Stock symbol
            analysis_type: Type of analysis ('summary', 'prediction', 'risk')
            
        Returns:
            Dict containing stock data and AI analysis
        """
        # Get stock data
        stock_data = self.get_stock_price(symbol)
        
        if stock_data.get('status') != 'success':
            return stock_data
        
        # Prepare prompt for AI analysis
        price = stock_data.get('regularMarketPrice', 'N/A')
        prev_close = stock_data.get('previousClose', 'N/A')
        volume = stock_data.get('regularMarketVolume', 'N/A')
        
        if analysis_type == 'summary':
            prompt = f"""Analyze this stock data for {symbol}:
Current Price: ${price}
Previous Close: ${prev_close}
Volume: {volume}

Provide a brief summary of the stock's current status."""
        
        elif analysis_type == 'prediction':
            prompt = f"""Based on this stock data for {symbol}:
Current Price: ${price}
Previous Close: ${prev_close}
Volume: {volume}

What might be the short-term outlook? Consider general market factors."""
        
        elif analysis_type == 'risk':
            prompt = f"""Assess the risk level for {symbol} based on:
Current Price: ${price}
Previous Close: ${prev_close}
Volume: {volume}

What are potential risks to consider?"""
        
        else:
            prompt = f"Analyze stock {symbol} with current price ${price}"
        
        # Get AI analysis
        ai_response = self.ask_ai(prompt)
        
        return {
            'status': 'success',
            'symbol': symbol,
            'stock_data': stock_data,
            'ai_analysis': ai_response,
            'analysis_type': analysis_type
        }
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Check the status of all configured APIs
        
        Returns:
            Dict containing API status information
        """
        status = {
            'stock_apis': {
                'yahoo_finance': 'available (no key required)',
                'alpha_vantage': 'configured' if self.config.alpha_vantage_key else 'no key',
                'finnhub': 'configured' if self.config.finnhub_key else 'no key'
            },
            'ai_apis': {
                'huggingface': 'configured' if self.config.huggingface_key else 'limited (no key)',
                'openrouter': 'configured' if self.config.openrouter_key else 'limited (no key)',
                'together': 'configured' if self.config.together_key else 'no key'
            },
            'free_models': self.ai_extractor.get_free_models(),
            'config': {
                'requests_per_minute': self.config.requests_per_minute,
                'retry_attempts': self.config.retry_attempts
            }
        }
        
        return status
    
    def test_apis(self) -> Dict[str, Any]:
        """
        Test all available APIs to check functionality
        
        Returns:
            Dict containing test results
        """
        results = {}
        
        # Test stock APIs
        print("Testing stock APIs...")
        stock_test = self.get_stock_price('AAPL')
        results['stock_yahoo'] = 'working' if stock_test.get('status') == 'success' else 'failed'
        
        # Test AI APIs
        print("Testing AI APIs...")
        ai_test = self.ask_ai("Hello, can you respond with just 'working'?")
        results['ai_auto'] = 'working' if ai_test.get('status') == 'success' else 'failed'
        
        return results
    
    def get_crypto_prices(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get cryptocurrency prices using free APIs
        
        Args:
            symbols: List of crypto symbols/IDs (e.g., ['bitcoin', 'ethereum'])
            
        Returns:
            Dict containing crypto price data
        """
        return self.web_scraper.scrape_crypto_prices(symbols)
    
    def get_trending_stocks(self) -> List[Dict[str, Any]]:
        """
        Get trending/popular stocks
        
        Returns:
            List of trending stock information
        """
        return self.web_scraper.get_trending_stocks()
    
    def get_stock_with_fallback(self, symbol: str) -> Dict[str, Any]:
        """
        Get stock data with comprehensive fallback strategy
        Tries multiple methods to ensure data retrieval
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dict containing stock data from the first successful method
        """
        methods = [
            ('Yahoo API', lambda: self.stock_extractor.get_yahoo_stock_data(symbol)),
            ('Web Scraper', lambda: self.web_scraper.multi_source_scrape(symbol)),
        ]
        
        # Add API methods if keys are available
        if self.config.alpha_vantage_key:
            methods.insert(1, ('Alpha Vantage', lambda: self.stock_extractor.get_alpha_vantage_data(symbol)))
        
        if self.config.finnhub_key:
            methods.insert(1, ('Finnhub', lambda: self.stock_extractor.get_finnhub_data(symbol)))
        
        for method_name, method_func in methods:
            try:
                result = method_func()
                if result.get('status') == 'success' and result.get('regularMarketPrice') or result.get('price'):
                    result['method_used'] = method_name
                    return result
            except Exception as e:
                continue
        
        return {
            'status': 'error',
            'message': 'All stock data retrieval methods failed',
            'symbol': symbol
        }