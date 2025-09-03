"""
AI/GPT API Extractor
Supports multiple free AI APIs for text generation, chat, and inference
"""
import requests
import json
import time
from typing import Dict, List, Optional, Any, Union
from config import APIConfig, FREE_AI_APIS


class AIExtractor:
    """Extract data and perform inference using various free AI APIs"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
    
    def huggingface_inference(self, 
                             model: str, 
                             inputs: Union[str, Dict], 
                             parameters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Use Hugging Face Inference API (free tier available)
        
        Args:
            model: Model name (e.g., 'microsoft/DialoGPT-medium', 'gpt2')
            inputs: Input text or dict
            parameters: Optional parameters for the model
            
        Returns:
            Dict containing the inference results
        """
        try:
            url = FREE_AI_APIS['huggingface_free'] + model
            headers = {'Content-Type': 'application/json'}
            
            if self.config.huggingface_key:
                headers['Authorization'] = f'Bearer {self.config.huggingface_key}'
            
            payload = {'inputs': inputs}
            if parameters:
                payload['parameters'] = parameters
            
            response = self.session.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 503:
                return {'status': 'loading', 'message': 'Model is loading, try again in a few seconds'}
            
            response.raise_for_status()
            result = response.json()
            
            return {'status': 'success', 'model': model, 'result': result}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def huggingface_text_generation(self, 
                                  text: str, 
                                  model: str = 'gpt2',
                                  max_length: int = 100,
                                  temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate text using Hugging Face models
        
        Args:
            text: Input text prompt
            model: Model name (default: 'gpt2')
            max_length: Maximum length of generated text
            temperature: Randomness control (0.0 to 1.0)
            
        Returns:
            Dict containing generated text
        """
        parameters = {
            'max_length': max_length,
            'temperature': temperature,
            'return_full_text': False,
            'do_sample': True
        }
        
        return self.huggingface_inference(model, text, parameters)
    
    def huggingface_chat(self, 
                        messages: List[Dict[str, str]], 
                        model: str = 'microsoft/DialoGPT-medium') -> Dict[str, Any]:
        """
        Chat using Hugging Face conversational models
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name for conversation
            
        Returns:
            Dict containing chat response
        """
        # Convert messages to simple text for simpler models
        conversation = ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            conversation += f"{role}: {content}\n"
        
        conversation += "assistant:"
        
        return self.huggingface_text_generation(conversation, model)
    
    def openrouter_chat(self, 
                       messages: List[Dict[str, str]], 
                       model: str = 'meta-llama/llama-3.2-1b-instruct:free') -> Dict[str, Any]:
        """
        Use OpenRouter API with free models
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (free models available)
            
        Returns:
            Dict containing chat response
        """
        try:
            url = FREE_AI_APIS['openrouter_free'] + 'chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://github.com/operatortecnick/sintaxes_deliciosas',
                'X-Title': 'Sintaxes Deliciosas API Extractor'
            }
            
            if self.config.openrouter_key:
                headers['Authorization'] = f'Bearer {self.config.openrouter_key}'
            
            payload = {
                'model': model,
                'messages': messages,
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            response = self.session.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return {'status': 'success', 'model': model, 'result': result}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def together_chat(self, 
                     messages: List[Dict[str, str]], 
                     model: str = 'meta-llama/Llama-3.2-1B-Instruct-Turbo') -> Dict[str, Any]:
        """
        Use Together AI API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name
            
        Returns:
            Dict containing chat response
        """
        if not self.config.together_key:
            return {'status': 'error', 'message': 'Together AI API key required'}
        
        try:
            url = FREE_AI_APIS['together_free'] + 'chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.together_key}'
            }
            
            payload = {
                'model': model,
                'messages': messages,
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            response = self.session.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return {'status': 'success', 'model': model, 'result': result}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_free_models(self) -> Dict[str, List[str]]:
        """
        Get list of available free models from different providers
        
        Returns:
            Dict containing lists of free models by provider
        """
        return {
            'huggingface_free': [
                'gpt2',
                'microsoft/DialoGPT-medium',
                'facebook/blenderbot-400M-distill',
                'microsoft/DialoGPT-small',
                'distilgpt2',
                'EleutherAI/gpt-neo-125M',
                'facebook/opt-125m'
            ],
            'openrouter_free': [
                'meta-llama/llama-3.2-1b-instruct:free',
                'meta-llama/llama-3.2-3b-instruct:free',
                'google/gemma-2-2b-it:free',
                'huggingfaceh4/zephyr-7b-beta:free',
                'openchat/openchat-7b:free'
            ],
            'together_credits': [
                'meta-llama/Llama-3.2-1B-Instruct-Turbo',
                'meta-llama/Llama-3.2-3B-Instruct-Turbo',
                'Qwen/Qwen2-1.5B-Instruct',
                'togethercomputer/RedPajama-INCITE-7B-Chat'
            ]
        }
    
    def multi_provider_chat(self, 
                           message: str, 
                           providers: List[str] = None) -> Dict[str, Any]:
        """
        Try multiple providers for chat completion (fallback system)
        
        Args:
            message: The message/prompt to send
            providers: List of providers to try (default: all available)
            
        Returns:
            Dict containing successful response from first working provider
        """
        if providers is None:
            providers = ['huggingface', 'openrouter', 'together']
        
        messages = [{'role': 'user', 'content': message}]
        
        for provider in providers:
            try:
                if provider == 'huggingface':
                    result = self.huggingface_chat(messages)
                elif provider == 'openrouter':
                    result = self.openrouter_chat(messages)
                elif provider == 'together' and self.config.together_key:
                    result = self.together_chat(messages)
                else:
                    continue
                
                if result.get('status') == 'success':
                    result['provider'] = provider
                    return result
                    
            except Exception as e:
                continue
        
        return {'status': 'error', 'message': 'All providers failed'}
    
    def text_completion(self, 
                       prompt: str, 
                       model: str = 'gpt2',
                       max_tokens: int = 100) -> Dict[str, Any]:
        """
        Simple text completion using available free models
        
        Args:
            prompt: Text prompt to complete
            model: Model to use
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dict containing completion
        """
        return self.huggingface_text_generation(
            prompt, 
            model=model, 
            max_length=len(prompt.split()) + max_tokens
        )