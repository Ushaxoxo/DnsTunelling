from Crypto.Util.Padding import pad

from EncryptionUtil import EncryptionUtil
import socket
import sys
import os

class Client:
    serverIP = "127.0.0.1"

    @staticmethod
    def main(args):
        if len(args) != 3:
            print("Usage: python Client.py <portNumber> <filePath>")
            return
        portNumber = int(args[1])
        filePath = args[2]
        file = open(filePath, 'r')
        print("Reading file: " + filePath)

        content = file.read()
        print("File content:\n", content)  # Display file content

        try:
            responses = Client.sendFileViaDNS(content, Client.serverIP, portNumber)
            for response in responses:
                print("Received response:", response)
        except Exception as e:
            print(e)

    @staticmethod
    def sendFileViaDNS(content, serverIP, portNumber):
        encryptedContent = Client.encryptContent(content)
        print("Encrypted content:\n", encryptedContent)  # Display encrypted content

        chunkSize = 50
        chunks = (len(encryptedContent) + chunkSize - 1) // chunkSize
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        responses = []
        for i in range(chunks):
            
            chunk = encryptedContent[i * chunkSize: min((i + 1) * chunkSize, len(encryptedContent))]
            if i == chunks - 1:  # Ensure the last chunk ends with '='
                dnsQuery = chunk +"="+ ".part" + str(i) + ".example.com"
            else:
                dnsQuery = chunk + ".part" + str(i) + ".example.com"
            
            serverAddr = socket.gethostbyname(serverIP)
            sendData = dnsQuery.encode()
            sendPacket = (sendData, (serverAddr, portNumber))
            socketObj.sendto(*sendPacket)
            print("Sent DNS query: " + dnsQuery)

            # Receive response from the server
            response, _ = socketObj.recvfrom(1024)
            responses.append(response.decode())

        # Signal server to terminate after all queries are sent
        termination_signal = "-1"
        sendData = termination_signal.encode()
        sendPacket = (sendData, (serverAddr, portNumber))
        socketObj.sendto(*sendPacket)

        socketObj.close()
        return responses

    @staticmethod
    def encryptContent(content):
        padded_content = pad(content.encode("utf-8"), 16)  # Pad to a multiple of 16 bytes (AES block size)
        return EncryptionUtil.encrypt(content)

if __name__ == "__main__":
    Client.main(sys.argv)
