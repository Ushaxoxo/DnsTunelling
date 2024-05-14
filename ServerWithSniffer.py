import socket
import subprocess
import pickle
import math

def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def calculate_entropy(text):
    if not text: 
        return 0 
    entropy = 0
    for x in range(256): 
        p_x = float(text.count(chr(x)))/len(text) 
        if p_x > 0: 
            entropy += - p_x*math.log(p_x, 2) 
    return entropy


def main():
    model = load_model('DataTunelling_DecisionTree.pkl')

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('localhost', 58))

        while True:  # Continuously listen for queries
            receiveData = bytearray(1024)
            receivePacket, clientAddr = serverSocket.recvfrom_into(receiveData)
            receivedData = "WWW.GOOGLE.COM"
            print("Received from client:", receivedData)
            
            # Check for termination signal
            if receivedData == "-1":
                print("Termination signal received. Closing server.")
                break
            
            # Calculate entropy
            data_entropy = calculate_entropy(receivedData)
            print("Entropy:", data_entropy)

            # Use the model to predict
            prediction = model.predict([[data_entropy]])  # Assuming receivedData is the query
            print("Model Prediction:", prediction)
            print(prediction[0])
            
            if prediction[0] == 1:  
 
                print("Prediction is 1. Rejecting DNS query.")
                serverSocket.sendto(b"DNS query rejected", clientAddr)
            else:
                print("Prediction is . Moving forward with nslookup")


                serverOutput = executeNSLookup(receivedData)
                clientPort = clientAddr[1]
                print(serverOutput)
                sendData = serverOutput.encode()
                sendPacket = (sendData, clientAddr)
                serverSocket.sendto(*sendPacket)
        
    except OSError as e:
        print(e)
    finally:
        serverSocket.close()

def executeNSLookup(dnsQuery):
    command = "nslookup -type=A " + dnsQuery
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode()

if __name__ == "__main__":
    main()
