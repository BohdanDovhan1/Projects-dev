import binascii
import sys, getopt

#Permutation tables + S-boxes
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)

IP = (2, 6, 3, 1, 4, 8, 5, 7)
IPi = (4, 1, 3, 5, 7, 2, 8, 6)

E = (4, 1, 2, 3, 2, 3, 4, 1)

S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
     ]

S1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
     ]

#Function for permutation   
def permutation(permTable, key):
    permutated_key = ""
    for i in permTable:
        permutated_key += key[i-1]

    return permutated_key

#Function for the first key generation  
def gen_1_key(left_key, right_key):
    left_key_rot = left_key[1:] + left_key[:1]
    right_key_rot = right_key[1:] + right_key[:1]
    key_rot = left_key_rot + right_key_rot
    return permutation(P8, key_rot)

#Function for the second key generation 
def gen_2_key(left_key, right_key):
    left_key_rot = left_key[3:] + left_key[:3]
    right_key_rot = right_key[3:] + right_key[:3]
    key_rot = left_key_rot + right_key_rot
    return permutation(P8, key_rot)

#Function for the expanding right part of the IP plaintext then XOR with key then using Sboxes and then permutation after Sboxes 
def F(right, subkey):
    expanded_plaintext = permutation(E, right)
    xor_plaintext = bin( int(expanded_plaintext, 2) ^ int(subkey, 2) )[2:].zfill(8)
    left_xor_plaintext = xor_plaintext[:4]
    right_xor_plaintext = xor_plaintext[4:]
    left_sbox_plaintext = Sbox(left_xor_plaintext, S0)
    right_sbox_plaintext = Sbox(right_xor_plaintext, S1)
    qq=permutation(P4, left_sbox_plaintext + right_sbox_plaintext)
    return permutation(P4, left_sbox_plaintext + right_sbox_plaintext)

#Function for the S-boxes operation
def Sbox(input, sbox):
    row = int(input[0] + input[3], 2)
    column = int(input[1] + input[2], 2)
    return bin(sbox[row][column])[2:].zfill(2)

#Function for the XOR of the left part IP plaintext with the result from the above F function and then adding copy of the right part of IP plaintext
def f(first_half, second_half, key):
     left = int(first_half, 2) ^ int(F(second_half, key), 2)
     return bin(left)[2:].zfill(4), second_half


#Keys generating
def keygen(key):
    p10key = permutation(P10, key)
    left = p10key[0:5]
    right = p10key[5:10]
    global first_key
    global second_key
    first_key = gen_1_key(left, right)
    second_key = gen_2_key(left, right)
    print ("k1=" + first_key)
    print ("k2=" + second_key)



#Encryption function
def encr(IV,key,name,sname):
    
    begin = 0
    end = 8
    #Opening file to read plaintext
    with open(name, 'rb') as t:
        hexdata = binascii.hexlify(t.read())  #Converting hex to binary
        binarydata = bin(int(hexdata, 16))[2:].zfill(len(hexdata)*4) #Converting hex to binary

    l = len(binarydata)

    list1 = [] # List that will be used to store encrypted results (8 bits for each round of following loop)
    printplaintext = [] #List was used just for convenience printing plaintext
    keygen(key)
    while (end <= l):    #Loop for encrypting plaintext
    
        b =  binarydata[begin:end]

        printplaintext.append(b) 

        plaintext = bin( int(b, 2) ^ int(IV, 2) )[2:].zfill(8) #XOR plaintext with IV for first time and with ciphertext during each next round
        permutated_plaintext = permutation(IP, plaintext) #Initial Permutation of plaintext

        first_half_plaintext = permutated_plaintext[0:4] 
        second_half_plaintext = permutated_plaintext[4:8]

        left, right = f(first_half_plaintext, second_half_plaintext, first_key)
        left, right = f(right, left, second_key) # switch left and right!
    
        output = permutation(IPi, left + right) #Final or IP–1 Permutation 

        IV = output #Assigning new IV (ciphertext becoming new IV for next round) according to CBC mode 

        begin = begin + 8
        end = end + 8;

    
        list1.append(output)  #Appending results to the list in order to store it, appending every round


        global str1
        str1 = ''.join(list1) #Joining encrypted result from the list to use it for converting it back  and write into file
        toprint = ' '.join(list1) #Joining encrypted result from the list to print it with blanks
        toprintplain = ' '.join(printplaintext) #Joining plaintext  from the list to print it with blanks
        
    print ("plaintext=" + toprintplain)
    print ("ciphertext=" + toprint)

    bin2hex = hex(int(str1, 2))[2:].zfill(len(str1)//4)  #Converting binary to hex
    hexdata1 = binascii.unhexlify(bin2hex) #Converting binary to hex

    #Writing cipher text into file 
    file = open(sname,"wb")  
    file.write(hexdata1)
    file.close()   


#Decryption function
def decr(IV,key,name,sname):

    begin = 0
    end = 8
     #Opening file to read ciphertext
    with open(sname, 'rb') as t:
        hexdata = binascii.hexlify(t.read()) #Converting hex to binary
        binarydata = bin(int(hexdata, 16))[2:].zfill(len(hexdata)*4) #Converting hex to binary

    l = len(binarydata)

    list2 = []
    printciphertext = []
    keygen(key)
    while (end <= l):   #Loop for decrypting ciphertext
        q =  binarydata[begin:end]
        printciphertext.append(q)

        permutated_plaintext = permutation(IP, q) #Initial Permutation

        first_half_plaintext = permutated_plaintext[0:4]
        second_half_plaintext = permutated_plaintext[4:8]

        left, right = f(first_half_plaintext, second_half_plaintext, second_key)
        left, right = f(right, left, first_key ) 

        plain = bin( int(permutation(IPi, left + right), 2) ^ int(IV, 2) )[2:].zfill(8) #XOR ciphertext with IV for first time and then with plaintext during each next round


        IV = q  #Assigning new IV (decrypted result becoming new IV for next round) according to CBC mode

        begin = begin + 8
        end = end + 8;

        list2.append(plain) #Appending results to the list in order to store it, appending every round


        global str2
        str2 = ''.join(list2)  #Joining decrypted result from the list to use it for converting it back  and write into file
        toprint2 = ' '.join(list2) #Joining decrypted result from the list to print it with blanks
        toprintcipher = ' '.join(printciphertext) #Joining cipher text from the list to print it with blanks

    print ("ciphertext=" + toprintcipher)    
    print ("plaintext=" + toprint2)
    
     #Writing result into file    
    bin2hex = hex(int(str2, 2))[2:].zfill(len(str2)//4) #Converting binary to hex
    hexdata1 = binascii.unhexlify(bin2hex) #Converting binary to hex
    #Writing cipher text into file 
    file = open(name,"wb")
    file.write(hexdata1)
    file.close()

#Main function, using for the input command 
def main(argv):
    
   key = ''
   IV = ''
   mode = ''
   file2read = ''
   file2write = ''
   
   opts, args = getopt.getopt(argv,"hm:k:i:p:c:")

   for opt, arg in opts:
       
      if  opt in ("-m", "--mode"):
          if arg == 'encrypt':
                global r
                r=1
          if arg == 'decrypt':
                r=0
         
      elif opt in ("-k", "--key"):
         key = arg
         
      elif opt in ("-i", "--IV"):
         IV = arg

      elif opt in ("-p", "--file2read"):
         name = arg
         
      elif opt in ("-c", "--file2write"):
         sname = arg
         if r==1:
             encr(IV,key,name,sname)
         if r==0:
             decr(IV,key,name,sname)

if __name__ == "__main__":
   main(sys.argv[1:])
    












