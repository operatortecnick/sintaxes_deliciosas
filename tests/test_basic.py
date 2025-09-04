"""
Testes básicos para Sintaxes Deliciosas
"""

import pytest
import os
import tempfile
from pathlib import Path

from sintaxes_deliciosas.config import Config
from sintaxes_deliciosas.themes import get_theme, AVAILABLE_THEMES
from sintaxes_deliciosas.utils import (
    detect_code_language, 
    clean_code_block, 
    validate_api_key,
    format_duration
)


class TestConfig:
    """Testes para o sistema de configuração"""
    
    def test_config_creation(self):
        """Testa criação de configuração"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            config = Config(str(config_path))
            
            assert config.config_path == config_path
            assert config.get('theme') == 'luxury'
            assert config.get('ai_model') == 'gpt-3.5-turbo'
    
    def test_config_get_set(self):
        """Testa get/set de configurações"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            config = Config(str(config_path))
            
            # Teste de configuração simples
            config.set('test_key', 'test_value')
            assert config.get('test_key') == 'test_value'
            
            # Teste de configuração aninhada
            config.set('nested.key', 'nested_value')
            assert config.get('nested.key') == 'nested_value'
    
    def test_config_save_load(self):
        """Testa salvamento e carregamento"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.yaml"
            
            # Criar e salvar
            config1 = Config(str(config_path))
            config1.set('test_setting', 'test_value')
            config1.save()
            
            # Carregar nova instância
            config2 = Config(str(config_path))
            assert config2.get('test_setting') == 'test_value'


class TestThemes:
    """Testes para o sistema de temas"""
    
    def test_available_themes(self):
        """Testa temas disponíveis"""
        assert 'luxury' in AVAILABLE_THEMES
        assert 'midnight' in AVAILABLE_THEMES
        assert 'gold' in AVAILABLE_THEMES
    
    def test_get_theme(self):
        """Testa obtenção de tema"""
        theme = get_theme('luxury')
        assert theme is not None
        
        # Teste de tema inexistente retorna luxury
        default_theme = get_theme('inexistent')
        assert default_theme is not None


class TestUtils:
    """Testes para utilitários"""
    
    def test_detect_code_language(self):
        """Testa detecção de linguagem"""
        
        # Python
        python_code = "def hello():\n    print('hello')"
        assert detect_code_language(python_code) == 'python'
        
        # JavaScript
        js_code = "function hello() { console.log('hello'); }"
        assert detect_code_language(js_code) == 'javascript'
        
        # SQL
        sql_code = "SELECT * FROM users WHERE id = 1"
        assert detect_code_language(sql_code) == 'sql'
        
        # Texto sem código
        text = "Este é apenas um texto normal"
        assert detect_code_language(text) == 'text'
    
    def test_clean_code_block(self):
        """Testa limpeza de blocos de código"""
        
        # Código com markdown
        code_with_markdown = "```python\ndef hello():\n    print('hello')\n```"
        cleaned = clean_code_block(code_with_markdown)
        assert cleaned == "def hello():\n    print('hello')"
        
        # Código com indentação extra
        indented_code = "    def hello():\n        print('hello')"
        cleaned = clean_code_block(indented_code)
        assert cleaned == "def hello():\n    print('hello')"
    
    def test_validate_api_key(self):
        """Testa validação de API key"""
        
        # API key válida
        valid_key = "sk-1234567890abcdef1234567890abcdef1234567890"
        assert validate_api_key(valid_key) == True
        
        # API key inválida
        invalid_key = "invalid-key"
        assert validate_api_key(invalid_key) == False
        
        # Vazia
        assert validate_api_key("") == False
        assert validate_api_key(None) == False
    
    def test_format_duration(self):
        """Testa formatação de duração"""
        
        assert format_duration(30.5) == "30.5s"
        assert format_duration(90) == "1m 30.0s"
        assert format_duration(3660) == "1h 1m"


class TestCLIImports:
    """Testa se os módulos podem ser importados corretamente"""
    
    def test_import_main_modules(self):
        """Testa importação dos módulos principais"""
        
        try:
            from sintaxes_deliciosas import cli
            from sintaxes_deliciosas import config
            from sintaxes_deliciosas import themes
            from sintaxes_deliciosas import utils
        except ImportError as e:
            pytest.fail(f"Falha ao importar módulos: {e}")
    
    def test_cli_commands_exist(self):
        """Testa se os comandos CLI existem"""
        
        from sintaxes_deliciosas.cli import cli, setup, corrigir, comando
        
        # Verificar se são callables
        assert callable(cli)
        assert callable(setup)
        assert callable(corrigir)
        assert callable(comando)


if __name__ == '__main__':
    pytest.main([__file__])