#! /usr/bin/env python3
import string

def caesarEncrypt(message,key):
    message, letters, numbers = message.lower() , string.ascii_letters[:26] , range(0,26)
    dictionary = {letters[i]:numbers[i] for i in range(26)}
    conversion = [ list(dictionary.keys())[list(dictionary.values()).index((dictionary[alpha] + key)% 26)] if alpha in letters else alpha for alpha in list(message) ]
    return ''.join(conversion)

# message = input("Enter the message : ")
# key = int(input("Enter the key here: "))
# print('Translated Message:', caesarEncrypt(message, key))


