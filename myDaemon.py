#!/bin/env/python3

# Imported libraries
import sys
import os
import argparse
import signal
from socket import *
import socket
import errno
import random
from lotto import *

# Function to handle the communication between the child process and the client
def manualDaemon(connection, address):

    # Flushes input, output and error streams
    sys.stdin.flush()
    sys.stdout.flush()
    sys.stderr.flush()

    # Formats the data we recieve on input for processing
    fullMessage = connection.recv(4096).decode('utf-8')
    splitMessage = fullMessage.split(":")
    ticketString = ""
    
    # Loops through all of the inputted CLI params and gets the desired output
    for i in splitMessage:
        # First answer is max for example
        fieldAnswer = splitMessage[0]
        # Second answer is the number of tickets they want
        fieldAnswerCount = splitMessage[1]

        # Actual function calls that are made based on the user input to get the information they requested.
        if fieldAnswer == "max":
            ticketString = str(lottoMax(int(fieldAnswerCount)))
        elif fieldAnswer == "dailyGrand":
            ticketString = str(dailyGrand(int(fieldAnswerCount)))
        elif fieldAnswer == "sixFourNine":
            ticketString = str(lottoSixFourNine(int(fieldAnswerCount)))
    
    #print(str(ticketString))
    connection.send(str(ticketString).encode('utf-8'))
    # Closes connection
    connection.close()
