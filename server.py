# ! /usr/bin/python3.8
import socket
import threading
import time
from _thread import start_new_thread, exit_thread
import pickle
import datetime
from os import system

import subprocess
import traceback


class Colors:
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    WARNING = "\033[93m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"


class Server:
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.client_threads = []
        self.clients = []

    def listen(self):
        try:
            self.socket.bind((self.address, self.port))
            self.socket.listen()
            _ = system("clear")
            print(
                f"{Colors.BOLD}{Colors.OKBLUE}::**:E:**:l:**:V:**:i:**:s:**:T:**:o:**:O:**:l:**:S:**::"
            )
            print(
                f"{Colors.BOLD}{Colors.OKGREEN}[TUNNEL V1.0.4 for (FES) STARTED AT: {self.address}:{self.port}]\nUser Control+C to stop the server\n\n"
            )
        except:
            print("ERROR: could not start the server at the specified port")

        while True:
            try:
                conn, addr = self.socket.accept()
                print(
                    f"{Colors.WARNING}[+]{datetime.datetime.today()}--connected to:{addr}"
                )
                newthread = start_new_thread(client_thread, (conn, addr, self))
                self.client_threads.append(newthread)

            except socket.error:
                SystemExit()
            except KeyboardInterrupt:
                print("[!]Server Closed")
                self.socket.close()
                break


def client_thread(conn, addr, server):
    file_to_execute = conn.recv(4096)
    file_to_execute = file_to_execute.decode()
    print("[*]Attempting to run:", file_to_execute)
    try:
        if ".py" in file_to_execute:
            a = subprocess.run(
                ["python3.8", f"{file_to_execute}"], capture_output=True)
        elif ".cpp" in file_to_execute:
            a = subprocess.run(
                ["g++", f"{file_to_execute}"], capture_output=True)
            if len(a.stderr.decode("utf-8")) < 1:
                a = subprocess.run(
                    ["./a.out"], capture_output=True)
    except Exception as e:
        print("[!]Sys fail", e)
        error = f'Failed to execute {file_to_execute}'
        conn.send(error.encode())
        return
    try:
        if len(a.stdout.decode("utf-8")) == 0 and len(a.stderr.decode("utf-8")) == 0:
            conn.send(b"Program STD_OUT is empty")
        elif len(a.stdout.decode("utf-8")) > 0 and len(a.stderr.decode("utf-8")) < 1:
            conn.send(a.stdout)
        elif len(a.stderr.decode("utf-8")) > 0:
            g = a.stderr.decode("utf-8")
            g = g.replace(file_to_execute, "******/****")
            conn.send(g.encode())
    except:
        conn.send(b"Could not execute the file")


port = input("enter port: ")
myserver = Server("localhost", int(port))
myserver.listen()
