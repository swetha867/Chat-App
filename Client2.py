#!/usr/bin/env python3

import socket
import time
from getpass import getpass
import sys
import smtplib, ssl

def printCommands():
    print("""
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
    """)

def server_connect():
    ip_addr = input("Please enter the IP address: ")
    port = int(input("Please enter the IP port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    print("Connecting...")
    try:
        sock.connect((ip_addr, port))
        print("Connected!")
    except Exception as e:
        print("Error connection to the server", e)
    
    welcome_banner = sock.recv(1024)
    print(welcome_banner.decode())
    
    user_auth_prompt = sock.recv(1024)
    username = input(user_auth_prompt.decode())
    sock.send(str.encode(username))

    password_prompt = sock.recv(1024)
    password = getpass(password_prompt.decode())

    sock.send(str.encode(password))

    login_result = sock.recv(1024)

    if login_result == b'Login Success':
        return username, sock
    else:
        print("Login was unsuccesful, please reconnect and try again.")
        sock.close()

def wait_for_message_from_client(conn):
    while True:
        message = conn.recv(1024)
        if message is not None:
            return message.decode()

def connect_to_friend_chat_server():
    username = input("Please enter your name: ")
    ip_addr = input("Please enter your friend's IP address: ")
    port = int(input("Please enter the port number: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to your friend...")
    try:
        sock.connect((ip_addr, port))
        print("Connected!")
    except Exception as e:
        print("blah", e)
    print('<Type "Bye" to stop the conversation>')
    sock.send(username.encode())
    other_user = wait_for_message_from_client(sock)
    while True:
            my_message = input(username+": ")
            sock.send(my_message.encode())
            if my_message == "Bye":
                print("Ending chat")
                sock.close()
                break
            message = wait_for_message_from_client(sock)
            if message == "Bye":
                print("--------------------------------")
                print(other_user + " has ended the chat")
                sock.close()
                break
            else:
                print(other_user+ ": "+ message)

def create_chat_server():
    username = input("Please enter your name: ")
    port = int(input("Please enter the port number you want to listen on: "))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", port))
        s.listen()
        conn, addr = s.accept()
        other_user = wait_for_message_from_client(conn)
        conn.send(username.encode())
        print(other_user + " is connected.")
        print('<Type "Bye" to stop the conversation>')
        while True:
            message = wait_for_message_from_client(conn)
            if message == "Bye":
                print("--------------------------------")
                print(other_user + " has ended the chat")
                break
            else:
                print(other_user+ ": "+ message)
            my_message = input(username+": ")
            conn.send(my_message.encode())
            if my_message == "Bye":
                print("Ending chat")
                conn.close()
                break
def gmail_server_connect():
    port = 587  # For SSL
    sender_email = input("Please enter your gmail id ")
    gmailPassword = getpass("Type your gmail password : ")
    smtp_server = "smtp.gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)

        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, gmailPassword)
        print("-------Login Successful-------")
        receiver_email=input("Please enter receiver email")
        subject=input("please enter subject of the email:")
        message=input("please enter message")
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
   
def main():
    username = None
    sock = None
    while True:
        time.sleep(2.5)
        printCommands()
        option = input("Please enter your option: ")
        if option == '0':
            username, sock = server_connect()
            if sock is not None:
                print("Login successful!")
        elif option == '1':
            if sock is None:
                print("Please connect to server first!")
            else:
                # we are sending the option selected on client to server to invoke the correct server side function.
                sock.send(b'1')
                user_list = sock.recv(1024)
                print(user_list.decode())
        elif option == '2':
            if sock is None:
                print("Please connect to server first!")
            else:
                sock.send(b'2')
                recipient = input("Please enter the recipient's name: ")
                message = input("Please enter the message: ")
                sock.send(recipient.encode())
                time.sleep(1)
                sock.send(message.encode())
                print("message sent succesfully!")
        elif option == '3':
            if sock is None:
                print("Please connect to server first!")
            else:
                sock.send(b'3')
                time.sleep(1)
                sock.send(username.encode())
                messages = sock.recv(1024)
                print(messages.decode())
        elif option == '4':
            create_chat_server()
        elif option == '5':
            connect_to_friend_chat_server()
        elif option == '6':
            gmail_server_connect()
        elif option == '7':
            if sock is None:
                print("Please connect to server first!")
            else:
                sock.send(b'7')
        else:
            print("You selected the wrong option.")
            continue

if __name__ == "__main__":
    main()
