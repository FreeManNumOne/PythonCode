import random,string

def CreatePassword():
    src = string.ascii_letters + string.digits
    salt = '~!@#$%^&*()_+=-'
    count = input('请确认要生成几条密码： ')
    list_passwds = []
    for i in range(int(count)):
        list_passwd_all = random.sample(src, 6)
        list_passwd_all.extend(random.sample(string.digits, 2))
        list_passwd_all.extend(random.sample(string.ascii_lowercase, 2))
        list_passwd_all.extend(random.sample(string.ascii_uppercase, 2))
        list_passwd_all.extend(random.sample(salt, 3))
        random.shuffle(list_passwd_all)
        str_passwd = ''.join(list_passwd_all)
        if str_passwd not in list_passwds:
            list_passwds.append(str_passwd)
    print(list_passwds)

if __name__ == '__main__':
    CreatePassword()
