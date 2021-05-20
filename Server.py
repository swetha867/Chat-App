#!/usr/bin/env python3

import sys
import socket
import time
import threading


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


database = {
    "Swetha": {
        "password": "123",
        "messages":[

        ]
    },
    "Zhuojun": {
        "password": "123",
        "messages": [

        ]
    }
    ,
    "Alice": {
        "password": "123",
        "messages": [

        ]
    },
    "Bob": {
        "password": "123",
        "messages": [

        ]
    }
}


def handle_authentication(conn):
    conn.sendall(b'Welcome! Please log in.')

    # Using this sleep to prevent bundling
    # Welcome banner and username prompt.
    time.sleep(1)

    conn.sendall(b'Username:')
    while True:
        username = conn.recv(1024)
        if username is not None:
            username = username.decode()
            break
        else:
            print(username.decode())

    time.sleep(1)

    conn.sendall(b'Password:')
    while True:
        password = conn.recv(1024)
        if password is not None:
            password = password.decode()
            break
        else:
            print(password.decode())
    if database.get(username, {}).get("password", "") == password:
        print("Login Successful for : "+username)
        conn.sendall(b'Login Success')
    else:
        print("Login Failure for : "+username)
        conn.sendall(b'Login Failure')

    time.sleep(1)

def handle_user_list(conn):
    user_list = """
    User list:
    --------------------
    1. Swetha
    2. Zhoujun
    3. Alice
    4. Bob
    --------------------
    """
    conn.sendall(user_list.encode())

def wait_for_message_from_client(conn):
    while True:
        message = conn.recv(1024)
        if message is not None:
            return message.decode()

def handle_user_inbox(conn, user_name):
    messages = database.get(user_name,{}).get("messages",[])
    if len(messages) == 0:
        messages_string = """ 
        Inbox:
        -------------------
        No messages found.
        -------------------
        """
    else:
        messages_formatted = ""
        for message_idx in range(len(messages)):
            messages_formatted += "        " + str(message_idx) + ": " + messages[message_idx] + "\n"
        header = """ 
        Inbox:
        ------------------- 
"""
        footer = """-------------------
        """
        messages_string = header + messages_formatted + footer
    conn.sendall(messages_string.encode())


def handle_client(conn, addr):
    print('Socket connection established successfully  :', addr)
    try:
        handle_authentication(conn)
        with conn:
            while True:
                option = conn.recv(1024)
                if option is None:
                    continue
                else:
                    option = option.decode()
                    if option == '1':
                        handle_user_list(conn)
                    elif option == '2':
                        user_name = wait_for_message_from_client(conn)
                        time.sleep(1)
                        message = wait_for_message_from_client(conn)
                        global database
                        database.get(user_name,{}).get("messages",[]).append(message)
                    elif option == '3':
                        user_name = wait_for_message_from_client(conn)
                        handle_user_inbox(conn, user_name)
                    elif option == '7':
                        print("Closing connection..")
                        break
    except Exception:
        print("Unexpected error:", sys.exc_info())
        conn.close()
       # s.close()
   # print("Connection closed from :", addr)



def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[LISTENING] Server is listening on {HOST}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[Active Connections] {threading.activeCount() -1}")



if __name__ == "__main__":
    main()
