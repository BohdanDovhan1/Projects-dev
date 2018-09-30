from socket import *
import os


#Getting your IP address
def getIP():
    
    IP = gethostbyname(getfqdn())
    print ("Your IP address", IP)
    
    # IP1 will be used for sending PORT commands
    global IP1
    IP1 = str.replace(IP,'.',',')
getIP()


#Checking if the "myftp" command was used
while (True):
    welcome = input(">" ' ')
    welcome_split = welcome.split(' ')
    myftp_command = (welcome_split[0].split()[-1])
    if  myftp_command == 'myftp':
        break
    else:
        print ("Wrong command. Please use 'myftp server-name', where server-name is the name or IP")
    
#Separeting serverName from "myftp server-name" input     
serverName = (welcome_split[1].split()[0])
    



#Creating a clientSocket
serverPort = 21
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
modifiedSentence = clientSocket.recv(1024)
print (modifiedSentence)

#Calculating the port number which will be used in serverSocket, calculating based on the clientSocket number +1
portnumber=clientSocket.getsockname()[1]
portnumber = portnumber+1
first = (int)(portnumber / 256)
second = (int)(portnumber % 256)


#Loop for Login
while (True):
    user = input("User> ")
    #Sending User
    user_command = str.encode("USER " + str(user)+ "\r\n")
    clientSocket.send(user_command)
    modifiedSentence = clientSocket.recv(1024)
    print (modifiedSentence)
     
    passw = input("> ")
    #Sending Password
    passw_command = str.encode("PASS " + str(passw)+ "\r\n")
    clientSocket.send(passw_command)
    modifiedSentence = clientSocket.recv(1024)
    #Error notification if wrong username or password
    if modifiedSentence == b'530 Login incorrect.\r\n':
        print ("Login or Password incorrect")
    else:
        print (modifiedSentence)
        break
    
def ls():
    # #Server socket creating, binding and establishing "listen" mode
    s = socket(AF_INET,SOCK_STREAM)                    
    s.bind(('', portnumber))        
    s.listen(1)

    #Port command sending
    port_command = str.encode("PORT " + str(IP1) + "," + str(first)+ "," +str(second)+ "\r\n")
    clientSocket.send(port_command)
    modifiedSentence = clientSocket.recv(1024)
    print (modifiedSentence)

    #Sending the command for the list of files 
    clientSocket.send(b'LIST\r\n')
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)

    s, addr = s.accept()
    data = s.recv(10000)
    lines = data.splitlines()
    for line in lines:
            print (line)
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)
    
    #Calculating number of received bytes
    size = len(data)
    print ("Received" , size, "bytes")
    s.close()


def put(split):
    #Server socket creating, binding and establishing "listen" mode
    s = socket(AF_INET,SOCK_STREAM)                    
    s.bind(('', portnumber))        
    s.listen(1)

    #Separeting the file name from the user input 
    Name_of_file = (split[1].split()[0])
    
    #Port command sending
    port_command = str.encode("PORT " + str(IP1) + "," + str(first)+ "," +str(second)+ "\r\n")
    clientSocket.send(port_command)
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)

    #Sending the command for file uploading
    put_command = str.encode("STOR " + str(Name_of_file) + "\r\n")
    clientSocket.send(put_command)
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)
    
    f = open(str(Name_of_file),'rb')
    s, addr = s.accept()
    l = f.read(2048)
    print ('Sending...')
    
    #Loop for sending(until the entire file will be sent)
    while (l):
       s.send(l)
       l = f.read(2048)
    else:
        print ("File sent successfully") 
    s.close()

def get(split):
    #Server socket creating, binding and establishing "listen" mode
    s = socket(AF_INET,SOCK_STREAM)                    
    s.bind(('', portnumber))        
    s.listen(1)
    
    #Port command sending
    port_command = str.encode("PORT " + str(IP1) + "," + str(first)+ "," +str(second)+ "\r\n")

    clientSocket.send(port_command)
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)
    
    #Separeting the file name from the user input
    Name_of_file = (split[1].split()[0])

    #Sending the command for file downloading
    retr_command = str.encode("RETR " + str(Name_of_file)+ "\r\n")
    clientSocket.send(retr_command)
    modifiedSentencee = clientSocket.recv(2048)

    #Notification if the file does not exist
    if modifiedSentencee == b'550 Failed to open file.\r\n':
        print ("File does not exist")
        return
    print (modifiedSentencee)

    s, addr = s.accept()

    #Loop for file receiving (until the entire file will be received)
    with open(os.path.join('', str(Name_of_file)), 'wb') as file_to_write:
        while True:
            data = s.recv(1024)
            if not data:
                break
            file_to_write.write(data)
        file_to_write.close()
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)
    
    #Notification about received bytes
    modifiedSentence1 = str(modifiedSentencee)
    splitresponse = modifiedSentence1.split()
    sizefile = (splitresponse[8].split()[0])
    print ("File received successfully" , sizefile, ") bytes")
    s.close()
    

def delete(split):
    #Separeting the file name from the user input
    Name_of_file = (split[1].split()[0])
    
    #Sending the command for file deleting
    dele_command = str.encode("DELE " + str(Name_of_file) + "\r\n")
    clientSocket.send(dele_command)
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)
    

def quitf():
    #Command for file deleting
    clientSocket.send(b'QUIT\r\n')
    modifiedSentence = clientSocket.recv(2048)
    print (modifiedSentence)

#Main loop for commands
while(True):
    command = input("myftp> ")
    
    #Separeting the command from the user input
    split = command.split(' ')
    Name = (split[0].split()[-1])
    
    if Name == 'ls':
        ls()
    elif Name == 'put':
        put(split)
    elif Name == 'get':
        get(split)
    elif Name == 'delete':
        delete(split)
    elif Name == 'quit':
        quitf()
        break
    else:
        print ("Wrong command")
