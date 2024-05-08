![](https://raw.githubusercontent.com/moorejacob2017/Stricture/master/logos/stricture_logo_white_long.png)

Stricture is a python package that provides classes and a CLI tool for easy scheduling, automating, and managing specific operations.

Currently, Stricture provides 5 classes:
- `Schedule` - Used to determine if the current date and time falls within a user defined schedule. Provides a variety of functionality that promotes human readable schedules, ranging from broad week-to-week bases, to granular date and time ranges.
- `Stricture` - A class used to abstract the idea of starting and stopping a specified operation or process based on a `Schedule` or other condition. User supplied functions are orchestrated by a templated function to launch, pause, resume, and check conditions for an operation.
- `ProcessStricture` - A differentiated `Stricture` used to start and stop local system processes given a `Schedule` or other condition.
- `Command` - A basic utility for easily running terminal commands and collecting their output.
- `CommandStricture` - A differentiated `Stricture` used to start and stop terminal commands (using the `Command` Class) given a `Schedule` or other condition.

Please review the [Stricture Documentation](https://github.com/moorejacob2017/Stricture/README.md) for more information.