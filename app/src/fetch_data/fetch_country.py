"""
Fetch countries information from Chess.com API and save it to a file.
"""

from app.helpers.data_filenames import COUNTRIES_FILENAME
from app.helpers.iso_codes import ISO_CODES
from app.helpers.api_endpoints import COUNTRY_ENDPOINT
from app.src.fetch_data.fetch_base import FetchBase


class FetchCountry(FetchBase):
    FILE_NAME = COUNTRIES_FILENAME

    def fetch_data(self):
        countries = []
        for iso_code in ISO_CODES:
            country = self.fetch_item(COUNTRY_ENDPOINT.format(iso=iso_code))
            if country:
                countries.append(country)
        self.dataframe = self.create_dataframe_from_list(countries)


if __name__ == '__main__':
    FetchCountry().run()
