# DNS Attack Simulation and Detection

## Introduction

This repository contains code for simulating a DNS tunneling attack and detecting it using a decision tree model trained on common DNS tunneling attacks. The simulation involves running a client and server, where the client sends DNS queries to a normal server, and the server detects and blocks malicious DNS tunneling attempts.

## Simulation

### Running the Client

To run the client, execute the following command in your terminal:

`python Client.py <portNumber> <filePath>`


Replace `<portNumber>` with the port number mentioned in Server.py (e.g., 53) and `<filePath>` with the path to the file containing the data to be sent as DNS queries.

### Running the Server

To run the server, execute the following command in your terminal:

`python Server.py`


The contents of the `dnstunnel.txt` file will be split into DNS queries and sent to the normal server. These packets can be captured or sniffed using Wireshark, demonstrating the simulation of the attack.

## Detection

### Running the Detection Server

To run the server with the detection capability, execute the following command:

`python ServerWithSniffer.py`


### Usage

When the client attempts to send a message as chunked DNS queries, the server can identify it and prevent it from passing through. Instead, it returns the request to the client without forwarding it.

To use the client for detection purposes, run it with the following command:

`python Client.py <portNumber> <filePath>`



Replace `<portNumber>` with the port number 58, as this is the port number mentioned ServerWithSniffer.py

## Conclusion

This repository provides a basic simulation of a DNS tunneling attack and demonstrates the detection of such attacks using a decision tree model. Researchers and practitioners interested in understanding and mitigating DNS tunneling attacks can use this code as a starting point for further exploration and development.

