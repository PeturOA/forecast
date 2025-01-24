# Standard library imports.
from datetime import datetime, timedelta
import requests

# Third party imports.
import defusedxml.ElementTree as ET

# Local application imports.


API_URL = "xmlweather.vedur.is"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # "YYYY-MM-DD hh:mm:ss"
ICELANDIC = "is"
ENGLISH = "en"
LANGUAGES = (ICELANDIC, ENGLISH)
TEMPERATURE = "T"
DIRECTION = "D"
WINDSPEED = "F"
DESCRIPTION = "W"
MEASURES = (TEMPERATURE, WINDSPEED, DIRECTION, DESCRIPTION)
STATUS_OK = 200


def take_the_xml_parser_for_a_spin() -> None:
    """Look up weather forecast for the next 24 hours."""
    today = datetime.now()
    tomorrow = today + timedelta(1)
    fetch_forecast(start=today, end=tomorrow)


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

    assert response.status_code == STATUS_OK
    xml_str = response.content  # response.text works too.

    return extract_data_from_response(xml=xml_str, start=start, end=end)


def extract_data_from_response(
    xml: str, start: datetime, end: datetime
) -> dict[str, dict]:
    """Parse the xml response and pick out the relevant info."""

    xml_root = ET.fromstring(xml)

    data = {}
    for station in xml_root:
        predictions = []
        last_before = None
        first_after = None

        for forecast in station.findall("forecast"):
            time_str = forecast.find("ftime").text
            time = datetime.strptime(time_str, DATE_FORMAT)
            forecast_info = {"time": time}
            for measure in MEASURES:
                forecast_info[measure] = forecast.find(measure).text

            if start <= time <= end:
                predictions.append(forecast_info)
            else:
                last_before, first_after = update_bounds(
                    forecast_info, start, end, last_before, first_after
                )

        id = station.attrib["id"]
        data[id] = {
            "name": station.find("name").text,
            "last_before": last_before,
            "predictions": predictions,
            "first_after": first_after,
        }

    return data


def update_bounds(
    current_forecast: dict,
    start: str,
    end: str,
    last_before,
    first_after,
) -> tuple:
    """Update lower or upper bounds if new time is closer to the desired interval."""

    new_time = current_forecast["time"]
    if new_time < start:
        # Before desired interval. Only keep the closest one,
        # in case no data is available within the interval.
        if last_before is None:
            last_before = current_forecast
        elif last_before["time"] < new_time:
            assert last_before["time"] < new_time < start
            last_before = current_forecast

    else:
        assert end < new_time
        # After desired interval. Only keep the closest one,
        # in case no data is available within the interval.
        if first_after is None:
            first_after = current_forecast
        elif new_time < first_after["time"]:
            assert end < new_time < first_after["time"]
            first_after = current_forecast

    return last_before, first_after


if __name__ == "__main__":
    take_the_xml_parser_for_a_spin()
