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
    logger.info(f"CHILD: {os.getpid()} is logging")

def parent():
    logger.info(f"PARENT: {os.getpid()} is logging")



# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logzero.logfile("/home/lab/Documents/DPI912/m2-redo/logs/logsrotating-logfile.log", maxBytes=1e6, backupCount=3,disableStderrLogger=True)
daemonPID=os.getpid()
#logger.info(f"Started {daemonPID}")
#daemon(childWrites)
