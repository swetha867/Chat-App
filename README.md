# CSC845 project Mini Chatt

Members: Zhuojun He,  Swetha Govindu

# The Goal
To create a chatting app is the goal of our project. We will use python to create client and server programs for text messaging and the function of Internet chatting.

This app will contain a server and a client program. The server side holds all the account, password and the other necessary data information. It also handles different requests from the client side. The client side is for different users to connect to the server. This app will have two functions: text messaging between two clients asynchronously and instant chatting between two clients synchronously.   

# Environment
python version 3.8
python libraries used: Socket, SMTPLIB, GetPass etc.

# Configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Acct information: 
    "Swetha", "password": "123"
    "Zhuojun", "password": "123"
    "Alice", "password": "123"
    "Bob","password": "123"
    
# Functions of the app:
    ----------------------------------
    0. Connect to the server 
    1. Get the user list 
    2. Send a message 
    3. Get my messages 
    4. Initiate a chat with my friend 
    5. Chat with my friend
    6. Send an email through gmail
    7. Disconnect
    ----------------------------------
