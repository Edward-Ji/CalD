#!/bin/python
import signal
import os
import sys


# Use this variable for your loop
daemon_quit = False


# Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True


def run():
    # Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within
    # the run() funcion
    pass


if __name__ == '__main__':
    run()
