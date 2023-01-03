from app.src.fetch_data_from_chesscom_api.fetch_country import FetchCountry
from app.src.fetch_data_from_chesscom_api.fetch_country_player import FetchCountryPlayer
from app.src.fetch_data_from_chesscom_api.fetch_game import FetchGame
from app.src.fetch_data_from_chesscom_api.fetch_player_detail import FetchPlayerDetail
from app.src.fetch_data_from_chesscom_api.fetch_player_stats import FetchPlayerStats


def fetch_data():
    print("Fetching data")
    FetchCountry().run()
    print("Countries fetched")
    FetchCountryPlayer(player_limit_per_country=1).run()
    print("Country Players fetched")
    FetchPlayerDetail().run()
    print("Players Details fetched")
    FetchPlayerStats().run()
    print("Players Stats fetched")
    FetchGame(archives_cnt=1).run()
    print("Games fetched :)")


if __name__ == '__main__':
    import time
    start_time = time.time()
    fetch_data()
    print("--- %s seconds ---" % (time.time() - start_time))
