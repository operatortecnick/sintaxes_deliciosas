# Sintaxes Deliciosas - API Extractor

🚀 **Extrator de APIs supremo** - Acesse APIs gratuitas de ações e inteligência artificial de forma unificada!

## 📋 Funcionalidades

### 📊 APIs de Ações (Gratuitas)
- **Yahoo Finance** - Dados em tempo real, sem necessidade de chave API
- **Alpha Vantage** - 500 requisições/dia gratuitas
- **Finnhub** - 60 chamadas/minuto gratuitas
- **Web Scraping** - Fallback automático para múltiplas fontes
- **CoinGecko** - Preços de criptomoedas gratuitos
- Busca de ações por nome ou símbolo
- Análise de portfólio
- Dados históricos e em tempo real
- Ações em tendência
- Sistema de fallback robusto

### 🤖 APIs de IA/GPT (Gratuitas)
- **Hugging Face** - Modelos gratuitos disponíveis
- **OpenRouter** - Modelos gratuitos incluindo Llama 3.2
- **Together AI** - Créditos de teste gratuitos
- Sistema de fallback automático entre provedores
- Chat conversacional
- Geração de texto
- Análise de ações com IA

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/operatortecnick/sintaxes_deliciosas.git
cd sintaxes_deliciosas

# Instale as dependências
pip install -r requirements.txt

# Configure as chaves de API (opcional)
cp .env.example .env
# Edite .env com suas chaves (muitas APIs funcionam sem chaves!)
```

## 🚀 Uso Rápido

### Via CLI (Linha de Comando)

```bash
# Obter preço de uma ação
python cli.py stock price AAPL

# Buscar ações
python cli.py stock search "Apple Inc"

# Ações em tendência
python cli.py stock trending

# Preços de criptomoedas
python cli.py stock crypto bitcoin ethereum

# Fallback com web scraping
python cli.py stock fallback TSLA --scraper

# Perguntar para IA
python cli.py ai ask "O que é Python?"

# Analisar ação com IA
python cli.py analyze TSLA --analysis summary

# Ver status das APIs
python cli.py status

# Testar todas as APIs
python cli.py test
```

### Via Python

```python
from api_extractor import APIExtractor

# Inicializar o extrator
extractor = APIExtractor()

# Obter dados de ação
stock_data = extractor.get_stock_price('AAPL')
print(f"Apple: ${stock_data['regularMarketPrice']}")

# Perguntar para IA
ai_response = extractor.ask_ai("Explique o mercado de ações")
print(ai_response)

# Analisar ação com IA
analysis = extractor.analyze_stock_with_ai('GOOGL', 'prediction')
```

## 📚 Exemplos Completos

Execute o arquivo de exemplo:
```bash
python example.py
```

### Exemplo de Análise de Portfólio

```python
# Analisar múltiplas ações
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
portfolio = extractor.get_portfolio_summary(symbols)

for symbol, data in portfolio['stocks'].items():
    price = data.get('price', 0)
    change = data.get('change', 0)
    print(f"{symbol}: ${price:.2f} ({change:+.2f})")

# Obter criptomoedas
crypto_data = extractor.get_crypto_prices(['bitcoin', 'ethereum'])
print(crypto_data)

# Ações em tendência
trending = extractor.get_trending_stocks()
for stock in trending[:5]:
    print(f"{stock['symbol']}: {stock['name']}")

# Fallback robusto
stock_data = extractor.get_stock_with_fallback('AAPL')
print(f"Método usado: {stock_data.get('method_used')}")
```

### Exemplo de Chat com IA

```python
# Chat com diferentes provedores
providers = ['huggingface', 'openrouter', 'auto']

for provider in providers:
    response = extractor.ask_ai(
        "Quais são as melhores práticas para investir em ações?", 
        provider=provider
    )
    print(f"{provider}: {response}")
```

## 🔑 APIs Suportadas

### 📊 Ações (Todas com níveis gratuitos)

| API | Chave Necessária | Limite Gratuito | Características |
|-----|------------------|-----------------|-----------------|
| Yahoo Finance | ❌ Não | Ilimitado* | Dados em tempo real, histórico |
| Alpha Vantage | ✅ Sim | 500 req/dia | Dados detalhados, indicadores |
| Finnhub | ✅ Sim | 60 req/min | Dados fundamentais, notícias |
| Web Scraping | ❌ Não | Limitado por site | Fallback automático |
| CoinGecko | ❌ Não | Ilimitado* | Preços de criptomoedas |

*Sujeito a rate limiting informal

### 🤖 IA (Todas com opções gratuitas)

| API | Chave Necessária | Modelos Gratuitos | Características |
|-----|------------------|-------------------|-----------------|
| Hugging Face | ⚠️ Opcional | GPT-2, DialoGPT, Blenderbot | Muitos modelos, sem limite rígido |
| OpenRouter | ⚠️ Opcional | Llama 3.2, Gemma 2, Zephyr | Modelos modernos, créditos iniciais |
| Together AI | ✅ Sim | Llama, Qwen, RedPajama | Créditos de teste, modelos rápidos |

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# APIs de Ações (opcional)
ALPHA_VANTAGE_KEY=sua_chave_aqui
FINNHUB_KEY=sua_chave_aqui

# APIs de IA (opcional)
HUGGINGFACE_KEY=sua_chave_aqui
OPENROUTER_KEY=sua_chave_aqui
TOGETHER_KEY=sua_chave_aqui

# Configurações
REQUESTS_PER_MINUTE=60
RETRY_ATTEMPTS=3
```

### Como Obter Chaves Gratuitas

1. **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
2. **Finnhub**: https://finnhub.io/register
3. **Hugging Face**: https://huggingface.co/settings/tokens
4. **OpenRouter**: https://openrouter.ai/keys
5. **Together AI**: https://api.together.xyz/signup

## 📖 Comandos CLI Disponíveis

```bash
# Comandos de Ações
python cli.py stock price SYMBOL [--period 1d]
python cli.py stock search QUERY [--limit 5]
python cli.py stock portfolio SYMBOL1 SYMBOL2 ...
python cli.py stock trending
python cli.py stock crypto bitcoin ethereum
python cli.py stock fallback SYMBOL [--scraper]

# Comandos de IA
python cli.py ai ask "PERGUNTA" [--provider auto]
python cli.py ai generate "PROMPT" [--max-tokens 100]
python cli.py ai models

# Comandos Combinados
python cli.py analyze SYMBOL [--analysis summary]
python cli.py status
python cli.py test
```

## 🔧 Tratamento de Erros

O sistema inclui:
- **Retry automático** para falhas temporárias
- **Fallback entre diferentes provedores** de IA
- **Web scraping como backup** quando APIs falham
- **Rate limiting respeitoso**
- **Múltiplas fontes de dados** para redundância
- **Mensagens de erro detalhadas**
- **Validação de entrada**
- **Sistema robusto offline/online**

## 🎯 Casos de Uso

### Para Investidores
- Monitoramento de carteira em tempo real
- Análise técnica com IA
- Busca e descoberta de ações
- Alertas e notificações

### Para Desenvolvedores
- Integração fácil com APIs financeiras
- Acesso a modelos de IA sem complexidade
- Sistema de fallback robusto
- Interface unificada

### Para Estudantes
- Aprendizado sobre mercado financeiro
- Experimentação com IA
- Exemplos práticos de uso de APIs
- Análise de dados financeiros

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## ⚖️ Aviso Legal

Este software é fornecido para fins educacionais e de pesquisa. Os usuários são responsáveis por:
- Respeitar os termos de uso das APIs
- Não exceder limites de rate limiting
- Usar os dados de forma ética e legal

**Não constitui aconselhamento financeiro.** Sempre consulte profissionais qualificados antes de tomar decisões de investimento.

## 🆘 Suporte

- 📧 Issues: Use o sistema de issues do GitHub
- 📚 Documentação: Veja os exemplos em `example.py`
- 🧪 Testes: Execute `python cli.py test` para verificar funcionamento

---

*Desenvolvido com ❤️ para democratizar o acesso a APIs de ações e IA*
