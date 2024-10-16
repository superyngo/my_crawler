import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF1

def decrypt_cryptojs_aes(ciphertext_b64, password):
    # Decode the base64 ciphertext
    ciphertext = base64.b64decode(ciphertext_b64)
    
    # Extract salt from the first 16 bytes (8 bytes "Salted__" + 8 bytes salt)
    assert ciphertext[:8] == b"Salted__"
    salt = ciphertext[8:16]
    
    # Derive key and IV using the salt and password (MD5 hash function)
    key_iv = PBKDF1(password.encode(), salt, dkLen=32, count=1, hashAlgo=hashlib.md5)
    key, iv = key_iv[:16], key_iv[16:32]
    
    # Decrypt the rest of the data
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Ensure AES is correctly imported from Crypto.Cipher
    plaintext = cipher.decrypt(ciphertext[16:])
    
    # Remove potential PKCS7 padding
    padding_len = plaintext[-1]
    plaintext = plaintext[:-padding_len]
    
    return plaintext.decode()

# Example usage
ciphertext_b64 = "U2FsdGVkX198/GNl+BNWQnlWRywknE1Ske7+e310WTcIC5uZRcGTXqHf5lPa4Luvd+DTMs2L9RRFlWUqv2FWyCfUegJxsEC3cVhdxzk67N0XSDzz8ywLeA/ydk47IalJnmVUa7jhzAtLZxL1RxIc+kqiJUvbQE+e3NtSc1NCU/hlrN4n1CIb7pRg3LUyjcSJUP0SL9sDgqNZ5YWrA/Ne4AXRF72BfGpMueodNQgzCjkOyhSSCzUuyk+vkrjmUEyod/hMWC/Se7NZyh9f/89nqVRL2/eawSbUS1LTYbaG5KE="
password = '96YNV-9X4RP-2YYKB-RMQH4-6Q72D'

decrypted_text = decrypt_cryptojs_aes(ciphertext_b64, password)
print(decrypted_text)
