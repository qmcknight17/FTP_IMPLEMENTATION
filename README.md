# FTP_IMPLEMENTATION

HW3 FTP server
Quentin McKnight

ReadMe:

Important files:
HW3_FTP_SERVER.py is my ftp server
sample.log: this is a sample log of my server running
Question and extra credit: this is where you can find the answers to the questions
Test_Client_QM.py: Is a better version of my Hw2 client its only purpose is to test my client if you want to use it
PAIN: a sample doc of my store cmd working

Important Notes:

During this process there are three things I did not implement:
    1. Port does not work, if you send the port command you will receive a 502 error
    2. EPRT same as port you will recive a 502 error
    3. It is not multi threaded it can only handle one client at a time

INSTRUCTIONS:
    1. please type in the following command in the terminal python HW3_FTP_SERVER.py (logfile) (Port)
    2. For For username and password you will find a USERLIST & a PASSWORDS at the top with all avalible I recomend using username: qtm23 and password: 1. Capitlization does not matter
    2. from there it should start running and you can connect a client to it and start testing it
    3. I am attatching my client to the hw because I tested it using that and all of my commands worked with it the Name is "Test_Client_QM" i also added the configuration if you are using pyecharm
    4.my client you just have to add a configuration to run it if you chose to test with it
    5. a Sample log is attached with all of the commands being run
    6. All error handling should be good if there is any issues please conntact me
    7. If there is any confustion with the code please let me know email: Qtm23@drexel.edu
    8. if you dont give it a port or log it will give you a defult

Please enjoy!

