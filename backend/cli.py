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

    choice = input().strip()
    print(f"You have selected {AVAILABLE_LOCATIONS[int(choice)-1]}")
    return choice


def ask_for_time_input():
    """Ask user to specify which time they are interested in."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
