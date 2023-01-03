from app.src.fetch_data_from_chesscom_api.fetch_country import FetchCountry
from app.src.fetch_data_from_chesscom_api.fetch_country_player import FetchCountryPlayer
from app.src.fetch_data_from_chesscom_api.fetch_game import FetchGame
from app.src.fetch_data_from_chesscom_api.fetch_player_detail import FetchPlayerDetail
from app.src.fetch_data_from_chesscom_api.fetch_player_stats import FetchPlayerStats


def fetch_data():
    FetchCountry().run()
    FetchCountryPlayer(player_limit_per_country=1).run()
    FetchPlayerDetail().run()
    FetchPlayerStats().run()
    FetchGame(archives_cnt=1).run()


if __name__ == '__main__':
    import time
    start_time = time.time()
    fetch_data()
    print("--- %s seconds ---" % (time.time() - start_time))
