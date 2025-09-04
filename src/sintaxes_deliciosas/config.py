"""
Sistema de Configuração para Sintaxes Deliciosas
Gerencia configurações personalizadas do usuário
"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import keyring


class Config:
    """Gerenciador de configurações personalizadas"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.app_name = "sintaxes-deliciosas"
        
        # Determinar caminho do arquivo de configuração
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Usar diretório padrão do usuário
            config_dir = Path.home() / ".config" / "sintaxes-deliciosas"
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_path = config_dir / "config.yaml"
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo"""
        if not self.config_path.exists():
            return self._default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
                
            # Mesclar com configurações padrão
            default = self._default_config()
            default.update(config)
            return default
            
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Configurações padrão"""
        return {
            'theme': 'luxury',
            'ai_model': 'gpt-3.5-turbo',
            'max_history': 100,
            'auto_save_history': True,
            'verbose': False,
            'language_preference': 'pt-BR',
            'code_style': {
                'preferred_language': 'python',
                'line_length': 88,
                'use_tabs': False,
                'tab_width': 4,
            },
            'ai_settings': {
                'temperature': 0.7,
                'max_tokens': 2000,
                'system_prompt': (
                    "Você é um assistente IA de luxo especializado em programação. "
                    "Seja elegante, preciso e útil. Responda sempre em português brasileiro "
                    "de forma clara e profissional."
                ),
            },
            'shortcuts': {
                'cc': 'corrigir código',
                'mc': 'melhorar código',
                'ec': 'explicar código',
                'cmd': 'comando para',
            },
            'personalization': {
                'name': 'Dev',
                'greeting_style': 'formal',
                'preferred_examples': 'python',
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração com suporte a chaves aninhadas"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Define valor de configuração com suporte a chaves aninhadas"""
        keys = key.split('.')
        config = self._config
        
        # Navegar até o penúltimo nível
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Definir valor final
        config[keys[-1]] = value
    
    def save(self) -> bool:
        """Salva configurações no arquivo"""
        try:
            # Criar diretório se não existir
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Salvar configurações (exceto dados sensíveis)
            config_to_save = self._config.copy()
            
            # Remover API key do arquivo (armazenar no keyring)
            if 'openai_api_key' in config_to_save:
                api_key = config_to_save.pop('openai_api_key')
                self._store_api_key(api_key)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_to_save, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def _store_api_key(self, api_key: str) -> None:
        """Armazena API key no keyring do sistema"""
        try:
            keyring.set_password(self.app_name, "openai_api_key", api_key)
        except Exception as e:
            print(f"Aviso: Não foi possível armazenar API key no keyring: {e}")
    
    def _get_api_key(self) -> Optional[str]:
        """Recupera API key do keyring do sistema"""
        try:
            return keyring.get_password(self.app_name, "openai_api_key")
        except Exception:
            return None
    
    def get_api_key(self) -> Optional[str]:
        """Obtém API key (do keyring ou variável de ambiente)"""
        # Tentar keyring primeiro
        api_key = self._get_api_key()
        if api_key:
            return api_key
        
        # Tentar variável de ambiente
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key
        
        # Tentar configuração (para compatibilidade)
        return self.get('openai_api_key')
    
    def is_configured(self) -> bool:
        """Verifica se o assistente está configurado adequadamente"""
        return bool(self.get_api_key())
    
    def reset_to_defaults(self) -> None:
        """Reseta configurações para valores padrão"""
        self._config = self._default_config()
    
    def export_config(self, file_path: str) -> bool:
        """Exporta configurações para um arquivo"""
        try:
            export_config = self._config.copy()
            # Não exportar dados sensíveis
            export_config.pop('openai_api_key', None)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(export_config, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao exportar configuração: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Importa configurações de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = yaml.safe_load(f)
            
            if imported_config:
                self._config.update(imported_config)
                return self.save()
            return False
            
        except Exception as e:
            print(f"Erro ao importar configuração: {e}")
            return False
    
    def get_user_name(self) -> str:
        """Obtém nome personalizado do usuário"""
        return self.get('personalization.name', 'Dev')
    
    def get_ai_settings(self) -> Dict[str, Any]:
        """Obtém configurações do AI"""
        return self.get('ai_settings', {})
    
    def get_shortcuts(self) -> Dict[str, str]:
        """Obtém atalhos personalizados"""
        return self.get('shortcuts', {})
    
    def __repr__(self) -> str:
        return f"Config(path={self.config_path}, configured={self.is_configured()})"