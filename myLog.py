#!/usr/bin/python3
import os
import signal
import time
import logzero
from logzero import logger

def cull(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,          # Wait for any child process
                os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return

        if pid == 0:  # no more zombies
            return

def child():
    logger.info(f"CHILD: {os.getpid()} {childWrites}")

def parent():
    logger.info( f"PARENT: {os.getpid()} is logging")


def daemon(childWrites):
        forks=5
        signal.signal(signal.SIGCHLD, cull)
        for i in range(forks):
            try:
                processID = os.fork()
            except OSError:
                sys.stderr.write("Could not create a child process\n")
                logger.error("Could not create a child process")
                continue

            if processID==0:
                child()
                exit(0)
            else:
                parent()


if __name__ == '__main__':
    # Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
    logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1e6, backupCount=3,disableStderrLogger=True)
    childWrites = "And now, for something completely different"
    daemonPID=os.getpid()
    logger.info(f"Started {daemonPID}")
    daemon(childWrites)
