"""
Utilitários para Sintaxes Deliciosas
Funções auxiliares para formatação e exibição
"""

import re
import sys
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.table import Table


def display_banner(console: Console) -> None:
    """Exibe banner elegante de boas-vindas"""
    
    banner_text = """
╔══════════════════════════════════════════════════════════════╗
║                  🎭 SINTAXES DELICIOSAS 🎭                   ║
║                                                              ║
║           Seu Assistente IA de Luxo Personalizado           ║
║                                                              ║
║    ✨ Correção de Código  ⚡ Sugestões Inteligentes          ║
║    🔧 Melhorias Automáticas  💡 Explicações Detalhadas      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    
    panel = Panel(
        Text(banner_text, style="luxury", justify="center"),
        border_style="bright_magenta",
        padding=(0, 1)
    )
    
    console.print(panel)


def format_code_output(code: str, language: str = "python") -> Syntax:
    """Formata código com syntax highlighting"""
    return Syntax(
        code,
        language,
        theme="monokai",
        line_numbers=True,
        word_wrap=True,
        background_color="default"
    )


def format_markdown(text: str) -> Markdown:
    """Formata texto markdown"""
    return Markdown(text)


def create_status_table(items: List[Dict[str, Any]]) -> Table:
    """Cria tabela de status elegante"""
    
    table = Table(show_header=True, header_style="bold luxury")
    table.add_column("Item", style="primary")
    table.add_column("Status", style="info")
    table.add_column("Detalhes", style="secondary")
    
    for item in items:
        status_style = "success" if item.get('status') == 'ok' else "error"
        table.add_row(
            item.get('name', ''),
            f"[{status_style}]{item.get('status', 'unknown')}[/{status_style}]",
            item.get('details', '')
        )
    
    return table


def detect_code_language(code: str) -> str:
    """Detecta linguagem de programação do código"""
    
    # Padrões para diferentes linguagens
    patterns = {
        'python': [
            r'def\s+\w+\(',
            r'import\s+\w+',
            r'from\s+\w+\s+import',
            r'if\s+__name__\s*==\s*["\']__main__["\']',
            r'print\s*\(',
            r'class\s+\w+\s*\([^)]*\):',
        ],
        'javascript': [
            r'function\s+\w+\s*\(',
            r'const\s+\w+\s*=',
            r'let\s+\w+\s*=',
            r'var\s+\w+\s*=',
            r'console\.log\s*\(',
            r'=>\s*{',
        ],
        'java': [
            r'public\s+class\s+\w+',
            r'public\s+static\s+void\s+main',
            r'System\.out\.println',
            r'import\s+java\.',
            r'@Override',
        ],
        'cpp': [
            r'#include\s*<[^>]+>',
            r'int\s+main\s*\(',
            r'std::',
            r'cout\s*<<',
            r'using\s+namespace\s+std',
        ],
        'c': [
            r'#include\s*<[^>]+\.h>',
            r'int\s+main\s*\(',
            r'printf\s*\(',
            r'scanf\s*\(',
        ],
        'sql': [
            r'SELECT\s+.*\s+FROM',
            r'INSERT\s+INTO',
            r'UPDATE\s+.*\s+SET',
            r'DELETE\s+FROM',
            r'CREATE\s+TABLE',
        ],
        'html': [
            r'<html',
            r'<div',
            r'<span',
            r'<!DOCTYPE',
            r'<script',
        ],
        'css': [
            r'{\s*\w+\s*:',
            r'@media',
            r'\.[\w-]+\s*{',
            r'#[\w-]+\s*{',
        ],
        'bash': [
            r'#!/bin/bash',
            r'#!/bin/sh',
            r'\$\w+',
            r'echo\s+',
            r'if\s*\[\s*.*\s*\]\s*;\s*then',
        ],
        'json': [
            r'{\s*"[^"]+"\s*:',
            r'\[\s*{',
            r'}\s*,\s*{',
        ],
        'yaml': [
            r'^\s*\w+\s*:',
            r'^\s*-\s+\w+',
            r'---',
        ],
    }
    
    code_lower = code.lower()
    
    # Contar matches para cada linguagem
    scores = {}
    for lang, lang_patterns in patterns.items():
        score = sum(1 for pattern in lang_patterns 
                   if re.search(pattern, code, re.MULTILINE | re.IGNORECASE))
        if score > 0:
            scores[lang] = score
    
    # Retornar linguagem com maior score
    if scores:
        return max(scores, key=scores.get)
    
    return "text"


def clean_code_block(text: str) -> str:
    """Remove markdown code block markers"""
    
    # Remove ```language e ``` no início e fim
    text = re.sub(r'^```\w*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
    
    # Remove indentação excessiva
    lines = text.split('\n')
    if lines:
        # Encontrar menor indentação (ignorando linhas vazias)
        min_indent = min(
            len(line) - len(line.lstrip())
            for line in lines
            if line.strip()
        ) if any(line.strip() for line in lines) else 0
        
        # Remover indentação mínima de todas as linhas
        lines = [line[min_indent:] if len(line) > min_indent else line for line in lines]
        text = '\n'.join(lines)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Trunca texto com reticências elegantes"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def format_file_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def validate_api_key(api_key: str) -> bool:
    """Valida formato da API key da OpenAI"""
    if not api_key:
        return False
    
    # OpenAI API keys começam com 'sk-' e têm formato específico
    return api_key.startswith('sk-') and len(api_key) > 20


def get_terminal_size() -> tuple:
    """Obtém tamanho do terminal"""
    try:
        import shutil
        return shutil.get_terminal_size()
    except:
        return (80, 24)  # Fallback


def center_text(text: str, width: int = None) -> str:
    """Centraliza texto na largura especificada"""
    if width is None:
        width = get_terminal_size()[0]
    
    lines = text.split('\n')
    centered_lines = []
    
    for line in lines:
        # Remove códigos de cor para calcular largura real
        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        padding = max(0, (width - len(clean_line)) // 2)
        centered_lines.append(' ' * padding + line)
    
    return '\n'.join(centered_lines)


def create_progress_bar(progress: float, width: int = 40) -> str:
    """Cria barra de progresso ASCII"""
    filled = int(progress * width)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {progress*100:.1f}%"


def format_duration(seconds: float) -> str:
    """Formata duração em formato legível"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{int(minutes)}m {secs:.1f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"