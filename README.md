# sintaxes_deliciosas

Corretor supremo de programas, funções e aprimoramentos de sintaxes no geral.

Este projeto inclui um utilitário chamado `organizar_estrutura_sintaxes.py` que
cria a árvore de diretórios e arquivos necessária para o restante do sistema.
O script aceita algumas opções avançadas:

```bash
python organizar_estrutura_sintaxes.py --help
```

Execute-o sem argumentos para gerar a estrutura padrão ou use `--check` para
apenas verificar se os arquivos existem. Use `--force` para sobrescrever
arquivos já criados. Os componentes principais ficam em `src/`, incluindo um
bot Telegram simples, o processo principal e módulos de utilidades.
