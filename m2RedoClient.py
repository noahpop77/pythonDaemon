#!/bin/env/python3

import argparse
from socket import *
import socket
import os
import sys
import time


# Argparse arguments
parser = argparse.ArgumentParser(description="Lotto ticketing system")
parser.add_argument('-max', '--max', type=int, help="Lotto max")
parser.add_argument('-sfn', '--sixFourNine', type=int, help="Ticket type for lotto 649 ")
parser.add_argument('-dg', '--dailyGrand', type=int, help="Ticket type for lotto daily grand ")

args = parser.parse_args()

# Gets user input for the ip address and the port to be used
ipv6Address = "::1"
portNumber = input("What port are you connecting to\n-> ")
print("\n")

# Var for appending the connection.recv output
dataRecv = ""

# Declares the socket and connects to the specified ip address and port number
forkLoop = 0

# File handling
try:
    os.remove("daemonOut.txt")
except:
    pass
outFile = open("daemonOut.txt", "a+")

##################################
if args.max:
    # Banner
    print("-------------------------- Here are your tickets!!! --------------------------")
    
    # Fork loop counter
    forkLoop = int(args.max)

    # Fork loop
    for i in range(int(args.max)):

        # Time delay
        time.sleep(0.01)

        try:
            # Create fork
            pid = os.fork()

            # Code the child is going to run
            if pid == 0:
                # Creates socket connection
                mySocket = socket.socket(AF_INET6, SOCK_STREAM)
                mySocket.connect((ipv6Address,int(portNumber)))
                

                # Sends and receives the information to the server
                mySocket.send("max:1".encode('utf-8'))
                dataRecv += mySocket.recv(4096).decode('utf-8') #+ "\n"
                
                # Saves ticket information to a file
                outFile.write(str(dataRecv))
                # Print ticket information
                print(str(dataRecv))
                
                # Close socket and kill child
                mySocket.close()
                sys.exit(0)
        # Error catch
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

##################################
elif args.sixFourNine:
    print("-------------------------- Here are your tickets!!! --------------------------")
    # Fork loop counter
    forkLoop = int(args.sixFourNine)

    # Fork Loop
    for i in range(int(args.sixFourNine)):
        # Time delay
        time.sleep(0.005)
        
        # Loop counter
        #print("Loop number = " + str(i))
        try:
            # Create fork
            pid = os.fork()

            # Code the child is going to run
            if pid == 0:
                # Creates socket connection
                mySocket = socket.socket(AF_INET6, SOCK_STREAM)
                mySocket.connect((ipv6Address,int(portNumber)))
                
                # Sends and receives the information to the server
                mySocket.send("sixFourNine:1".encode('utf-8'))
                dataRecv += mySocket.recv(4096).decode('utf-8') #+ "\n"

                # Saves ticket information to a file
                outFile.write(str(dataRecv))
                # Print ticket information
                print(str(dataRecv))
                
                # Close socket and kill child
                mySocket.close()
                sys.exit(0)
        # Error catch
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

##################################
elif args.dailyGrand:
    print("-------------------------- Here are your tickets!!! --------------------------")
    # Fork loop counter
    forkLoop = int(args.dailyGrand)

    #Loop for fork
    for i in range(int(args.dailyGrand)):
        # Time delay
        time.sleep(0.005)
        
        # Loop counter
        #print("Loop number = " + str(i))
        try:
            # Create fork
            pid = os.fork()

            # Code the child is going to run
            if pid == 0:
                # Creates socket connection
                mySocket = socket.socket(AF_INET6, SOCK_STREAM)
                mySocket.connect((ipv6Address,int(portNumber)))
                
                # Sends and receives the information to the server
                mySocket.send("dailyGrand:1".encode('utf-8'))
                dataRecv = mySocket.recv(4096).decode('utf-8')

                # Saves ticket information to a file
                outFile.write(str(dataRecv))
                # Print ticket information
                print(str(dataRecv))
                
                # Close socket and kill child
                mySocket.close()
                sys.exit(0)
        # Error catch
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
# If the argparse doesnt catch the incorrect user input then this will, it will simply exit the program if something is entered that isn't max, sfn, or dg
else:
    sys.exit(0)

# Closes output file
outFile.close()

# waits for the forks to end
for i in range(forkLoop):
    finishedFork = os.waitpid(0, os.WNOHANG)
