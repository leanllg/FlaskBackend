from Crypto.Hash import SHA512
import bcrypt
import base64

def get_salt_pwd(password):
    h = SHA512.new()
    h.update(password.encode('utf-8'))
    pwd = bcrypt.hashpw(
        base64.b64encode(h.digest()),
        bcrypt.gensalt()
    )
    return pwd

def hash_pwd(password):
    h = SHA512.new()
    h.update(password.encode('utf-8'))
    return base64.b64encode(h.digest())