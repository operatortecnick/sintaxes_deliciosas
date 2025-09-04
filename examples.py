#!/usr/bin/env python3
"""
Exemplo de uso do Sintaxes Deliciosas
Demonstra as principais funcionalidades do assistente IA
"""

import os
import sys

# Adicionar src ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sintaxes_deliciosas.config import Config
from sintaxes_deliciosas.ai_assistant import AIAssistant
from sintaxes_deliciosas.themes import get_theme, list_themes
from sintaxes_deliciosas.utils import display_banner
from rich.console import Console


def exemplo_configuracao():
    """Exemplo de configuração"""
    print("🔧 Exemplo: Configuração")
    
    config = Config()
    
    # Configurações básicas
    config.set('theme', 'gold')
    config.set('personalization.name', 'Desenvolvedor Supremo')
    config.set('ai_settings.temperature', 0.8)
    
    print(f"Tema atual: {config.get('theme')}")
    print(f"Nome do usuário: {config.get_user_name()}")
    print(f"Modelo IA: {config.get('ai_model')}")
    
    print("✅ Configuração atualizada!\n")


def exemplo_temas():
    """Exemplo de temas"""
    print("🎨 Exemplo: Temas Disponíveis")
    
    console = Console()
    
    for theme_name, description in list_themes().items():
        theme = get_theme(theme_name)
        console.print(f"[bold]{theme_name.upper()}[/bold]: {description}")
    
    print("\n✅ Temas carregados com sucesso!\n")


def exemplo_deteccao_codigo():
    """Exemplo de detecção de código"""
    print("🔍 Exemplo: Detecção de Linguagem")
    
    from sintaxes_deliciosas.utils import detect_code_language
    
    exemplos = {
        "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)": "Python",
        "function factorial(n) { return n <= 1 ? 1 : n * factorial(n-1); }": "JavaScript",
        "SELECT users.name, COUNT(orders.id) FROM users LEFT JOIN orders ON users.id = orders.user_id GROUP BY users.id": "SQL",
        "#include <stdio.h>\nint main() { printf(\"Hello World\"); return 0; }": "C",
        "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello\"); } }": "Java"
    }
    
    for code, expected in exemplos.items():
        detected = detect_code_language(code)
        status = "✅" if detected.lower() == expected.lower() else "⚠️"
        print(f"{status} {expected}: {detected}")
        print(f"   Código: {code[:50]}...")
        print()


def exemplo_sem_api():
    """Exemplo de funcionalidades que não precisam de API"""
    print("🎭 Sintaxes Deliciosas - Exemplos de Uso")
    print("=" * 50)
    
    exemplo_configuracao()
    exemplo_temas()
    exemplo_deteccao_codigo()
    
    print("💡 Dica: Para usar as funcionalidades de IA, configure sua API Key:")
    print("   sintaxes setup")
    print()
    print("🚀 Para iniciar o assistente interativo:")
    print("   sintaxes")
    print()


def exemplo_com_api():
    """Exemplo com API configurada (simulado)"""
    print("🤖 Exemplo: Assistente IA (Requer API Key)")
    
    config = Config()
    
    if not config.is_configured():
        print("⚠️ API Key não configurada. Execute 'sintaxes setup' primeiro.")
        return
    
    try:
        assistant = AIAssistant(config)
        print("✅ Assistente IA inicializado com sucesso!")
        
        # Exemplo de correção de código (sem fazer chamada real à API)
        codigo_exemplo = "def hello world: print('hello')"
        print(f"📝 Código para correção: {codigo_exemplo}")
        print("🔧 Para corrigir, use: sintaxes corrigir \"def hello world: print('hello')\"")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar assistente: {e}")


if __name__ == '__main__':
    # Banner elegante
    console = Console()
    display_banner(console)
    
    print("\n")
    exemplo_sem_api()
    exemplo_com_api()
    
    print("🎉 Exemplos concluídos!")
    print("📚 Veja o README.md para documentação completa.")