def encrypt_field(login, password, limit=1):
    out = []
    len_login = 0
    for item in range(len(password)):
        if len_login == len(login) and limit == 1:
            len_login = 0
        elif len_login == len(login) and limit == 2:
            return ''.join(out)
        tmp = (144 ^ ord(password[item]) ^ ord(login[len_login]) )
        out.append('{:x}'.format(tmp))
        len_login += 1
    return ''.join(out)
