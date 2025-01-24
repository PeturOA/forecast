# forecast
An application that connects to and reads weather forecast information from the Icelandic national weather forecast service.

For the sake of simplicity, the following restrictions have been imposed for now:

1. The application only serves forecasts for Reykjavík.
This should not be that hard to extend to other weather stations, but involves some tedius manual labor.
2. The application only offers the data in Icelandic for now.
The API can serve it in English as well, and a little groundwork has been laid for offering the choice,
but proper localization remains unfinished for now.
3. The application only serves up information about temperature and wind velocity, as well as a general weather description,
but it would be possible to add the option for the user to specify other types of information to examine,
such as road temperatures, cloud coverage, humidity, air pressure etc.
4. The user interface is of course text-based, and as such very crude.
The next step will probably be to add a web-based interface (in vue preferably),
where proper tools can be applied, such as datepickers and drop-down menus.
5. Proper handling of connection problems is lacking for now.
The application simply assumes that it will always be able to connect to the API.
6. When displaying the forecasts, the predictions are not explicitly sorted.
Manual observations indicate that they consistently appear in the correct order,
although I have not been able to verify that in the relevant documentation.
So it might be a little risky to take this for granted, and an it may be prudent to sort the data explicitly,
because it would be rather confusing for the user if the data were not displayed in order.

## Installation

1. Make sure you have `python` available on your system.
2. Clone this repository (e.g. from https://github.com/PeturOA/forecast.git)
3. `pip install -r requirements.txt`

That should be enough to start using the application.


## Command line Interface

The command line interface can be started by:

```
(cd backend && python cli.py)
```
