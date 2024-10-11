"""
CPSC 5520, Seattle University
This is free and unencumbered software released into the public domain.
:Authors: Ai Sun
:Version: 1.0
"""
import pickle
import socket
import sys

MSG_BEGIN = 'BEGIN'  # Begin message which send to GCD
MSG_HELLO = 'HELLO'  # Hello message for members


def encode(msg):
    """
    Encode (pickle) a message
    :param msg: The message to pickle
    :return: The pickled message
    """
    return pickle.dumps(msg)


def decode(msg):
    """
    Decode (unpickle) a message
    :param msg: The message to unpickle
    :return: The unpickled message
    """
    return pickle.loads(msg)


def client(h, p, msg):
    """
    Client function that connects to the server at specified host and port,
    send a message and wait for response.
    :param h: The host to connect to
    :param p: The port to connect to
    :param msg: The message to send
    :return: The response
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((h, p))
            s.sendall(encode(msg))
            data = s.recv(1024)
        return decode(data)
    except ConnectionRefusedError as e:
        print('failed to connect:', end=" ")
        print(e)
    except Exception as e:
        print('error occurred:', end=" ")
        print(e)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python lab1.py HOST PORT")
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    result = client(host, port, MSG_BEGIN)

    if result is not None:
        for i in result:
            print('HELLO to', end=' ')
            print(i)
            try:
                host = i["host"]
                port = i["port"]
                result = client(host, port, MSG_HELLO)

                if result is not None:
                    print(repr(result))

            except:
                print('failed to find/use host and/or port in response.')
