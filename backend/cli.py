# Standard library imports.
from datetime import datetime, timedelta

# Third party imports.

# Local application imports.
import weather_service as ws


YES, NO = "Y", "N"
AVAILABLE_LOCATIONS = (
    "Reykjavík",
    # "Grindavík",
    # "Keflavík",
    # "Stykkishólmur",
    # "Patreksfjörður",
    # "Ísafjörður",
    # "Hólmavík",
    # "Blönduós",
    # "Siglufjörður",
    # "Grímsey",
    # "Akureyri",
    # "Húsavík",
    # "Raufarhöfn",
    # "Egilstaðir",
    # "Fáskrúðsfjörður",
    # "Höfn í Hornafirði",
    # "Skaftafell",
    # "Kirkjubæjarklaustur",
    # "Vík í Mýrdal",
    # "Vestmannaeyjar",
    # "Hella",
    # "Þingvellir",
)


def main():
    """Prompt user for input and display the desired data.

    Repeat the process as long as the user's curiosity prevails.
    """
    bid_welcome()

    report_forecast()
    while keep_going():
        report_forecast()


def bid_welcome() -> None:
    """Greet user."""
    print("Good day, I hope. Well, we shall see, perhaps.")


def report_forecast() -> None:
    """Ask user for input and display the forecast data."""
    if len(AVAILABLE_LOCATIONS) == 1:
        location = AVAILABLE_LOCATIONS[0]
        print(f"At the moment, the forecast is only available for {location}.")
    else:
        location = ask_for_location_input()

    start, end = ask_for_time_input()

    forecast = ws.fetch_forecast(start=start, end=end)
    present_results(forecast)


def keep_going() -> bool:
    """Ask user if they want to continue."""
    print("Do you want to know more? (Y)es/(N)o.")
    answer = input()
    return answer.upper() == YES


def ask_for_location_input():
    """Ask user to specify which area they are interested in."""
    print("Please select a location to enquire about.")
    print("The following locations are available at the moment:")
    print(
        "\n".join(
            [f"{idx+1}. {location}" for idx, location in enumerate(AVAILABLE_LOCATIONS)]
        )
    )
    print("Please enter the number given in front of the option you want.")

    num_options = len(AVAILABLE_LOCATIONS)
    while (choice := input().strip()) not in (f"{idx+1}" for idx in range(num_options)):
        print(f"{choice} is not one of the available options.")
        print(f"Please enter a number between 1 and {num_options} (inclusive).")

    print(f"You have selected {AVAILABLE_LOCATIONS[int(choice)-1]}")
    return choice


def ask_for_time_input() -> tuple[datetime]:
    """Ask user to specify which time they are interested in."""
    print("Please choose whether you want the weather forecast for:")
    print("1. One specific point in time.")
    print("2. The interval between two specific points in time.")

    while (choice := input().strip()) not in ("1", "2"):
        print(f"'{choice}' is neither '1' nor '2'.")
        print("Please enter either '1' or '2'.")

    assert choice in ("1", "2")
    if choice == "1":
        start = end = ask_for_desired_time()
        return start, end
    else:
        assert choice == "2"
        return ask_for_desired_period()


def ask_for_desired_time() -> datetime:
    """Ask the user to specify a single point for which to check the forecast."""
    print("For what time would you like to see the forecast?")
    return ask_for_time_point()


def ask_for_time_point() -> datetime:
    print("What day? '0' for today, '1' for tomorrow, etc.")
    while not valid_day(days_ahead := input().strip()):
        print("Please enter a non-negative integer")

    print("At which hour? (Integer from 0 to 23):")
    while not valid_hour(hour := input()):
        print("Please enter an integer between 0 and 23 (inclusive).")

    time = datetime.today() + timedelta(int(days_ahead))
    time = time.replace(hour=int(hour), minute=0, second=0, microsecond=0)
    print(f"You have selected the date {time}")
    return time


def valid_day(days: str) -> bool:
    try:
        number_of_days = int(days)
        return number_of_days >= 0
    except ValueError:
        return False


def valid_hour(hour: str) -> bool:
    try:
        hour = int(hour)
        return 0 <= hour <= 23
    except ValueError:
        return False


def ask_for_desired_period() -> tuple[datetime]:
    """Ask the user to specify two ends of a forecast interval."""
    print("Please specify first one end of the period you want.")
    start = ask_for_time_point()

    print("Now the other end.")
    end = ask_for_time_point()

    if end < start:
        start, end = end, start

    return (start, end)


def present_results(forecast: dict) -> None:
    """Display the forecast in a somewhat readable format."""
    print("The forecast for the selectd time is as follows:")
    for station in forecast.values():
        print(f"\t{station['name']}")
        predictions = station["predictions"]

        if not predictions:
            print("No forecast available for the specified time.")
            closest = []

            last_before = station["last_before"]
            if last_before is not None:
                closest.append(last_before)

            first_after = station["first_after"]
            if first_after is not None:
                closest.append(first_after)

            if closest:
                print("The closest forecast is as follows:")
                predictions = closest

        print(
            f"{'time':20}",
            f"{'temperature':13}",
            f"{'windspeed(m/s)':16}",
            f"{'direction':13}",
            f"{'description':13}",
            sep="",
        )

        for prediction in predictions:
            print(f"{prediction['time']:20}", end="")
            for measure in ws.MEASURES:
                print(f"{prediction[measure]:^14}", end="")

            print()


if __name__ == "__main__":
    main()
