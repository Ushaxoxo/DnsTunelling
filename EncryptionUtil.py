import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class EncryptionUtil:
    AES_ENCRYPTION_KEY = b"abcdefghijklmnop"
    AES_INIT_VECTOR = b"1234567890abcdef"

    @staticmethod
    def encrypt(content):
        try:
            cipher = AES.new(EncryptionUtil.AES_ENCRYPTION_KEY, AES.MODE_CBC, EncryptionUtil.AES_INIT_VECTOR)
            encrypted = cipher.encrypt(pad(content.encode("utf-8"), AES.block_size))
            return base64.b64encode(encrypted).decode("utf-8")
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def decrypt(encrypted, key, iv):
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(base64.b64decode(encrypted))
            return decrypted
        except Exception as e:
            print(e)
            return None
        
if __name__ == "__main__":
    # Encrypting a message
    provided_ciphertext = "w1hHbihQQPK6J/oA5kPfC8zpq2Z9T0nnJC8CcfTuQ+lzDg2T5dO+5xV3iFQ7SVQsWtM+NJO1QcYl0B0Rt9GzpHoE40R2+JfgPgW8XTYovfQ="
    decrypted_text = EncryptionUtil.decrypt(provided_ciphertext, EncryptionUtil.AES_ENCRYPTION_KEY, EncryptionUtil.AES_INIT_VECTOR)
    if decrypted_text:
        print(f"Decrypted text: {decrypted_text.decode('utf-8')}")
    else:
        print("Decryption failed.")

