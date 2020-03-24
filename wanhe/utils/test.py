from werkzeug.security import check_password_hash, generate_password_hash

if __name__ == '__main__':
    print(generate_password_hash('0pen.Wanhe.Admin'))