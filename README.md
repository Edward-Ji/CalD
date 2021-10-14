# Cald

A calendar app.

## Run manually

**Run calendar daemon with `python daemon.py [<database path>]`.**

If the optional database path is supplied, it is used by both the daemon and
calendar command to store all events.

**Run calendar command with `python calendar.py <action> [<option>] [<arguments>]`.**

There are four available actions detailed below:

### GET

Retrieves events from calendar database using the specified criteria.

`python calendar.py GET DATE <date>`

_All dates here and below assume the format "dd-mm-yyyy"._

`python calendar.py GET INTERVAL <start date> <end date>`

_The interval includes both start date and end date._

`python calendar.py GET NAME <name>`

_All event names here and below must match exactly and completely._

The output is in the following format with each event on a new line:

`<date> : <name> : <description>`

### ADD

Add as event with specified date and name to the database.

`python calendar.py ADD <date> <name> [<desc>]`

### UPD

Update all events matching the specified date and name with the new name and
the optional new description. If a new description is not specified, the old
description is still discarded.

`python calendar.py UPD <date> <old name> <new name> [<new description]`

### DEL

Delete all events matching the specified date and name.

`python calendar.py DEL <date> <name>`

## Run tests

There are a series of tests included in the `test` directory. Run them from the
project root. You can run them individually `./test/test_<name>` or `./test/run`
will run all tests.

## Install

A distribution is available as an alpine linux package.
