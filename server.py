import socket
import threading

def server():
    global fn
    f = open('server_log.txt', 'a')
    while True:
        conn, addr = sock.accept()
        print("Client connection")
        f.write("Client connection" + '\n')
        print(addr)
        #  Проверка логина и пароля в текстовых документах
        try:
            name = usr_dct[list(addr)[0]]
            pas = pas_dct[list(addr)[0]]
            while True:
                print('Input password: ', end='')
                check = input()
                if check == pas:
                    break
                else:
                    print('Incorrect password')
            print('Welcome ' + name)
        except KeyError:
            print('Input name: ', end='')
            name = input()
            usr = open('user.txt', 'a')
            usr.write(list(addr)[0] + ' ' + name + '\n')
            usr.close()

            print('Input password: ', end='')
            pas_reg = input()
            pas_file = open('pass.txt', 'a')
            pas_file.write(list(addr)[0] + ' ' + pas_reg + '\n')
            usr.close()

        f.write(str(addr))
        f.write('\n')

        #  Отправка сообщения
        msg = ''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Data receiving...")
            f.write("Data receiving..." + '\n')
            msg += data.decode()
            print("Data sending...")
            f.write("Data receiving..." + '\n')
            conn.send(data)
        print(msg)

        #  Остановка сервера
        print("Server stop")
        f.write("Server stop" + '\n')
        conn.close()

        #  Ожидание команды end на остановку потока
        print('input command:', end=' ')
        fn = input()
        f.write('input command: ' + fn + '\n')
        if fn == 'end':
            print('Thread off')
            f.write('Thread off' + '\n')
            f.close()
            break
        f.write('Thread off' + '\n')
        f.close()

#  Создание словарей для логинов и паролей по общему IP ключу
usr_dct = {}
pas_dct = {}

with open('user.txt', 'r') as usr:
    for i in usr.readlines():
        user = i.split(' ')
        usr_dct.update({user[0]:user[1]})

with open('pass.txt', 'r') as pswd:
    for i in pswd.readlines():
        ps = i.split(' ')
        pas_dct.update({ps[0]:ps[1][0:-1]})

#  Запуск сервера
try:
    f = open('server_log.txt', 'a')
    fn = ''
    sock = socket.socket()
    print("Boot up server")
    f.write("Boot up server"+'\n')
    df = ['', 9090]
    sock.bind(tuple(df))
    sock.listen(1)
    print("Listening...")
    f.write("Listening..."+'\n')
    f.close()
except OSError: #  Исключение возникает в случае, если порт подключения занят
    while True:
        try:
            df[1] = df[1] + 1
            sock.bind(tuple(df))
            sock.listen(1)
            break
        except OSError:
            pass

#  Организация многопоточного
ports = [threading.Thread(target=server) for i in range(1)]
for i in ports:
    i.start()

