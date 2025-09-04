"""
Assistente IA para Sintaxes Deliciosas
Integração com OpenAI para correções de código e assistência personalizada
"""

import re
import json
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI
from .config import Config


class AIAssistant:
    """Assistente IA personalizado para correção de código e sugestões"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Configurar client OpenAI
        api_key = config.get_api_key()
        if not api_key:
            raise ValueError("API Key da OpenAI não configurada. Execute 'sintaxes setup' primeiro.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = config.get('ai_model', 'gpt-3.5-turbo')
        self.ai_settings = config.get_ai_settings()
        
        # Configurações personalizadas
        self.user_name = config.get_user_name()
        self.language_preference = config.get('language_preference', 'pt-BR')
        
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Processa solicitação do usuário e determina tipo de resposta"""
        
        # Detectar tipo de solicitação
        request_type = self._detect_request_type(user_input)
        
        if request_type == 'code_correction':
            return self.correct_syntax(user_input)
        elif request_type == 'code_improvement':
            return self.improve_code(user_input)
        elif request_type == 'code_explanation':
            return self.explain_code(user_input)
        elif request_type == 'command_suggestion':
            return self.suggest_command(user_input)
        else:
            return self.general_assistance(user_input)
    
    def _detect_request_type(self, user_input: str) -> str:
        """Detecta o tipo de solicitação baseado no input do usuário"""
        
        input_lower = user_input.lower()
        
        # Padrões para diferentes tipos de solicitação
        if any(word in input_lower for word in ['corrigir', 'corrija', 'fix', 'erro', 'bug']):
            return 'code_correction'
        elif any(word in input_lower for word in ['melhorar', 'otimizar', 'improve', 'optimize']):
            return 'code_improvement'
        elif any(word in input_lower for word in ['explicar', 'explique', 'explain', 'como funciona']):
            return 'code_explanation'
        elif any(word in input_lower for word in ['comando', 'command', 'shell', 'terminal']):
            return 'command_suggestion'
        elif self._has_code_pattern(user_input):
            return 'code_correction'
        else:
            return 'general'
    
    def _has_code_pattern(self, text: str) -> bool:
        """Detecta se o texto contém padrões de código"""
        
        code_patterns = [
            r'def\s+\w+\(',      # Python functions
            r'function\s+\w+\(', # JavaScript functions
            r'class\s+\w+',      # Class definitions
            r'import\s+\w+',     # Import statements
            r'#include\s*<',     # C/C++ includes
            r'public\s+class',   # Java classes
            r'{\s*\w+:',         # JSON-like objects
            r'SELECT\s+.*FROM',  # SQL queries
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in code_patterns)
    
    def correct_syntax(self, code: str) -> Dict[str, Any]:
        """Corrige sintaxe de código"""
        
        prompt = f"""
        Como especialista em programação, analise o código abaixo e corrija quaisquer erros de sintaxe.
        
        Instruções:
        - Identifique e corrija todos os erros de sintaxe
        - Mantenha a lógica original do código
        - Forneça explicação clara das correções
        - Responda em português brasileiro
        - Seja elegante e profissional
        
        Código para correção:
        ```
        {code}
        ```
        
        Formate sua resposta como JSON:
        {{
            "corrected_code": "código corrigido aqui",
            "errors_found": ["lista de erros encontrados"],
            "explanation": "explicação das correções feitas"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.ai_settings.get('system_prompt', '')},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_settings.get('temperature', 0.7),
                max_tokens=self.ai_settings.get('max_tokens', 2000)
            )
            
            content = response.choices[0].message.content
            
            # Tentar parsear JSON da resposta
            try:
                result = json.loads(content)
                return {
                    'type': 'code_correction',
                    'content': result.get('corrected_code', content),
                    'errors': result.get('errors_found', []),
                    'explanation': result.get('explanation', '')
                }
            except json.JSONDecodeError:
                return {
                    'type': 'code_correction',
                    'content': content,
                    'explanation': 'Análise concluída'
                }
                
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Erro ao processar correção: {str(e)}"
            }
    
    def improve_code(self, code: str) -> Dict[str, Any]:
        """Sugere melhorias para o código"""
        
        prompt = f"""
        Como especialista em programação, analise o código abaixo e sugira melhorias.
        
        Instruções:
        - Sugira melhorias de performance, legibilidade e boas práticas
        - Mantenha a funcionalidade original
        - Explique cada melhoria sugerida
        - Responda em português brasileiro
        - Seja elegante e profissional
        
        Código para melhorar:
        ```
        {code}
        ```
        
        Formate sua resposta como JSON:
        {{
            "improved_code": "código melhorado aqui",
            "improvements": ["lista de melhorias aplicadas"],
            "explanation": "explicação detalhada das melhorias"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.ai_settings.get('system_prompt', '')},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_settings.get('temperature', 0.7),
                max_tokens=self.ai_settings.get('max_tokens', 2000)
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                return {
                    'type': 'code_improvement',
                    'content': result.get('improved_code', content),
                    'improvements': result.get('improvements', []),
                    'explanation': result.get('explanation', '')
                }
            except json.JSONDecodeError:
                return {
                    'type': 'code_improvement',
                    'content': content,
                    'explanation': 'Análise de melhorias concluída'
                }
                
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Erro ao processar melhorias: {str(e)}"
            }
    
    def explain_code(self, code: str) -> Dict[str, Any]:
        """Explica o funcionamento do código"""
        
        prompt = f"""
        Como especialista em programação, explique o funcionamento do código abaixo de forma clara e didática.
        
        Instruções:
        - Explique linha por linha quando necessário
        - Use linguagem clara e acessível
        - Identifique padrões e técnicas utilizadas
        - Responda em português brasileiro
        - Seja elegante e educativo
        
        Código para explicar:
        ```
        {code}
        ```
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.ai_settings.get('system_prompt', '')},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_settings.get('temperature', 0.7),
                max_tokens=self.ai_settings.get('max_tokens', 2000)
            )
            
            return {
                'type': 'code_explanation',
                'content': response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Erro ao explicar código: {str(e)}"
            }
    
    def suggest_command(self, task: str) -> Dict[str, Any]:
        """Sugere comando shell para uma tarefa específica"""
        
        prompt = f"""
        Como especialista em linha de comando, sugira o comando shell mais adequado para a seguinte tarefa:
        
        Tarefa: {task}
        
        Instruções:
        - Forneça o comando mais eficiente e seguro
        - Explique o que o comando faz
        - Inclua opções relevantes
        - Considere diferentes sistemas operacionais quando necessário
        - Responda em português brasileiro
        
        Formate sua resposta como JSON:
        {{
            "command": "comando shell aqui",
            "explanation": "explicação do comando",
            "platform": "linux/windows/mac ou all",
            "safety_notes": "avisos de segurança se aplicável"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.ai_settings.get('system_prompt', '')},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_settings.get('temperature', 0.3),  # Menos criativo para comandos
                max_tokens=self.ai_settings.get('max_tokens', 1000)
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                return {
                    'type': 'command_suggestion',
                    'command': result.get('command', ''),
                    'content': result.get('explanation', content),
                    'platform': result.get('platform', 'all'),
                    'safety_notes': result.get('safety_notes', '')
                }
            except json.JSONDecodeError:
                return {
                    'type': 'command_suggestion',
                    'content': content
                }
                
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Erro ao sugerir comando: {str(e)}"
            }
    
    def general_assistance(self, query: str) -> Dict[str, Any]:
        """Assistência geral personalizada"""
        
        prompt = f"""
        Olá {self.user_name}! Como seu assistente IA de luxo personalizado, estou aqui para ajudar.
        
        Sua pergunta: {query}
        
        Instruções:
        - Seja útil, elegante e profissional
        - Responda em português brasileiro
        - Considere contexto de programação quando relevante
        - Seja conciso mas completo
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.ai_settings.get('system_prompt', '')},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_settings.get('temperature', 0.7),
                max_tokens=self.ai_settings.get('max_tokens', 1500)
            )
            
            return {
                'type': 'general_assistance',
                'content': response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Erro na assistência geral: {str(e)}"
            }