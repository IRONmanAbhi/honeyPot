import os
import paramiko
import socket
import sys
import threading

HOSTKEY = paramiko.RSAKey.from_private_key_file(
    "/home/ironmanabhi/Documents/venv/hack_tests/cyber_project/Proj5_HoneyPot/key"
)

file_system = {
    "/": {
        "bin": {
            "files": ["ls", "cp", "rm", "mv"],
            "directories": [],
        },
        "home": {
            "ironmanabhi": {
                "files": ["file1.txt", "file2.txt", "file3.txt"],
                "directories": {
                    "Desktop",
                    "Documents",
                    "Downloads",
                    "Music",
                    "Pictures",
                    "Public",
                    "Templates",
                    "Videos",
                },
            },
        },
        "lib32": {
            "files": ["lib32_1.so", "lib32_2.so"],
            "directories": [],
        },
        "media": {
            "files": [],
            "directories": [],
        },
        "root": {
            "files": [],
            "directories": [],
        },
        "srv": {
            "files": [],
            "directories": [],
        },
        "var": {
            "log": {
                "files": ["app.log", "system.log"],
                "directories": [],
            },
            "tmp": {
                "files": [],
                "directories": [],
            },
        },
        "boot": {
            "files": ["vmlinuz"],
            "directories": [],
        },
        "lib64": {
            "files": ["lib64_1.so", "lib64_2.so"],
            "directories": [],
        },
        "mnt": {
            "files": [],
            "directories": [],
        },
        "run": {
            "files": [],
            "directories": [],
        },
        "sys": {
            "files": [],
            "directories": [],
        },
        "vmlinuz": {
            "files": [],
            "directories": [],
        },
        "dev": {
            "files": [],
            "directories": [],
        },
        "opt": {
            "files": [],
            "directories": [],
        },
        "sbin": {
            "files": ["service1", "service2"],
            "directories": [],
        },
        "tmp": {
            "files": [],
            "directories": [],
        },
        "etc": {
            "files": ["config1", "config2"],
            "directories": [],
        },
        "lib": {
            "files": ["lib1.so", "lib2.so", "lib3.so"],
            "directories": [],
        },
        "usr": {
            "files": [],
            "directories": [],
        },
    },
}


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

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True

    def check_channel_shell_request(self, channel):
        return True


if __name__ == "__main__":
    server = "172.16.222.86"
    ssh_port = 2222

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", ssh_port))
    sock.listen(100)
    print("[+] Listening for connection ...")
    while True:
        client, addr = sock.accept()

        print("[+] Got a connection!", addr)
        Session = paramiko.Transport(client)
        Session.add_server_key(HOSTKEY)
        Session.set_gss_host(socket.getfqdn(""))
        Session.load_server_moduli()

        serv = Server()
        Session.start_server(server=serv)
        chan = Session.accept(20)
        if chan is None:
            print("*** No channel.")
            sys.exit(1)
        print("[+] Authenticated!")
        chan.send("Welcome to SSH\n".encode())
        chan.send("To exit, simply type 'exit'.\n")
        chan.send("Enter 'help' to see the list of commands\n".encode())
        while True:
            chan.send("$ ")
            cmd = chan.recv(1024)
            if not cmd:
                break
            cmd = cmd.decode("utf-8").strip()
            if (
                cmd.lower() == "exit"
                or cmd.lower() == "quit"
                or cmd.lower() == "logout"
            ):
                chan.send("Goodbye!\n")
                chan.close()
                break
            else:
                # command definitions
                chan.send()
