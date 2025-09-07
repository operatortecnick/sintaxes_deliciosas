# GitHub Repository Search App - Sintaxes Deliciosas

Uma aplicação desktop com interface gráfica que permite buscar repositórios do GitHub mundialmente através de uma interface similar a um chat.

## 🚀 Funcionalidades

- 🖥️ **Interface Gráfica Amigável**: Janela desktop com interface de chat
- 🔍 **Busca Global**: Conecta-se à API do GitHub para buscar repositórios mundialmente
- 💬 **Interface de Chat**: Digite suas consultas como em um chat (ex: "spotify gratis")
- 🎯 **Filtros Avançados**: Filtre por linguagem de programação e critérios de ordenação
- ⭐ **Resultados Detalhados**: Mostra stars, linguagem, descrição e link para cada repositório
- 🛡️ **Modo Demo**: Funciona mesmo quando a API está limitada

## 🛠️ Instalação

### Pré-requisitos
- Python 3.7+
- Sistema operacional com interface gráfica (Windows, macOS, Linux com X11)

### Instalação Automática
```bash
chmod +x run_app.sh
./run_app.sh
```

### Instalação Manual
```bash
# Instalar dependências Python
pip install -r requirements.txt

# No Ubuntu/Debian, instalar tkinter se necessário
sudo apt update && sudo apt install python3-tk

# Executar aplicação
python3 github_search_app.py
```

## 📖 Como Usar

1. **Iniciar a Aplicação**: Execute `python3 github_search_app.py` ou `./run_app.sh`
2. **Digite sua Busca**: No campo de entrada, digite o que deseja procurar
   - Exemplo: "spotify gratis"
   - Exemplo: "machine learning python"
   - Exemplo: "web scraper"
3. **Configurar Filtros** (opcional):
   - Selecione uma linguagem específica
   - Escolha o critério de ordenação (relevância, stars, forks, atualização)
4. **Buscar**: Clique no botão "🔍 Search" ou pressione Enter
5. **Ver Resultados**: Os resultados aparecerão na área de chat com:
   - Nome do repositório
   - Número de stars
   - Linguagem de programação
   - Descrição
   - Link direto para o repositório

## 🔧 Tecnologias Utilizadas

- **Python 3**: Linguagem principal
- **tkinter**: Interface gráfica nativa do Python
- **requests**: Para comunicação com a API do GitHub
- **threading**: Para operações assíncronas sem travar a interface

## 🌐 API do GitHub

A aplicação utiliza a API pública do GitHub para buscar repositórios:
- Endpoint: `https://api.github.com/search/repositories`
- Suporte a filtros avançados
- Limitação de taxa (rate limiting) tratada com modo demo

## 📸 Capturas de Tela

A aplicação apresenta:
- ✅ Janela principal com área de chat
- ✅ Campo de entrada para consultas
- ✅ Opções de filtro (linguagem e ordenação)
- ✅ Área de resultados formatada
- ✅ Barra de status informativa

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏆 Sintaxes Deliciosas

Parte do projeto "sintaxes deliciosas" - corretor supremo de programas, funções, aprimoramentos e sintaxes no geral.
