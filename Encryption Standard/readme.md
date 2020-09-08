**Programming Language:** Python 3.6.2

A program to encrypt and decrypt binary files using **S-DES (Simplified DES)** in the Cipher Block Chaining mode. The program takes the input of an initial key and an initial vector, reads the plaintext or ciphertext from a file, conducts the encryption or decryption, and writes the resulting ciphertext or plaintext into a second file.

**Instruction:** the command line to run code: 

mycipher.py -m mode -k initial_key -i initial_vector -p plaintext_file -c ciphertext_file
mode: can be encrypt or decrypt
initial_key: 10-bit initial key
initial_vector: 8-bit initial vector
plaintext_file: a binary (not text) file to store the plaintext
ciphertext_file: a binary (not text) file to store the ciphertext

**For example:** python mycipher.py -m encrypt -k 0111111101 -i 10101010 -p f1 -c f3
                 python mycipher.py -m decrypt -k 0111111101 -i 10101010 -p f2 -c f3
            
The file f2  will be the same after decryption as the plaintext file f1. 
            
            
          The program able to encrypt and decrypt other files and formats also: jpeg, png, pdf, word, mp3, etc.
