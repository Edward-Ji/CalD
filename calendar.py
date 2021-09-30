import os
import sys


# Constants for file paths
PIPE_PATH = "/tmp/cald_pipe"


def run():
    # Check if named pipe exists
    if not os.path.exists(PIPE_PATH):
        sys.stderr.write("PIPE DOESN'T EXISTS\n")
        return

    # Open named pipe in write only mode
    pipe = open(PIPE_PATH, "w")
    try:
        pipe.write(sys.argv[1] + "\n")
    except OSError:
        sys.stdout.write("Pipe has been closed\n")
    pipe.close()


if __name__ == '__main__':
    run()

