#!/usr/bin/env python3
"""
CLI Principal do Sintaxes Deliciosas
Interface de linha de comando luxury para assistente IA personalizado
"""

import os
import sys
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.theme import Theme
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
import json
from pathlib import Path

from .config import Config
from .ai_assistant import AIAssistant
from .themes import get_theme, AVAILABLE_THEMES
from .utils import display_banner, format_code_output

console = Console()

# Tema luxury personalizado
LUXURY_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "primary": "bold magenta",
    "secondary": "blue",
    "accent": "bright_yellow",
    "luxury": "bold bright_magenta",
    "code": "bright_blue",
    "command": "bright_green",
})

console = Console(theme=LUXURY_THEME)


@click.group(invoke_without_command=True)
@click.option('--config', '-c', help='Arquivo de configuração personalizado')
@click.option('--theme', '-t', type=click.Choice(AVAILABLE_THEMES), help='Tema da interface')
@click.option('--verbose', '-v', is_flag=True, help='Modo verboso')
@click.pass_context
def cli(ctx, config: Optional[str], theme: Optional[str], verbose: bool):
    """
    🎭 SINTAXES DELICIOSAS 🎭
    
    Seu assistente IA de luxo personalizado para correção de código,
    melhorias de sintaxe e muito mais!
    """
    ctx.ensure_object(dict)
    
    # Configurar tema
    if theme:
        console.print(f"[luxury]Aplicando tema: {theme}[/luxury]")
        # Aplicar tema personalizado aqui
    
    # Se nenhum subcomando foi chamado, iniciar modo interativo
    if ctx.invoked_subcommand is None:
        interactive_mode(config, verbose)


def interactive_mode(config_path: Optional[str] = None, verbose: bool = False):
    """Modo interativo principal do assistente"""
    
    # Mostrar banner de boas-vindas
    display_banner(console)
    
    # Carregar configuração
    config = Config(config_path)
    
    # Inicializar assistente IA
    try:
        assistant = AIAssistant(config)
    except Exception as e:
        console.print(f"[error]Erro ao inicializar assistente IA: {e}[/error]")
        if not config.is_configured():
            setup_assistant()
            return
        sys.exit(1)
    
    console.print("\n[luxury]Bem-vindo ao seu assistente IA de luxo![/luxury]")
    console.print("[info]Digite 'help' para ver comandos disponíveis ou 'quit' para sair[/info]\n")
    
    session_history = []
    
    while True:
        try:
            # Prompt customizado e elegante
            user_input = Prompt.ask(
                "\n[luxury]❯[/luxury]",
                default="",
                show_default=False
            ).strip()
            
            if not user_input:
                continue
                
            # Comandos especiais
            if user_input.lower() in ['quit', 'exit', 'sair']:
                console.print("\n[luxury]Até logo! ✨[/luxury]")
                break
            elif user_input.lower() == 'help':
                show_help()
                continue
            elif user_input.lower() == 'history':
                show_history(session_history)
                continue
            elif user_input.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                display_banner(console)
                continue
            elif user_input.lower().startswith('theme '):
                theme_name = user_input[6:].strip()
                change_theme(theme_name)
                continue
            elif user_input.lower() == 'config':
                show_config(config)
                continue
                
            # Adicionar ao histórico
            session_history.append(user_input)
            
            # Processar com assistente IA
            with console.status("[luxury]Processando sua solicitação...[/luxury]", spinner="dots"):
                try:
                    response = assistant.process_request(user_input)
                    display_response(response)
                except Exception as e:
                    console.print(f"[error]Erro ao processar solicitação: {e}[/error]")
                    
        except KeyboardInterrupt:
            console.print("\n\n[warning]Operação cancelada pelo usuário[/warning]")
            continue
        except EOFError:
            console.print("\n\n[luxury]Até logo! ✨[/luxury]")
            break


def display_response(response: dict):
    """Exibe a resposta do assistente de forma elegante"""
    
    if response.get('type') == 'code_correction':
        panel = Panel(
            response['content'],
            title="[luxury]🔧 Correção de Código[/luxury]",
            border_style="bright_magenta",
            padding=(1, 2)
        )
        console.print(panel)
        
        if response.get('explanation'):
            console.print(f"\n[info]💡 Explicação:[/info] {response['explanation']}")
            
    elif response.get('type') == 'command_suggestion':
        panel = Panel(
            f"[command]{response['command']}[/command]",
            title="[luxury]⚡ Comando Sugerido[/luxury]",
            border_style="bright_green",
            padding=(1, 2)
        )
        console.print(panel)
        
        if Confirm.ask("[info]Executar este comando?[/info]"):
            execute_command(response['command'])
            
    else:
        # Resposta geral do assistente
        panel = Panel(
            response.get('content', str(response)),
            title="[luxury]🤖 Assistente IA[/luxury]",
            border_style="cyan",
            padding=(1, 2)
        )
        console.print(panel)


def execute_command(command: str):
    """Executa um comando do sistema com segurança"""
    try:
        console.print(f"[command]Executando: {command}[/command]")
        os.system(command)
    except Exception as e:
        console.print(f"[error]Erro ao executar comando: {e}[/error]")


def show_help():
    """Mostra ajuda com comandos disponíveis"""
    
    table = Table(title="[luxury]🎭 Comandos Disponíveis[/luxury]", show_header=True, header_style="bold magenta")
    table.add_column("Comando", style="command", width=15)
    table.add_column("Descrição", style="info")
    
    table.add_row("help", "Mostra esta ajuda")
    table.add_row("quit/exit/sair", "Sai do assistente")
    table.add_row("history", "Mostra histórico da sessão")
    table.add_row("clear", "Limpa a tela")
    table.add_row("config", "Mostra configurações atuais")
    table.add_row("theme <nome>", "Altera o tema da interface")
    table.add_row("", "")
    table.add_row("[bold]Funcionalidades IA:[/bold]", "")
    table.add_row("corrigir <código>", "Corrige sintaxe de código")
    table.add_row("melhorar <código>", "Sugere melhorias")
    table.add_row("explicar <código>", "Explica funcionamento")
    table.add_row("comando para <tarefa>", "Sugere comando shell")
    
    console.print(table)


def show_history(history: list):
    """Mostra histórico da sessão"""
    if not history:
        console.print("[info]Nenhum comando no histórico desta sessão[/info]")
        return
        
    table = Table(title="[luxury]📜 Histórico da Sessão[/luxury]", show_header=True)
    table.add_column("#", style="accent", width=5)
    table.add_column("Comando", style="code")
    
    for i, cmd in enumerate(history[-10:], 1):  # Últimos 10 comandos
        table.add_row(str(i), cmd)
    
    console.print(table)


def show_config(config: Config):
    """Mostra configurações atuais"""
    
    table = Table(title="[luxury]⚙️ Configurações[/luxury]", show_header=True)
    table.add_column("Configuração", style="primary")
    table.add_column("Valor", style="info")
    
    table.add_row("API Key Configurada", "✅ Sim" if config.get('openai_api_key') else "❌ Não")
    table.add_row("Tema", config.get('theme', 'default'))
    table.add_row("Modelo IA", config.get('ai_model', 'gpt-3.5-turbo'))
    table.add_row("Arquivo Config", str(config.config_path))
    
    console.print(table)


def change_theme(theme_name: str):
    """Altera o tema da interface"""
    if theme_name not in AVAILABLE_THEMES:
        console.print(f"[error]Tema '{theme_name}' não encontrado[/error]")
        console.print(f"[info]Temas disponíveis: {', '.join(AVAILABLE_THEMES)}[/info]")
        return
    
    console.print(f"[success]Tema alterado para: {theme_name}[/success]")
    # Aqui seria implementada a lógica de mudança de tema


@cli.command()
def setup():
    """Configuração inicial do assistente"""
    setup_assistant()


def setup_assistant():
    """Assistente de configuração inicial"""
    
    console.print("\n[luxury]🎭 Configuração Inicial - Sintaxes Deliciosas[/luxury]\n")
    
    # Solicitar API Key
    api_key = Prompt.ask(
        "[primary]Insira sua OpenAI API Key[/primary]",
        password=True,
        default=""
    )
    
    if api_key:
        config = Config()
        config.set('openai_api_key', api_key)
        config.save()
        console.print("[success]✅ API Key configurada com sucesso![/success]")
    else:
        console.print("[warning]⚠️ Configuração cancelada. Use 'sintaxes setup' para configurar depois.[/warning]")
        return
    
    # Configurar tema preferido
    theme = Prompt.ask(
        "[primary]Escolha um tema[/primary]",
        choices=AVAILABLE_THEMES,
        default="luxury"
    )
    
    config.set('theme', theme)
    config.save()
    
    console.print(f"[success]✅ Configuração concluída! Tema: {theme}[/success]")
    console.print("[info]Use 'sintaxes' para iniciar o assistente[/info]")


@cli.command()
@click.argument('code', required=False)
def corrigir(code: Optional[str]):
    """Corrige sintaxe de código"""
    if not code:
        code = Prompt.ask("[primary]Cole o código para correção[/primary]")
    
    config = Config()
    assistant = AIAssistant(config)
    
    with console.status("[luxury]Analisando e corrigindo código...[/luxury]"):
        result = assistant.correct_syntax(code)
        display_response(result)


@cli.command()
@click.argument('task')
def comando(task: str):
    """Sugere comando shell para uma tarefa"""
    config = Config()
    assistant = AIAssistant(config)
    
    with console.status("[luxury]Gerando comando...[/luxury]"):
        result = assistant.suggest_command(task)
        display_response(result)


def main():
    """Ponto de entrada principal"""
    try:
        cli()
    except Exception as e:
        console.print(f"[error]Erro fatal: {e}[/error]")
        sys.exit(1)


if __name__ == '__main__':
    main()