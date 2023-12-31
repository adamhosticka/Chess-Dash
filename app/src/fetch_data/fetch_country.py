"""Fetch countries information from Chess.com API and save it to a file."""

import pandas as pd

from app.helpers.data_filenames import COUNTRIES_FILENAME
from app.helpers.iso_codes import ISO_CODES
from app.helpers.api_endpoints import COUNTRY_ENDPOINT
from app.src.fetch_data.fetch_base import FetchBase
from app.utils.dataframe_utils import create_dataframe_from_list


class FetchCountry(FetchBase):
    """Fetch countries information from Chess.com API and save it to a file."""

    FILE_NAME = COUNTRIES_FILENAME

    def fetch_data(self) -> pd.DataFrame:
        countries = []
        for iso_code in ISO_CODES:
            country = self.fetch_item(COUNTRY_ENDPOINT.format(iso=iso_code))
            if country:
                countries.append(country)
        return create_dataframe_from_list(countries)
