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
    raise NotImplementedError


def report_forecast() -> None:
    """Ask user for input and display the forecast data."""
    raise NotImplementedError


def keep_going() -> bool:
    """Ask user if they want to continue."""
    raise NotImplementedError



if __name__ == "__main__":
    main()