# 🎭 Sintaxes Deliciosas

**Seu Assistente IA de Luxo Personalizado**

Um CLI assistant elegante e poderoso para correção de código, melhorias de sintaxe e assistência IA personalizada. Projetado com interface luxury para uma experiência premium.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Características Luxury

- 🎭 **Interface Elegante**: CLI luxury com Rich para experiência visual premium
- 🤖 **IA Personalizada**: Integração com OpenAI para assistência inteligente
- 🔧 **Correção de Código**: Correção automática de sintaxe em múltiplas linguagens
- ⚡ **Sugestões Inteligentes**: Melhorias de código e comandos shell
- 🎨 **Temas Personalizados**: Múltiplos temas elegantes (luxury, midnight, gold, cyber)
- 💎 **Configuração Rica**: Sistema de configuração personalizada avançado
- 🚀 **Instalação Fácil**: Script de instalação automatizado e elegante
- 📚 **Histórico Inteligente**: Gerenciamento de sessões e histórico

## 🚀 Instalação Rápida

### Método Luxury (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/operatortecnick/sintaxes_deliciosas.git
cd sintaxes_deliciosas

# Execute o instalador luxury
./install.sh
```

### Instalação Manual

```bash
# Instalar dependências
pip install -e .

# Configurar assistente
sintaxes setup
```

## 🎯 Uso

### Modo Interativo

```bash
# Iniciar assistente (comando principal)
sintaxes

# Ou usar o atalho
sd
```

### Comandos Diretos

```bash
# Corrigir código
sintaxes corrigir "def hello world print('hello')"

# Sugerir comando shell
sintaxes comando "listar arquivos por tamanho"

# Configuração
sintaxes setup

# Ajuda
sintaxes --help
```

## 🎨 Temas Disponíveis

- **🎭 luxury** - Tema principal elegante (padrão)
- **🌙 midnight** - Tema noturno suave
- **⚪ minimal** - Tema minimalista limpo
- **✨ gold** - Tema dourado premium
- **🤖 cyber** - Tema cyberpunk futurista

```bash
# Trocar tema no modo interativo
theme gold

# Ou via comando
sintaxes --theme midnight
```

## 💡 Funcionalidades

### Correção de Código
```
❯ corrigir def hello world: print("hello")
```
O assistente detecta e corrige erros de sintaxe automaticamente.

### Melhorias de Código
```
❯ melhorar for i in range(len(lista)): print(lista[i])
```
Sugere versões mais eficientes e pythônicas.

### Sugestões de Comandos
```
❯ comando para comprimir arquivos
```
Gera comandos shell apropriados para tarefas específicas.

### Explicações Detalhadas
```
❯ explicar lambda x: x**2
```
Explica conceitos e funcionamento do código.

## ⚙️ Configuração

### Arquivo de Configuração

O assistente cria automaticamente `~/.config/sintaxes-deliciosas/config.yaml`:

```yaml
theme: luxury
ai_model: gpt-3.5-turbo
language_preference: pt-BR
personalization:
  name: "Seu Nome"
  greeting_style: formal
ai_settings:
  temperature: 0.7
  max_tokens: 2000
  system_prompt: "Prompt personalizado..."
shortcuts:
  cc: corrigir código
  mc: melhorar código
  ec: explicar código
```

### Variáveis de Ambiente

```bash
export OPENAI_API_KEY="sua-api-key-aqui"
```

## 🔐 Segurança

- API Keys são armazenadas no keyring do sistema
- Configurações sensíveis não são salvas em texto plano
- Validação de comandos antes da execução

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
sintaxes_deliciosas/
├── src/sintaxes_deliciosas/
│   ├── __init__.py
│   ├── cli.py              # Interface principal
│   ├── config.py           # Sistema de configuração
│   ├── ai_assistant.py     # Integração IA
│   ├── themes.py           # Temas visuais
│   └── utils.py            # Utilitários
├── pyproject.toml          # Configuração do projeto
├── install.sh              # Script de instalação
└── README.md
```

### Comandos de Desenvolvimento

```bash
# Instalação em modo desenvolvimento
pip install -e .

# Executar testes
pytest

# Formatação de código
black src/

# Linting
flake8 src/
```

## 📋 Comandos Disponíveis

### Modo Interativo

| Comando | Descrição |
|---------|-----------|
| `help` | Mostra ajuda |
| `quit`, `exit`, `sair` | Sair do assistente |
| `history` | Histórico da sessão |
| `clear` | Limpar tela |
| `config` | Mostrar configurações |
| `theme <nome>` | Trocar tema |

### Funcionalidades IA

| Comando | Descrição |
|---------|-----------|
| `corrigir <código>` | Corrigir sintaxe |
| `melhorar <código>` | Sugerir melhorias |
| `explicar <código>` | Explicar funcionamento |
| `comando para <tarefa>` | Sugerir comando shell |

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎯 Roadmap

- [ ] Integração com mais modelos IA (Claude, Gemini)
- [ ] Plugin system para extensões
- [ ] Interface web opcional
- [ ] Sincronização de configurações na nuvem
- [ ] Suporte a mais linguagens de programação
- [ ] Integração com IDEs

## 🐛 Relatório de Bugs

Encontrou um bug? [Abra uma issue](https://github.com/operatortecnick/sintaxes_deliciosas/issues)

## 💬 Suporte

- [Documentação](https://github.com/operatortecnick/sintaxes_deliciosas/wiki)
- [Issues](https://github.com/operatortecnick/sintaxes_deliciosas/issues)
- [Discussões](https://github.com/operatortecnick/sintaxes_deliciosas/discussions)

---

**🎭 Desenvolvido com luxo e carinho para desenvolvedores exigentes ✨**
