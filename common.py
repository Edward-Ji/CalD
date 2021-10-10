from datetime import datetime
import sys
import os

# Prevent my calendar from being imported
sys.path.pop(0)


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


def print_entry(entry):
    date, name, desc = entry
    date = datetime.strftime(date, "%d-%m-%Y")
    print(" : ".join((date, name, desc)))


if __name__ == '__main__':
    # test quoted_split()
    print(quoted_split("calendar GET DATE 06-07-1977"))
    print(quoted_split("calendar GET INTERVAL 06-07-1977 07-06-1978"))
    print(quoted_split('calendar GET NAME "Birthday Party"'))
    print(quoted_split('calendar ADD 19-11-1986 "Jeff\'s Cake Day!" '
                       '"It\'s for jeff!"'))
    print(quoted_split('calendar UPD 18-05-2018 "Tea Break" "Tee Break"'))
    print(quoted_split('calendar DEL 20-04-2014 "Boring Meeting"'))

    # test parse_date()
    print(f"{parse_date('06-07-1977') = }")
    print(f"{parse_date('32-07-1977') = }")
    print(f"{parse_date('31-07-77') = }")
