"""
API endpoints of the Chess.com API (https://www.chess.com/news/view/published-data-api)
"""

REQUEST_HEADERS = {
    'Host': 'api.chess.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'From': 'adamhosticka@gmail.com',
}

COUNTRY_ENDPOINT = "https://api.chess.com/pub/country/{iso}"
COUNTRY_PLAYERS_ENDPOINT = "https://api.chess.com/pub/country/{iso}/players"
PLAYER_PROFILE_ENDPOINT = "https://api.chess.com/pub/player/{username}"
PLAYER_STATS_ENDPOINT = "https://api.chess.com/pub/player/{username}/stats"
PLAYER_GAMES_MONTH = "https://api.chess.com/pub/player/{username}/games/{year}/{month}"
