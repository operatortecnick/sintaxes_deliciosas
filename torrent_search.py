import argparse
import re
from typing import List, Optional

import requests

TOR_PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}


def query_pirate_bay(term: str, use_tor: bool = False) -> List[dict]:
    """Fetch results from the Pirate Bay API for a given term."""
    url = f"https://apibay.org/q.php?q={term}&cat=0"
    proxies = TOR_PROXIES if use_tor else None
    resp = requests.get(url, proxies=proxies, timeout=20)
    resp.raise_for_status()
    return resp.json()


def filter_result(torr: dict) -> Optional[dict]:
    """Filter a single torrent entry based on quality, language and seeders."""
    name_lc = torr['name'].lower()
    seeds = int(torr.get('seeders', 0))

    if '1080' not in name_lc and '2160' not in name_lc:
        return None

    palavras_pt = ['dublado', 'dub', 'dual', 'portugues', 'legenda', 'pt-br']
    if not any(p in name_lc for p in palavras_pt):
        return None

    if seeds < 5:
        return None

    info_hash = torr.get('info_hash') or torr.get('info_hash_v1')
    magnet = f"magnet:?xt=urn:btih:{info_hash}&dn={torr['name']}"

    ano = None
    m = re.search(r"\((\d{4})\)", torr['name'])
    if m:
        ano = m.group(1)

    legenda_disp = 'Sim' if any(x in name_lc for x in ['legenda', 'leg', 'pt-br']) else 'Não'
    qualidade = '2160p' if '2160' in name_lc else '1080p'

    return {
        'titulo': torr['name'],
        'ano': ano,
        'qualidade': qualidade,
        'seeders': seeds,
        'legenda': legenda_disp,
        'magnet': magnet,
    }


def search(genres: List[str], epoca: str, use_tor: bool = False) -> List[dict]:
    """Search torrents for multiple genres and return filtered results."""
    results: List[dict] = []
    for genre in genres:
        term = genre
        if epoca and epoca != 'sem restricao':
            term += f" {epoca}"
        torrs = query_pirate_bay(term, use_tor=use_tor)
        for torr in torrs:
            item = filter_result(torr)
            if item:
                results.append(item)

    results.sort(key=lambda x: x['seeders'], reverse=True)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Busca torrents de filmes por gênero.")
    parser.add_argument('--genres', required=True, help='Lista de gêneros separada por vírgula')
    parser.add_argument('--epoca', default='', help='Filtrar por época (ex: "anos 2010")')
    parser.add_argument('--tor', action='store_true', help='Usar proxy Tor na busca')
    parser.add_argument('--limit', type=int, default=5, help='Limite de resultados exibidos')
    args = parser.parse_args()

    genres = [g.strip() for g in args.genres.split(',') if g.strip()]
    resultados = search(genres, args.epoca, use_tor=args.tor)

    for item in resultados[:args.limit]:
        ano = item.get('ano', 'N/A')
        print(
            f"Título: {item['titulo']} - Ano: {ano} - "
            f"Qualidade: {item['qualidade']} - Legenda PT-BR: {item['legenda']} - "
            f"Link: {item['magnet']}\n"
        )


if __name__ == '__main__':
    main()
