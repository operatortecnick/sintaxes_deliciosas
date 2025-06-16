# sintaxes_deliciosas

Utilitário para buscar torrents de filmes por gênero.

## Uso rápido em WSL

1. Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install requests
```

3. (Opcional) Inicie o serviço Tor para usar proxy:

```bash
sudo service tor start
```

4. Execute o script passando os gêneros desejados separados por vírgula:

```bash
python torrent_search.py --genres "Terror,Ação" --epoca "anos 2010" --tor
```

O script exibirá os resultados filtrados com qualidade **1080p** ou **2160p**, em português e com pelo menos cinco seeders.
