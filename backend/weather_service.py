# Standard library imports.
from datetime import datetime, timedelta
import requests

# Third party imports.

# Local application imports.


API_URL = "xmlweather.vedur.is"

ICELANDIC = "is"
ENGLISH = "en"
LANGUAGES = (ICELANDIC, ENGLISH)
TEMPERATURE = "T"
DIRECTION = "D"
WINDSPEED = "F"
DESCRIPTION = "W"
MEASURES = (TEMPERATURE, WINDSPEED, DIRECTION, DESCRIPTION)


def fetch_forecast(
    start: datetime,
    end: datetime,
    language: str = "is",
) -> dict[str, dict]:
    """Get temperature and wind in Reykjavík for the specified duration."""

    type_of_data = "forec"  # Forecast.
    assert language in ("is", "en")
    result_format = "xml"
    weather_station_ids = ";".join(
        [
            str(station)
            for station in [
                1,  # Reykjavík
            ]
        ]
    )
    measures = ";".join(MEASURES)
    parameters = "&".join(
        [
            f"op_w=xml",
            f"type={type_of_data}",
            f"lang={language}",
            f"view={result_format}",
            f"ids={weather_station_ids}",
            f"params={measures}",
        ]
    )
    url = f"https://{API_URL}?{parameters}"
    response = requests.get(url=url)

    xml_str = response.content  # response.text works too.

    return extract_data_from_response(xml=xml_str, start=start, end=end)


def extract_data_from_response(
    xml: str, start: datetime, end: datetime
) -> dict[str, dict]:
    """Parse the xml response and pick out the relevant info."""
    raise NotImplementedError
