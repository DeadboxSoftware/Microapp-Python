import hashlib
# import pyaes
from base64 import b64encode, b64decode
import os
import bcrypt

def hash_password(password):
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))