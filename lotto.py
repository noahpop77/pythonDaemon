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


# Defined function that produces lotto 649 numbers
def lottoSixFourNine(ticketCount):
    outString = ""
    for i in range(ticketCount):
        lottoNumbers = []
        # loops 7 times (once per how many numbers you want)
        for i in range(0, 7):
            # appends random number within a range to lottoNumbers list
            random.seed()
            tempNumber = random.randint(1,49)
            if tempNumber not in lottoNumbers:
                lottoNumbers.append(str(tempNumber))
        
        outString += "Ticket: "
        for i in lottoNumbers:
            outString = outString + str(i) + " "
        outString += "\n"
    return outString
    
# Defined function that produces Daily Grand numbers
def dailyGrand(ticketCount):
    outString = ""
    for i in range(ticketCount):
        lottoNumbers = []
        # loops 5 times (once per how many numbers you want)
        for i in range(0, 5):
            #appends random number in a range to lottoNumbers list
            random.seed()
            tempNumber = random.randint(1,49)
            if tempNumber not in lottoNumbers:
                lottoNumbers.append(str(tempNumber))

        outString += "Ticket: "
        for i in lottoNumbers:
            outString = outString + str(i) + " "
        outString += "\n"
    return outString

# Defined function that produces lotto max numbers
def lottoMax(ticketCount):
    outString = ""
    for i in range(ticketCount):
        lottoNumbers = []
        # loops 7 times (once per how many numbers you want)
        for i in range(0, 7):
            # appends a random number to the lottoNumbers list
            random.seed()
            tempNumber = random.randint(1,49)
            if tempNumber not in lottoNumbers:
                lottoNumbers.append(str(tempNumber))
                
        outString += "Ticket: "
        for i in lottoNumbers:
            outString = outString + str(i) + " "
        outString += "\n"
    return outString