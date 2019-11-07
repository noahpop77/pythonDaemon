#!/bin/env python3


#==============================================================================
 #   Assignment:  Milestone 3, Logging Daemon
 #
 #       Author:  Brian Sawa
 #     Language:  Writen in python 3.7.3 using the libraries sys, os, argparse, socket, signal, errno, random, atexit, lgozero, and the rest were imports from the other files that contain my code
 #   To Compile:  n/a
 #
 #        Class:  DPI912 
 #    Professor:  Harvey Kaduri
 #     Due Date:  Wendsdat November 6th 2019 11:59PM
 #    Submitted:  Wendsday November 6th 2019
 #
 #-----------------------------------------------------------------------------
 #
 #  Description:  This program solves the problem of a multiprocessing environment being able to provide simultaneous connections and data return to multiple users.
 #
 #        Input:  The main daemon script takes in a command line argument of -start or -stop to start or stop the daemon, after that the client script takes in the arguments of the ticket type and number.
 #
 #       Output:  Lottery ticket numbers
 #
 #    Algorithm:  The main approach used was that of forking off children processes for asyncronisity and security of the daemon
 #
 #   Required Features Not Included: Detaches itself from the terminal without &
 #
 #   Known Bugs: For some reason, randomly at a rate of give or take, 1 out of 4, a fork dies
 #
 #   Classification: B
 #
#==============================================================================



# Imported libraries
import sys
import os
import argparse
import signal
from socket import *
import socket
import errno
import random
import atexit

import logzero
from logzero import logger

from childParent import cull
from childParent import child
from childParent import parent

import forkDaemon
from forkDaemon import *
from myDaemon import *

from lotto import *

parser = argparse.ArgumentParser(description="Lotto ticketing system")
parser.add_argument('-start', action='store_true', help="Start or stop the daemon")
parser.add_argument('-stop', action='store_true', help="Stops daemon")

args = parser.parse_args()
#os.setuid(1)

def daemonize(self):
    try:
            pid = os.fork()
            if pid > 0:
                    # exit first parent
                    sys.exit(0)
    except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

    # decouple from parent environment
    os.chdir("/tmp/")
    os.setsid()
    os.umask(0)

    # do second fork
    try:
            pid = os.fork()
            if pid > 0:
                    # exit from second parent
                    sys.exit(0)
    except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()

    si = file(self.stdin, 'r')
    so = file(self.stdout, 'a+')
    se = file(self.stderr, 'a+', 0)

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    # write pidfile
    atexit.register(self.delpid)
    file(self.pidfile,'w+').write("%s\n" % pid)


try:
    checkPid = open("/var/run/pidDir/pidFile", "r")
    pidFileContents = str(checkPid.read())
    checkPid.close()
except FileNotFoundError:
    pidFileContents = 0
try:
    if len(pidFileContents) > 0:
        sys.exit(1)
except:
    pass

#os.system("rm -rf /var/run/pidDir/*")

if args.start:
    #os.chown("/var/run/pidDir", 1, 1)
    pidFile = open("/var/run/pidDir/pidFile", "w+")
    pidFile.write(f"{os.getpid()}")
    pidFile.close()
elif args.stop:
    pidFileCheck = open("/var/run/pidDir/pidFile", "r")
    os.system(f"kill {pidFileCheck.read()}")
    os.system("rm -rf /var/run/pidDir/pidFile")
    sys.exit()
elif len(sys.argv) <= 1:
    sys.exit(0)

# Server asks user for input on which port they wanna operate on
portNumber = 1212

logzero.logfile("/home/lab/Documents/DPI912/m2-redo/logs/logsrotating-logfile.log", maxBytes=1e6, backupCount=3,disableStderrLogger=True)
childWrites = "And now, for something completely different"
logger.info(f"Started {os.getpid()}")


# Main loop for the daemon
while True:
    connection = None
    address = None
    # Accepts the incoming connection once one is ended
    # Socket gets declared
    serverSocket = socket.socket(AF_INET6, SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        
    # Socket is bound to the user specified port
    serverSocket.bind(("",int(portNumber)))
    serverSocket.listen(100)

    # Waits to accept an incomming connection
    connection, address = serverSocket.accept()

    if connection is not None and address is not None:
        daemonize
        parent()
        pid = os.fork()
        
        if pid > 0:
            parent()
            serverSocket.close()
        elif pid == 0:
            child()
            manualDaemon(connection, address)
            sys.exit(0)
        else:
            serverSocket.close()
            sys.exit(0)
