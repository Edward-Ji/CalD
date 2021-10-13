#!/usr/bin/env python

import signal
import os
import sys

sys.path.append(sys.path.pop(0))
from datetime import datetime


# Constants for file paths
PIPE_PATH = "/tmp/cald_pipe"
LINK_PATH = "/tmp/calendar_link"
ERRLOG_PATH = "/tmp/cald_err.log"


# Write to error log
def error(message):
    if not os.path.exists(ERRLOG_PATH):
        open(db_path, "w").close()
    with open(ERRLOG_PATH, "a") as f:
        f.write(message + "\n")


# Craete and link datebase
if len(sys.argv) < 2:
    # Use default database path if not specified
    db_path = os.path.join(os.path.dirname(__file__), "cald_db.csv")
else:
    # User database path argument if specified
    db_path = sys.argv[1]
# Create empty database if it does not exist
if not os.path.exists(db_path):
    open(db_path, "w").close()
# Write database path to link file
with open(LINK_PATH, "w") as link:
    link.write(db_path)

# Create the named pipe if it does not exist
if not os.path.exists(PIPE_PATH):
    try:
        os.mkfifo(PIPE_PATH)
    except OSError as e:
        error(f"OSError: {e}")


# ================
# Helper functions
# ================
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
        return datetime.strptime(date_string, "%d-%m-%Y").date()
    except ValueError:
        return None


def read_db(db_path):
    db = []
    with open(db_path) as f:
        for entry in f.readlines():
            entry = entry.strip()
            if not entry:
                continue
            date, name, desc = quoted_split(entry, sep=",")
            date = parse_date(date)
            db.append([date, name, desc])
    return db


read_db(db_path)


def write_db(db_path, db):
    with open(db_path, "w") as f:
        for entry in db:
            date, name, desc = entry
            date = datetime.strftime(date, "%d-%m-%Y")
            if "," in name:
                name = f'"{name}"'
            if "," in desc:
                desc = f'"{desc}"'
            f.write(",".join((date, name, desc)) + "\n")


# ==================
# Calendar functions
# ==================
def calendar_add(date, name, desc=""):
    db = read_db(db_path)
    db.append([date, name, desc])
    write_db(db_path, db)


def calendar_upd(date, name, new_name, new_desc=""):
    db = read_db(db_path)
    for entry in db:
        if entry[0] == date and entry[1] == name:
            entry[1] = new_name
            entry[2] = new_desc
    write_db(db_path, db)


def calendar_del(date, name):
    db = read_db(db_path)
    for entry in db:
        if entry[0] == date and entry[1] == name:
            db.remove(entry)
    write_db(db_path, db)


# Daemon quit handling
daemon_quit = False


def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True


def run():
    # Reconfigure interrupt signal
    signal.signal(signal.SIGINT, quit_gracefully)

    # Open named pipe in readonly mode
    pipe = open(PIPE_PATH)

    # Main loop guarded by quit flag
    while not daemon_quit:
        # Read from the named pipe
        command = pipe.readline().strip()

        if not command:
            continue

        args = quoted_split(command)
        if args is None:
            error("Unterminated literal")
        elif args[0] == "ADD":
            if len(args) == 1:
                error("Missing event date")
            else:
                date = parse_date(args[1])
                if date is None:
                    error("Unable to parse date")
                if len(args) == 2:
                    error("Missing event name")
                else:
                    calendar_add(date, *args[2:4])
        elif args[0] == "UPD":
            if len(args) == 1:
                error("Missing event date")
            else:
                date = parse_date(args[1])
                if date is None:
                    error("Unable to parse date")
                elif len(args) < 4:
                    error("Note enough arguments given")
                else:
                    calendar_upd(date, *args[2:5])
        elif args[0] == "DEL":
            if len(args) == 1:
                error("Missing event date")
            else:
                date = parse_date(args[1])
                if date is None:
                    error("Unable to parse date")
                if len(args) == 2:
                    error("Missing event name")
                else:
                    calendar_del(date, args[2])
        else:
            error("Unrecognised action: " + args[0])

    # Close named pipe
    pipe.close()


if __name__ == '__main__':
    run()
