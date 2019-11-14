final_list = []
count = 0
with open("/root/PycharmProjects/crawler/password_list", "r") as passwords:
    for line in passwords:
        word = line.strip()
        if word not in final_list and len(word) > 5:
            count = count + 1
            print(count)
            final_list.append(word)
            with open('unique.list', 'w') as f:
                f.write("%s\n" % word)
                print(str(count) + " >> " + word)

with open('unique.list', 'w') as f:
    for item in final_list:
        f.write("%s\n" % item)
