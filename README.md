# Cald

[![Docker Image CI](https://github.com/Edward-Ji/Cald/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Edward-Ji/Cald/actions/workflows/docker-image.yml)
[![Run Test CI](https://github.com/Edward-Ji/Cald/actions/workflows/run_test.yml/badge.svg)](https://github.com/Edward-Ji/Cald/actions/workflows/run_test.yml)

A calendar daemon with command line interface.

<details>
    <summary> Functionality details </summary>

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

</details>

## Testing

Tests can only be run from the repository root. You can run them individually
by specifying their path or `test/run_all` will run all tests automatically.

## Install

This project is available as an Alpine Linux build.

All the files needed to build the package is included in the `build` directory.
To build the package yourself, execute the following commands in an Alpine
Linux machine from the repository root. If you haven't setup your system and
account for `abuild`, follow
[the Alpine wiki](https://wiki.alpinelinux.org/wiki/Creating_an_Alpine_package#Setup_your_system_and_account).

```
cd build
abuild checksum && abuild -r
```

The package will be generated in the default packages directory usually
`~/packages/cald`.

Assuming all the configurations are default, install the package using

```
sudo apk add --repository /home/$USER/packages/cald cald
```

After installing the package, the daemon will automatically run upon start up
with OpenRC service. A shortcut command `calendar` is available in place of
`python3 calendar.py`. For example, you can execute the following at command
line.

```
calendar ADD 15-10-2021 "some event" "this will be amazing!"
```

You can uninstall at anytime with `sudo apk del cald`. The cald daemon will be
automatically stopped and removed from OpenRC.
