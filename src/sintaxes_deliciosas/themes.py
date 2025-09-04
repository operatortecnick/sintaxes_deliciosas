"""
Temas personalizados para Sintaxes Deliciosas
Interface luxury com múltiplos temas elegantes
"""

from rich.theme import Theme
from typing import Dict


# Tema principal luxury
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
    "banner": "bold bright_magenta",
    "prompt": "bold cyan",
})

# Tema noturno elegante
MIDNIGHT_THEME = Theme({
    "info": "bright_cyan",
    "warning": "bright_yellow",
    "error": "bright_red", 
    "success": "bright_green",
    "primary": "bright_blue",
    "secondary": "blue",
    "accent": "white",
    "luxury": "bright_white",
    "code": "cyan",
    "command": "green",
    "banner": "bright_white",
    "prompt": "bright_blue",
})

# Tema minimalista
MINIMAL_THEME = Theme({
    "info": "blue",
    "warning": "yellow",
    "error": "red",
    "success": "green", 
    "primary": "black",
    "secondary": "dim",
    "accent": "bright_white",
    "luxury": "bold",
    "code": "blue",
    "command": "green",
    "banner": "bold",
    "prompt": "blue",
})

# Tema gold luxury
GOLD_THEME = Theme({
    "info": "blue",
    "warning": "bright_yellow",
    "error": "red",
    "success": "green",
    "primary": "yellow",
    "secondary": "bright_yellow",
    "accent": "gold1", 
    "luxury": "bold gold1",
    "code": "cyan",
    "command": "green",
    "banner": "bold gold1",
    "prompt": "yellow",
})

# Tema cyberpunk
CYBER_THEME = Theme({
    "info": "bright_cyan",
    "warning": "bright_yellow",
    "error": "bright_red",
    "success": "bright_green",
    "primary": "bright_magenta",
    "secondary": "magenta",
    "accent": "bright_white",
    "luxury": "bold bright_magenta",
    "code": "cyan",
    "command": "green",
    "banner": "bold bright_magenta",
    "prompt": "bright_cyan",
})

# Mapeamento de temas
THEMES = {
    'luxury': LUXURY_THEME,
    'midnight': MIDNIGHT_THEME,
    'minimal': MINIMAL_THEME,
    'gold': GOLD_THEME,
    'cyber': CYBER_THEME,
}

AVAILABLE_THEMES = list(THEMES.keys())


def get_theme(theme_name: str) -> Theme:
    """Obtém tema por nome"""
    return THEMES.get(theme_name, LUXURY_THEME)


def get_theme_description(theme_name: str) -> str:
    """Obtém descrição do tema"""
    descriptions = {
        'luxury': '🎭 Luxury - Tema principal elegante com magenta e cores vibrantes',
        'midnight': '🌙 Midnight - Tema noturno com cores suaves para trabalho noturno',
        'minimal': '⚪ Minimal - Tema minimalista e limpo para foco máximo',
        'gold': '✨ Gold - Tema dourado luxury para experiência premium',
        'cyber': '🤖 Cyber - Tema cyberpunk com neon e cores futuristas',
    }
    return descriptions.get(theme_name, 'Tema personalizado')


def list_themes() -> Dict[str, str]:
    """Lista todos os temas disponíveis com descrições"""
    return {name: get_theme_description(name) for name in AVAILABLE_THEMES}