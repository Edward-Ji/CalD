import os
import sys
from datetime import date


# Constants for file paths
PIPE_PATH = "/tmp/cald_pipe"
LINK_PATH = "/tmp/calendar_link"


def quoted_split(line, sep=' '):
    """
    Separate a line into fields by the given separator. It a separator is
    double-quoted, it is taken literally.
    e.g. quoted_split('1 "2 3"', ' ') -> ['1', '2 3']
    """
    fields = []
    field = ""
    literal = False
    for c in line:
        if literal:
            if c == '"':
                literal = False
            else:
                field += c
        elif c == '"':
            literal = True
        elif c == sep:
            if field:
                fields.append(field)
                field = ""
        else:
            field += c
    # Unterminated literal
    if literal:
        return None

    if field:
        fields.append(field)
    return fields


def parse_date(date_string):
    """
    Wrapper for datetime formatted parse function. Returns None instead of
    throwing an exception. The string is parsed in 'dd-mm-yyyy' format.
    """
    try:
        day, month, year = map(int, date_string.split('-'))
        return date(year, month, day)
    except ValueError:
        return None


def read_db(db_path):
    db = []
    with open(db_path) as f:
        for entry in f.readlines():
            entry = entry.strip()
            if not entry:
                continue
            event_date, name, desc = quoted_split(entry, sep=",")
            event_date = parse_date(event_date)
            db.append([event_date, name, desc])
    return db


def print_entry(entry):
    event_date, name, desc = entry
    event_date = event_date.strftime("%d-%m-%Y")
    print(" : ".join((event_date, name, desc)))


# Read database path from link file
with open(LINK_PATH) as link:
    db_path = link.read()


# Write to standard error
def error(message):
    sys.stderr.write(message + "\n")


# Pipe to daemon
def daemon(command):
    try:
        with open(PIPE_PATH, "w") as pipe:
            pipe.write(command + "\n")
    except OSError as e:
        error("OSError: " + str(e))


def calendar_get_date(event_date):
    db = read_db(db_path)
    for entry in db:
        if entry[0] == event_date:
            print_entry(entry)


def calendar_get_interval(start_date, end_date):
    if start_date > end_date:
        error("Unable to Process, Start date is after End date")
        return
    db = read_db(db_path)
    for entry in db:
        if start_date <= entry[0] <= end_date:
            print_entry(entry)


def calendar_get_name(name):
    db = read_db(db_path)
    for entry in db:
        if entry[1] == name:
            print_entry(entry)


def run_get():
    if len(sys.argv) == 2:
        error("Missing action option")
    elif sys.argv[2] == "DATE":
        if len(sys.argv) == 3:
            error("Missing date argument")
        else:
            event_date = parse_date(sys.argv[3])
            if event_date is None:
                error("Unable to parse date")
            else:
                calendar_get_date(event_date)
    elif sys.argv[2] == "INTERVAL":
        if len(sys.argv) <= 4:
            error("Missing date arguments")
        else:
            start_date = parse_date(sys.argv[3])
            end_date = parse_date(sys.argv[4])
            if start_date is None or end_date is None:
                error("Unable to parse date")
            else:
                calendar_get_interval(start_date, end_date)
    elif sys.argv[2] == "NAME":
        if len(sys.argv) == 3:
            error("Please specify an argument")
        else:
            calendar_get_name(sys.argv[3])
    else:
        error("Unrecognised action option" + sys.argv[2])


def run():
    # Check if named pipe exists
    if not os.path.exists(PIPE_PATH):
        error("Pipe does not exist!")
        return

    # Open named pipe and error log using context manager
    if len(sys.argv) == 1:
        error("Missing action")
    elif sys.argv[1] == "GET":
        run_get()
    elif sys.argv[1] == "ADD":
        if len(sys.argv) == 2:
            error("Missing event date")
        else:
            event_date = parse_date(sys.argv[2])
            if event_date is None:
                error("Unable to parse date")
            if len(sys.argv) == 3:
                error("Missing event name")
            else:
                daemon(" ".join(map(lambda s: f'"{s}"', sys.argv[1:])))
    elif sys.argv[1] == "UPD":
        if len(sys.argv) == 2:
            error("Missing event date")
        else:
            event_date = parse_date(sys.argv[2])
            if event_date is None:
                error("Unable to parse date")
            elif len(sys.argv) < 5:
                error("Note enough arguments given")
            else:
                daemon(" ".join(map(lambda s: f'"{s}"', sys.argv[1:])))
    elif sys.argv[1] == "DEL":
        if len(sys.argv) == 2:
            error("Missing event date")
        else:
            event_date = parse_date(sys.argv[2])
            if event_date is None:
                error("Unable to parse date")
            if len(sys.argv) == 3:
                error("Missing event name")
            else:
                daemon(" ".join(map(lambda s: f'"{s}"', sys.argv[1:])))
    else:
        error("Unrecognised action: " + sys.argv[1])


if __name__ == '__main__':
    run()
