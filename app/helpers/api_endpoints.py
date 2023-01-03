"""
API endpoints of the Chess.com API (https://www.chess.com/news/view/published-data-api)
"""

COUNTRY_ENDPOINT = "https://api.chess.com/pub/country/{iso}"
COUNTRY_PLAYERS_ENDPOINT = "https://api.chess.com/pub/country/{iso}/players"
PLAYER_PROFILE_ENDPOINT = "https://api.chess.com/pub/player/{username}"
PLAYER_STATS_ENDPOINT = "https://api.chess.com/pub/player/{username}/stats"
PLAYER_MONTHLY_ARCHIVES = "https://api.chess.com/pub/player/{username}/games/archives"
PLAYER_GAMES_MONTH = "https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}"
