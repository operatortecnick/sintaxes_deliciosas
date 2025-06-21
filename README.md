# sintaxes_deliciosas

Pequeno conjunto de utilidades para automatizar a cria\u00e7\u00e3o de contas no Instagram
utilizando e-mails tempor\u00e1rios da API `mail.tm`. O c\u00f3digo est\u00e1 organizado em m\u00f3dulos
para facilitar a reutiliza\u00e7\u00e3o com diferentes provedores de e-mail e plataformas.

## Estrutura

- `bot/mailtm.py` -- cliente simples para a API do mail.tm.
- `bot/instagram.py` -- fun\u00e7\u00f5es para automatizar o cadastro no Instagram
  via Selenium.
- `bot/utils.py` -- fun\u00e7\u00f5es auxiliares para gerar nomes e credenciais.
- `bot/__main__.py` -- exemplo de uso.

## Execu\u00e7\u00e3o

\`\`\`bash
python -m bot
\`\`\`

O script usa o Selenium e, opcionalmente, permite configurar proxy e modo
headless. O c\u00f3digo n\u00e3o inclui depend\u00eancias bin\u00e1rias do Chrome/Chromedriver,
portanto certifique-se de t\u00ea-los instalados antes de executar.
