import socket
import subprocess

def main():
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('localhost', 53))

        while True:  # Continuously listen for queries
            receiveData = bytearray(1024)
            receivePacket, clientAddr = serverSocket.recvfrom_into(receiveData)
            receivedData = receiveData.decode().rstrip('\x00')
            print("Received from client:", receivedData)
            
            # Check for termination signal
            if receivedData == "-1":
                print("Termination signal received. Closing server.")
                break
            
            serverOutput = executeNSLookup(receivedData)
            clientPort = clientAddr[1]
            print(serverOutput)
            sendData = serverOutput.encode()
            sendPacket = (sendData, clientAddr)
            serverSocket.sendto(*sendPacket)
        
        serverSocket.close()
    except OSError as e:
        print(e)

def executeNSLookup(dnsQuery):
    command = "nslookup -type=A " + dnsQuery
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode()

if __name__ == "__main__":
    main()
