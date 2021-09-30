#!/usr/bin/env python
import signal
import os
import sys


# Constants for file paths
PIPE_PATH = "/tmp/cald_pipe"

# Use this variable in your loop
daemon_quit = False


# Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True


def run():
    # Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Create the named pipe if it does not exist
    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)

    # Open named pipe in readonly mode
    pipe = open(PIPE_PATH, "r")

    # Main loop guarded by quit flag
    while not daemon_quit:
        # Read from the named pipe
        command = pipe.readline()

        # Temporary output command
        sys.stdout.write(command)

    # Close named pipe
    pipe.close()


if __name__ == '__main__':
    run()
