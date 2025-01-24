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

    raise NotImplementedError


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


def ask_for_time_input():
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


def ask_for_desired_time():
    """Ask the user to specify a single point for which to check the forecast."""
    raise NotImplementedError


def ask_for_desired_period():
    """Ask the user to specify two ends of a forecast interval."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
