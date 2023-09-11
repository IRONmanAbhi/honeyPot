import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey.from_private_key_file(
    "/home/ironmanabhi/Documents/venv/hack_tests/cyber_project/Proj5_HoneyPot/key"
)


class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username: str, password: str) -> int:
        if "ironman" == username and "12345" == password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


if __name__ == "__main__":
    server = "172.16.222.86"
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+] Listening for connection ...")
        client, addr = sock.accept()
    except Exception as e:
        print("[-] Listen failed: " + str(e))
        sys.exit(1)
    else:
        print("[+] Got a connection!", addr)
        Session = paramiko.Transport(client)
        Session.add_server_key(HOSTKEY)
        serv = Server()
        Session.start_server(server=serv)
        chan = Session.accept(20)
        print(chan)
        if chan is None:
            print("*** No channel.")
            sys.exit(1)
        print("[+] Authenticated!")
        chan.send("Welcome to ssh\n".encode())
        chan.send("some more string\n".encode())
        flag = 0
        while True:
            pass
            # chan.send("more strings".encode())
            # command = chan.recv(1024).decode()
