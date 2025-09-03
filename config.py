"""
Configuration management for API extractors
"""
import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class APIConfig:
    """Configuration for API endpoints and keys"""
    
    # Stock APIs
    alpha_vantage_key: Optional[str] = None
    finnhub_key: Optional[str] = None
    
    # AI APIs  
    huggingface_key: Optional[str] = None
    openrouter_key: Optional[str] = None
    together_key: Optional[str] = None
    
    # Rate limiting
    requests_per_minute: int = 60
    retry_attempts: int = 3
    
    @classmethod
    def from_env(cls) -> 'APIConfig':
        """Load configuration from environment variables"""
        return cls(
            alpha_vantage_key=os.getenv('ALPHA_VANTAGE_KEY'),
            finnhub_key=os.getenv('FINNHUB_KEY'),
            huggingface_key=os.getenv('HUGGINGFACE_KEY'),
            openrouter_key=os.getenv('OPENROUTER_KEY'),
            together_key=os.getenv('TOGETHER_KEY'),
            requests_per_minute=int(os.getenv('REQUESTS_PER_MINUTE', '60')),
            retry_attempts=int(os.getenv('RETRY_ATTEMPTS', '3'))
        )


# Free API endpoints that don't require keys
FREE_STOCK_APIS = {
    'yahoo_finance': 'https://query1.finance.yahoo.com/v8/finance/chart/',
    'yahoo_search': 'https://query1.finance.yahoo.com/v1/finance/search',
    'fmp_free': 'https://financialmodelingprep.com/api/v3/',
}

FREE_AI_APIS = {
    'huggingface_free': 'https://api-inference.huggingface.co/models/',
    'openrouter_free': 'https://openrouter.ai/api/v1/',
    'together_free': 'https://api.together.xyz/v1/',
}