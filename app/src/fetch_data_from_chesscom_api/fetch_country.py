"""
Fetch country information from Chess.com API and save it to csv file.
"""

from app.helpers.data_filenames import COUNTRIES_FILENAME
from app.helpers.iso_codes import ISO_CODES
from app.helpers.api_endpoints import COUNTRY_ENDPOINT
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase


class FetchCountry(FetchBase):
    FILE_NAME = COUNTRIES_FILENAME

    def fetch_data(self):
        for iso_code in ISO_CODES:
            self.data.append(self.fetch_item(COUNTRY_ENDPOINT.format(iso=iso_code)))


if __name__ == '__main__':
    FetchCountry().run()
