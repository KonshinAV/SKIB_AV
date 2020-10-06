from utils import secure_string

if __name__ == '__main__':
    pwd = secure_string.SecureString("Pass")
    print (pwd.encoding())
    pass
