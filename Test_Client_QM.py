import sys
from socket import *
import os
import datetime
import re
import logging
#loop on listening to a connection

#reading for connections make a new thread pass it to the thread
#make the whole while loop into a method
#main function get connections
#have a paser that gets the command
#buffer variables

#loop until it reads a command
# then it will parce

#parser and then have a loop on recv and wait till you get like a /n/r and then pass it to the send it to the commands
BUFFER = 8000
class MyClientFTP:
    def __init__(self, host, port):
        self.host = host
        self.port = port


#setting up of the client sever request and creating a object socket
        try:
            self.mySocket = socket(AF_INET, SOCK_STREAM)
            try:
               hostName = gethostbyname(host)
               print(hostName)
            except error:
                print("Invalid Host Name")
            self.mySocket.connect((host, port))
            ip = gethostbyname(host)
            logging.warning("Connecting to: %s\n" % ip)

        except error as e:
            print(e)
#a way to close the socket
    def close(self):
        self.mySocket.close()

#a helper function to help clear my buffer with the client receive data
    def receive(self,):
        msg_received = b""
        self.mySocket.settimeout(2)
        while True:
            try:
                buffer = self.mySocket.recv(4024)
            except timeout:
                break
            msg_received += buffer
            if len(buffer) == 0:
                break
#doesnt really work
    def severStatus(self):
        modifiedSentence2 = self.mySocket.recv(4024)
        s = []
        for t in modifiedSentence2.decode().split(","):
            try:
                s.append(int(t))
            except ValueError:
                pass

#a way to send commands to the server and also a helper function to help get the sever response and to log what is happening
    def send2(self, command):
        try:
            self.mySocket.send(bytes(command, encoding='utf8'))
            logging.warning("Sent: %s" % command)
            message = repr(self.mySocket.recv(4024))
            print(message)
            myoutput = self.myParser(message)
            logging.warning("Received: %s\n" % myoutput)
        except error:
            print("unable to send command to the host")
            exit(0)
        return myoutput

#a way to recieve data from a data socket
    def rec_data(self):
        message = b""
        print("hello")
        while 1:
            print("hello")
            buffer = self.mySocket.recv(4024)
            print(buffer)
            message += buffer
            if len(buffer) == 0:
                break
        return message
#a way to help parse out the message from the server to get nessacry information
    def myParser(self, message):
        str(message)
        if message[0] == b"":
            print(message[2:-5])
            return message[2:-5]
        else:
            print(message)
            return message

# a way to check if the socket is connected to a server
    def connected(self):
        if self.mySocket:
            return True
        else:
            return False
# a helper function to get the status code from the server
def getstatusCOde(msg):
    numArr = re.findall(r'\b\d+\b', msg)
    return numArr[0]

#a way to set wether the data socket will be pasv or active mode
def transferType():
    print("\nplease select how you would like to transfer your data?"
          "\n1. Active (PORT)\n"
          "2. Extended Active (EPRT)\n"
          "3. Passive (PASV)\n"
          "4. Extended (PASV)\n"
          )
    while True:
        val = input("Please input one of the options: ")
        if val == "1" or val == "2":
            transfer = 1
            print(transfer)
            return transfer
            break
        elif val == "3":
            transfer = 1
            return transfer
            break

        elif val == "4":
            transfer = 2
            return transfer
            break

        else:
            print("please input the correct command")

def main():

#my logging functino
    logging.basicConfig(filename='myapp.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S.%f')

#I was not able to implement my sys agruments so I just hardcoded connecting to a server so that I can show my other code works please fun main to see my code work
    # serverName = '10.246.251.93'
    serverName = '127.0.0.1'
    severPort = 2121
    newclientSocket = MyClientFTP(serverName, severPort)
#checks for user and will continue to run until a valid user is sent to the server

    a = True
    while a == True:
        newclientSocket.receive()
        try:
            val = input("Please enter User name: ")
            z = "USER %s\r\n" % val
            output = newclientSocket.send2(z)
            print(output)
            code = getstatusCOde(output)
            if code == "530":
                print("bad username")
            else:
                val2 = input("Please enter a password: ")
                y = "PASS %s\r\n" % val2
                try:
                    output2 = newclientSocket.send2(y)
                    print(output2)
                    code = getstatusCOde(output2)
                    if code == "230":
                        a = False
                    else:
                        a = True
                except:
                    print("cannot send to host")
        except error as e:
            print(e)
# a helper variable to set up transfer type
    trans = 0

#while loop to get commands form the user to interact with the ftp server
    while True:
        print("\nplease select one of the following commands \n1. Print Current Working Directory \n"
              "2. Get a list of files\n"
              "3. Change Your Working Directory\n"
              "4. Store a file\n"
              "5. Download  file\n"
              "6. Information on server\n"
              "7. Pick Transfer type\n"
              "8. Help")

        text = input("Please type your command: ")
        text = text.upper()

        newclientSocket.receive()
#sets my commands
        if trans == 1:
            #pasv connect
            try:
                newclientSocket.receive()
                pasvReq = "PASV \r\n"
                modifiedSentence3 = newclientSocket.send2(pasvReq)
                numArr = re.findall(r'\b\d+\b', modifiedSentence3)
                print(numArr)
                dilim = '.'
                newIP = (dilim.join(numArr[1:5]))
                port = (int(numArr[5]) * 256) + int(numArr[6])
                datasocket = MyClientFTP(newIP, port)
            except error as e:
                logging.warning(e)

        if trans == 2:
            #extended passive conncet
            try:
                newclientSocket.receive()
                z = "EPSV \r\n"
                msg = newclientSocket.send2(z)
                newclientSocket.receive()
                print(msg)
                newmsg = re.search(r'\((.*?)\)', msg).group(1)
                print(newmsg)
                port = newmsg.split("|")[3]
                port2 = int(port)
                newIP = newclientSocket.mySocket.getpeername()[0]

                datasocket = MyClientFTP(newIP, port2)
            except error as e:
                logging.warning(e)

        if trans == 3:
            #extended port connect
            z = "EPRT \r\n"
            ipAdd = datasocket.mySocket.getsockname()[0]
            tcpPort = datasocket.mySocket.getsockname()[1]
            request = "|" + str(1) + "|" + str(ipAdd) + "|" + str(tcpPort) + "|"
            command = "EPRT " + request + "\r\n"
            msg = newclientSocket.send2(command)
            newclientSocket.receive()
            datasocket.close()

#I could not implement port
        if trans == 4:
            print("sorry port has not been implmented yet")

#prints your current working directory
        if text == "1":
            z = "PWD \r\n"
            severmsg = newclientSocket.send2(z)
            trans = 0

#gets a list of files in the CWD
        elif text == "2" and trans != 0:
            try:
                z = "LIST \r\n"
                output2 = newclientSocket.send2(z)
                newclientSocket.receive()
                code = getstatusCOde(output2)
                if code == "425":
                    print(output2)
                else:
                    modifiedSentence2 = datasocket.rec_data().decode()[1:-1]
                    print(modifiedSentence2)
                    datasocket.close()
            except error as e:
                print(e)
            trans = 0

#changes the directory you are in
        elif text == "3":
            dir = input("What direcotry would you like to change to: ")
            try:
                z = "CWD %s\r\n" % dir
                print(z)
                newclientSocket.send2(z)
            except Exception as e:
                print("Could not change direcotry")

#store function had a few issues with it though
        elif text == "4" and trans != 0:
            file = input("please enter file name: ")
            z = "STOR %s\r\n" % file
            print(file)
            newclientSocket.send2(z)
            with open(file, "rb") as x:
                fileToRead = x.read()
                print(fileToRead)
            print(fileToRead)
            datasocket.mySocket.send(fileToRead)
            datasocket.close()
            trans = 0

#will reteive files from a server
        elif text == "5" and trans != 0:
            file = input("please enter file name: ")
            z = "RETR %s\r\n" % file
            newclientSocket.send2(z)
            packet = datasocket.rec_data()
            with open(file, "wb") as f:
                f.write(packet)
            f.close()
            datasocket.close()
            trans = 0

#will tell you the system specs
        elif text == "6":
            try:
                z = "SYST \r\n"
                severmsg = newclientSocket.send2(z)
            except error as e:
                print(e)

#wills set the transfer type
        elif text == "7":
            trans = transferType()

#did not able to set this up
        elif text == "8":
            cmd = input("please input what command you want to learn about: ")
            z = "HELP %s\r\n" %cmd
            output2 = newclientSocket.mySocket.send(z.encode())
            modifiedSentence3 = newclientSocket.mySocket.recv(2048)
            print(modifiedSentence3)

        #quit the server
        elif text == "QUIT":
            reply = "QUIT\r\n"
            newclientSocket.send2(reply)
            break
        else:
            print("invalid command\n Or you have not specifced your transfer type")
    newclientSocket.close()
if __name__ == "__main__" :
	#execute main function
	main()
