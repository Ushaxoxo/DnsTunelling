from Crypto.Util.Padding import unpad, pad
from Crypto.Cipher import AES
from scapy.all import sniff, DNS, UDP
from EncryptionUtil import EncryptionUtil

# Key and IV used for encryption
AES_ENCRYPTION_KEY = b"abcdefghijklmnop"
AES_INIT_VECTOR = b"1234567890abcdef"

# Initialize a variable to store concatenated encrypted content
concatenated_encrypted_content = {}

def decrypt_content(encrypted_content):
    try:
        decrypted_data = EncryptionUtil.decrypt(encrypted_content, AES_ENCRYPTION_KEY, AES_INIT_VECTOR)
        if decrypted_data:
            unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7').decode("utf-8")
            return unpadded_data
        else:
            print("Decryption failed: decrypted_data is None")
            return None
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def packet_handler(packet):
    if packet.haslayer(DNS) and packet.haslayer(UDP):
        if packet[UDP].dport == 53 and packet[DNS].qr == 0:  # Check for DNS query packets to the server
            query = packet[DNS].qd.qname.decode()
            print(f"Original DNS query: {query}")  # Display original DNS query before further operations

            query_parts = query.split(".")
            if len(query_parts) >= 5 and query_parts[-3] == "example" and query_parts[-4].startswith("part"):
                part_number = query_parts[-4][4:]
                encrypted_data = query_parts[0]  # Get the encrypted content

                # Store the encrypted data for each part number
                concatenated_encrypted_content[int(part_number)] = encrypted_data

                # Concatenate encrypted content based on part number
                concatenated_encrypted_text = "".join([concatenated_encrypted_content[key] for key in sorted(concatenated_encrypted_content.keys())])
                print(f"Concatenated encrypted content: {concatenated_encrypted_text}")
                print(f"Concatenated encrypted length: {concatenated_encrypted_text[-1]}")

                # Check if the last character of the last element is '=' and call decrypt_content
                if concatenated_encrypted_text[-1] == '=':
                    print("in")
                    concatenated_encrypted_text = concatenated_encrypted_text[:-1]
                    decrypted_data = decrypt_content(concatenated_encrypted_text)
                    if decrypted_data:
                        print(f"Decrypted content: {decrypted_data}")

# Start capturing DNS packets
print("Capturing DNS packets...")
sniff(filter="udp port 53 ", prn=packet_handler, store=0, iface="en0")
