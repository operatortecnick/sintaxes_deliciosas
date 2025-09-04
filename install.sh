#!/bin/bash

# Script de instalação luxury para Sintaxes Deliciosas
# Instalação fácil e elegante do assistente IA

set -e

echo "🎭 SINTAXES DELICIOSAS - Instalação Luxury 🎭"
echo "=============================================="
echo ""

# Cores para output elegante
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Função para print colorido
print_color() {
    printf "${2}${1}${NC}\n"
}

print_success() {
    print_color "✅ $1" "$GREEN"
}

print_info() {
    print_color "ℹ️  $1" "$CYAN"
}

print_warning() {
    print_color "⚠️  $1" "$YELLOW"
}

print_error() {
    print_color "❌ $1" "$RED"
}

print_luxury() {
    print_color "🎭 $1" "$MAGENTA"
}

# Verificar se Python está instalado
check_python() {
    print_info "Verificando instalação do Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION encontrado"
        
        # Verificar se a versão é compatível (>= 3.8)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Versão do Python é compatível (>= 3.8)"
        else
            print_error "Python 3.8 ou superior é necessário"
            print_info "Instale uma versão mais recente do Python e tente novamente"
            exit 1
        fi
    else
        print_error "Python 3 não encontrado"
        print_info "Instale Python 3.8 ou superior antes de continuar"
        exit 1
    fi
}

# Verificar se pip está disponível
check_pip() {
    print_info "Verificando pip..."
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 encontrado"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip encontrado"
        PIP_CMD="pip"
    else
        print_error "pip não encontrado"
        print_info "Instale pip antes de continuar"
        exit 1
    fi
}

# Instalar o pacote
install_package() {
    print_luxury "Iniciando instalação luxury..."
    
    print_info "Instalando Sintaxes Deliciosas..."
    
    if [ -f "pyproject.toml" ]; then
        # Instalação em modo desenvolvimento se estiver no diretório do projeto
        print_info "Detectado diretório do projeto, instalando em modo desenvolvimento..."
        $PIP_CMD install -e .
    else
        # Instalação via PyPI (quando disponível)
        print_warning "Instalação via PyPI ainda não disponível"
        print_info "Clone o repositório e execute novamente no diretório do projeto"
        exit 1
    fi
    
    print_success "Instalação concluída!"
}

# Verificar instalação
verify_installation() {
    print_info "Verificando instalação..."
    
    if command -v sintaxes &> /dev/null; then
        print_success "Comando 'sintaxes' disponível"
    else
        print_warning "Comando 'sintaxes' não encontrado no PATH"
        print_info "Talvez seja necessário adicionar ~/.local/bin ao PATH"
    fi
    
    if command -v sd &> /dev/null; then
        print_success "Comando 'sd' (atalho) disponível"
    else
        print_warning "Comando 'sd' não encontrado no PATH"
    fi
}

# Configuração inicial
initial_setup() {
    print_luxury "Configuração inicial luxury..."
    
    echo ""
    print_info "Para usar o assistente IA, você precisará de uma API Key da OpenAI"
    print_info "Visite: https://platform.openai.com/api-keys"
    echo ""
    
    read -p "Deseja configurar agora? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v sintaxes &> /dev/null; then
            sintaxes setup
        else
            print_warning "Execute 'sintaxes setup' após adicionar ao PATH"
        fi
    else
        print_info "Você pode configurar depois com: sintaxes setup"
    fi
}

# Banner final
show_completion() {
    echo ""
    print_luxury "🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! 🎉"
    echo ""
    print_info "Comandos disponíveis:"
    print_color "  • sintaxes          - Iniciar assistente interativo" "$WHITE"
    print_color "  • sintaxes setup    - Configuração inicial" "$WHITE"
    print_color "  • sintaxes help     - Ajuda completa" "$WHITE"
    print_color "  • sd                - Atalho para sintaxes" "$WHITE"
    echo ""
    print_luxury "Bem-vindo ao seu assistente IA de luxo! ✨"
    echo ""
}

# Função principal
main() {
    check_python
    check_pip
    install_package
    verify_installation
    initial_setup
    show_completion
}

# Executar instalação
main