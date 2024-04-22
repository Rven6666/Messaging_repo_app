import bcrypt
import random
import sympy
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# #Generate users private key - 2048 bits - diffie Helman
# def privateKey(bits):
#     while True:
#         privatePrime = random.getrandbits(bits)
#         if sympy.isprime(privatePrime):
#             return bin(privatePrime)
        
#both on 2048 bits - diffie helam
def publicKeys(bits):
    while True:
        pubPrime = random.getrandbits(bits)
        if sympy.isprime(pubPrime):
            gKey = random.randint(2, pubPrime - 1)
            return pubPrime,gKey
