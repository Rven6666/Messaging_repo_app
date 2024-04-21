import bcrypt
import random
import sympy
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


#Generate users private key
def privateKey(bits):
    while True:
        pubPrime = random.getrandbits(bits)
        if sympy.isprime(pubPrime):
            return pubPrime