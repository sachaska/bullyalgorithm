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


class Lab1Client:
    def send(self, host, port, msg):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(pickle.dumps(msg))
                return pickle.loads(s.recv(1024))
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

    h = sys.argv[1]
    p = int(sys.argv[2])
    client = Lab1Client()
    result = client.send(h, p, MSG_BEGIN)

    if result is not None:
        for i in result:
            print('HELLO to', end=' ')
            print(i)
            try:
                h = i["host"]
                p = i["port"]
                result = client.send(h, p, MSG_HELLO)

                if result is not None:
                    print(repr(result))

            except:
                print('failed to find/use host and/or port in response.')
