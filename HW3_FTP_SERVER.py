"""
Quentin McKnight
HW3 FTP server
CS472
"""
import sys
from socket import *
import os
import datetime
import re
import subprocess
import logging
#userlist for correct users
USERLIST = {
    "QTM23": ["username1"],
    "ELL33":["username2"],
    "CS472": ["username3"],
    "HWW34": ["username4"],
    "BAS37": ["username5"],
}

#pasword list
PASSWORDS = {
    "1": ["1"],
    "224":["224"],
    "123": ["123"],
    "12345": ["12345"],
    "123456": ["123456"],
}

BUFFER = 4048
"""A helper class for sockets to send and recive data"""
class socketClass:
    def __init__(self, mySocket,host, port):
        self.mySocket = mySocket
        logging.warning("Connection Established\n")
        self.host = host
        self.port = port
#setting up of the client sever request and creating a object socket
    def connect(self,host,port):
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
# a way to check if the socket is connected to a server
    def connected(self):
        if self.mySocket:
            return True
        else:
            return False

#a helper function to help clear my buffer
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
#a modfited send that send it in bytes and also will log the messages
    def send2(self, command):
        try:
            self.mySocket.send(bytes(command, encoding='utf8'))
            logging.warning("Sent: %s" % command)
        except error as e:
            logging.warning("ERROR: %s\n" % e)
            logging.warning("unable to send command to the client\n")
# a helper function for recive that will also return a parsed message from the client
    def recv2(self):
        try:
            message = repr(self.mySocket.recv(4024))
            myoutput = self.myParser(message)
            logging.warning("Received: %s\n" % myoutput)
            return myoutput
        except error as e:
            logging.warning("ERROR: %s" % e)
            logging.warning("unable to receive command to the client")

#a way to recieve data from a data socket byte by byte until the buffer is empty
    def rec_data(self):
        message = b""
        while 1:
            buffer = self.mySocket.recv(4024)
            print(buffer)
            message += buffer
            if len(buffer) == 0:
                break
        return message

#a way to help parse out the message from the server to get nessacry information
    def myParser(self, message):
        str(message)
        if message[0] == "b":
            return message[2:-5]
        else:
            return message

class ftpServer():

    """ this is my FTP sever class where it stores the sever socket between client and sever the port and the IP"""
    def __init__(self, mySocket, ip, port):
        self.mySocket = mySocket
        self.ip = ip
        self.port = port
        #creates a socket class with helper functions
        logging.warning("Starting Quentin McKnights Server\n")
        clientSocket = socketClass(mySocket, ip, port)
        servCmd = "200 Welcome to Quentin's McKnights CS472 FTP sever\r\n"
        clientSocket.send2(servCmd)
        out = clientSocket.recv2()
        """ This is the start of my User and password loop it will keep running into you give it a validd command or a valid login until then it will keep asking """
        while True:
            cmd = out.split(" ")[0].strip('\r\n')
            userdata = out.split(" ")[1].strip('\r\n')
            try:
                #checks if cmd is user and if in userlist
                if cmd == "USER" and userdata.upper() in USERLIST:
                    print("User %s is valid" % userdata)
                    serverReply = "331 Please Provide Password\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                    cmd = out.split(" ")[0].strip('\r\n')
                    userdata = out.split(" ")[1].strip('\r\n')

                    #checks if cmd is PASS and password is in the password list
                    if cmd == "PASS" and userdata in PASSWORDS:
                        serverReply = "230 Successful Login\r\n"
                        clientSocket.send2(serverReply)
                        out = clientSocket.recv2()
                        break
                    #if we got the user but password was incorrect
                    elif cmd == "PASS" and userdata not in PASSWORDS:
                        print("Password %s invalde" % userdata)
                        serverReply = "530 Invalid Login\r\n"
                        clientSocket.send2(serverReply)
                        out = clientSocket.recv2()

                    #if we got the USER cmd but its not in the USERlist
                elif cmd == "USER" and userdata.upper() not in USERLIST:
                    print("User %s invalde" % userdata)
                    serverReply = "530 Invalid Login\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                #if invalid cmd is given
            except Exception as a:
                serverReply = "500 Syntax error, command unrecognized.\r\n"
                clientSocket.send2(serverReply)
                out = clientSocket.recv2()

        while True:
            """The start of a loop where commands are parsed out and then checked and handled"""
            cmd = out.split(" ")[0].strip('\r\n')
            print(cmd) #for debbuging purposes
            #print working Directory
            if cmd == "PWD":
                try:
                    #uses system os to get current working directory then sending
                    serverReply = "257 current working Directory is: %s\r\n" % (os.getcwd())
                    clientSocket.send2(serverReply)
                    #leaves a recv open for the next client command
                    out = clientSocket.recv2()
                except Exception as a:
                    serverReply = "500 Syntax error, command unrecognized.\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                    print("Error: " + str(a) + "\nPlease retry")

            #change working directory
            elif cmd == "CWD":
                userdata = out.split(" ")[1].strip('\r\n')
                #checks if the path exist then changes the directory
                if os.path.exists(userdata):
                    os.chdir(userdata)
                    serverReply = "250 successful directory change to: %s\r\n" % (os.getcwd())
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                else:
                    serverReply = "550 Unsuccessful directory change\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()

            #goes up one directroy
            elif cmd == "CDUP":
                if os.path.exists('..'):
                    os.chdir('..')
                    serverReply = "250 successful directory change to %s\r\n" % (os.getcwd())
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                else:
                    serverReply = "550 Unsuccessful directory change\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()

            #switches to passive mode
            elif cmd == "PASV":
                try:
                    hostname = gethostname()
                    #opens up a new data socket
                    datasocket = socket(AF_INET, SOCK_STREAM)
                    datasocket.bind((hostname, 0))
                    hostPort = datasocket.getsockname()[1]
                    datasocket.listen(1)
                    ipsend = self.ip.replace(".", ",")
                    p1 = str(int((hostPort - (hostPort % 256)) / 256))
                    p2 = str(hostPort % 256)
                    pasmsg = "(" + ipsend + "," + p1 + "," + p2 + ")"
                    serverReply = "277 Entering Passive Mode %s\r\n" % pasmsg
                    clientSocket.send2(serverReply)
                    #listens for data connection
                    out = clientSocket.recv2()
                    dataSS, addr = datasocket.accept()
                    #creates data socket class
                    dataS = socketClass(dataSS, hostname, hostPort)
                    #ready to recive next client cmd
                except error as e:
                    logging.warning("Error: %s\n" % e)
                    print(e)

            #extended passive

            elif cmd == "EPSV":
                try:
                    hostname = gethostname()
                    #opens up a data socket
                    datasocket = socket(AF_INET, SOCK_STREAM)
                    #binds it
                    datasocket.bind((hostname, 0))
                    #starts to listen for connection
                    datasocket.listen(5)
                    hostPort = datasocket.getsockname()[1]
                    IPV = 1
                    ip_address = clientSocket.mySocket.getsockname()[0]
                    epmsg ='|' + str(IPV) + '|' + str(ip_address) + '|' + str(hostPort) + '|'
                    serverReply = "227 Entering Passive Mode (%s)\r\n" % epmsg
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                except error as e:
                    logging.warning("Error: %s\n" % e)
                    print(e)
                try:
                    #creates data socket for later
                    dataSS, addr = datasocket.accept()
                    dataS = socketClass(dataSS, hostname, hostPort)
                except error as e:
                    logging.warning("Error: %s\n" % e)
                    print(e)
                    print("could not connect")
                # ready to recive next client cmd


            elif cmd == "PORT":
                """I could not figure out how to do this becasue it didnt work on my client side which I was testing with"""
                clientSocket.send2("502 Command not implemented.\r\n")
                out = clientSocket.recv2()

            elif cmd == "EPRT":
                """I could not figure out how to do this becasue it didnt work on my client side which I was testing with"""
                clientSocket.send2("502 Command not implemented.\r\n")
                out = clientSocket.recv2()

            #list of files
            elif cmd == "LIST":
                #check if the data connection exist
                if dataS.connected() == True:
                    #gets a list of the current directory you are in turns it into bytes
                    data = subprocess.check_output(['ls', '-l']).replace(b'\n', b'\r\n')
                    try:
                        dataS.mySocket.send(data)
                        logging.warning("Sent: %s\r\n" % data.decode())
                        dataS.close()
                        clientSocket.send2("150 prepare for data\r\n")
                    #if file can not be sent
                    except error as e:
                        clientSocket.send2("450 Requested file action not taken.\r\n")
                        logging.warning("Error: %s\n" % e)
                        out = clientSocket.recv2()
                    serverReply = "226 Successful transfer\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                else:
                    clientSocket.send2("425 Establish a data connection first.\r\n")
                    out = clientSocket.recv2()
            #retriving and storing files
            elif cmd == "STOR":
                # check if the data connection exist
                if dataS.connected() == True:
                    try:
                        userdata = out.split(" ")[1].strip('\r\n')
                        clientSocket.send2("150 prepare for data\r\n")
                        msg = dataS.rec_data()
                        logging.warning("Receiving the file: %s\r\n" % userdata)
                        #will write the file byte by byte
                        with open(userdata, 'wb') as f:
                            f.write(msg)
                        f.close()
                        logging.warning("This data was received: %s\r\n" % msg.decode())
                    #if file can not be sent
                    except error as e:
                        clientSocket.send2("450 Requested file action not taken.\r\n")
                        logging.warning("Error: %s\n" % e)
                        out = clientSocket.recv2()
                    # file was able to be sent
                    serverReply = "226 Successful transfer\r\n"
                    clientSocket.send2(serverReply)
                    out = clientSocket.recv2()
                    dataS.close()
                else:
                    clientSocket.send2("425 Establish a data connection first.\r\n")
                    out = clientSocket.recv2()
            #storing files from the client
            elif cmd == "RETR":
                if dataS.connected() == True:
                    try:
                        userdata = out.split(" ")[1].strip('\r\n')
                        serverReply = "150 prepare for data\r\n"
                        clientSocket.send2(serverReply)
                        #opens up the file and read its bytes in
                        with open(userdata, "rb") as x:
                            fileToRead = x.read()
                            print(fileToRead)
                        x.close()
                    except error as e:
                        #if get the data will send this
                        clientSocket.send2("450 Requested file action not taken.\r\n")
                        logging.warning("Error: %s\n" % e)
                        out = clientSocket.recv2()
                    #file was able to be stored
                    dataS.mySocket.send(fileToRead)
                    logging.warning("Sending the file %s to the client:\r\n" % userdata)
                    logging.warning("The data was sent: %s\r\n" % fileToRead.decode())
                    serverReply = "226 Successful transfer\r\n"
                    clientSocket.send2(serverReply)
                    dataS.close()
                    out = clientSocket.recv2()
                else:
                    clientSocket.send2("425 Establish a data connection first.\r\n")
                    out = clientSocket.recv2()
            #will quit and end the connection
            elif cmd == "QUIT":
                clientSocket.send2("closing connection")
                self.mySocket.close()
                break

            else:
                clientSocket.send2("500 Syntax error, command unrecognized.")
                out = clientSocket.recv2()

def StartServer(port):
    try:
        """ creating a new server socket and then binding the port and starting to listen"""
        severSocket = socket(AF_INET, SOCK_STREAM)
        severSocket.bind(('', port))
        severSocket.listen(1)
        logging.warning("Starting sever\n")
        while True:
            try:
                clientConnection, addr = severSocket.accept()
                ip = addr[0]
                port = addr[1]
                ftpsev = ftpServer(clientConnection,ip,port)
            except Exception as a:
                print("[Error]: " + str(a))
    except error as e:
        print("[ERROR]" + str(e))
    print("server shutting down")
    severSocket.close()

def cmdline():
    #getting comand line arg
    if len(sys.argv) > 3:
        print("Two many arguments please provide the name for your logfile and a port number")
        exit(0)
        #if none are provided it will give you defult
    elif len(sys.argv) < 2:
        print("you are going to be given a default port: 2121 and log file: sever.log because none were provided")
        log = "sever.log"
        port = 1234
    else:
        port = sys.argv[2]
        try:
            port = int(port)
            if port < 0 or port > 50000:
                raise ValueError("Please pick a port between 0 and 50000.")
        except Exception as a:
            print("Something went wrong.")
            exit(0)
        log = sys.argv[1]
    return log, port
def main():
#my logging functino
    log, port = cmdline()
    logging.basicConfig(filename=log ,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S.%f')
    severPort = port
    StartServer(severPort)
if __name__ == "__main__" :
    try:
        print("starting Server")
        main()
    except KeyboardInterrupt:
        print("Server shutting down")
        sys.exit(0)

