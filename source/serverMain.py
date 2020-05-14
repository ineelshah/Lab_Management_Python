import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys
import datetime
import pymysql

conn = pymysql.connect(host = 'localhost', user = 'Neel Shah', password = 'hiralkamlesh', db = 'attend')

sql = conn.cursor()

arr_ip = list()
arr_name = ['0']

def already(client_address):
    for i in range (0, len(arr_ip)):
        if arr_ip[i] == client_address:
            return True
    else:
        return False

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from Computer & IT Department. '\n' Type your name and press enter to register for the current session!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()
    
def handle_client(client, client_address):  # Takes client socket as argument.
    name = client.recv(BUFSIZ).decode("utf8")        
    if already(client_address[0]):     
        arr_ip.append(client_address[0])
        welcome1 = "This device is already being used by another user."
        welcome2 = "You can still send messages." + str(arr_ip)
        client.send(bytes(welcome1, "utf8"))
        client.send(bytes(welcome2, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
    
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                if len(clients) == 0:
                    SERVER.close()
                    sys.exit(0)
                    break
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break

    else:
        arr_ip.append(client_address[0])
        arr_name.insert(len(arr_name) + 1, name)
        if len(arr_name) <= 1:
            file_timestamper()
        f = open('attendance.txt', 'a')
        f.write(name + '\n')
        f.close()
        welcome1 = "Welcome %s! If you ever want to quit, type {quit} to exit." % name
        welcome2 = "Your name has been Added to the Attendance!"
        client.send(bytes(welcome1, "utf8"))
        client.send(bytes(welcome2, "utf8"))
        #attendance(name)
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                if len(clients) == 0:
                    SERVER.close()
                    sys.exit(0)
                    break
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def file_timestamper():
    today = datetime.datetime.today()
    today_str = today.strftime('%Y/%m/%d')
    f = open('attendance.txt', 'a')
    f.write("Attendance for:" + today_str + '\n')
    f.close()
"""
def attendance(name = ""):
    today = datetime.datetime.today()
    today_str = today.strftime('%Y/%m/%d')
    stud_name = name
    sql.execute("insert into `attend`(date, name) values(%s,%s)",today_str, stud_name)
    conn.commit()
"""


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33002
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    print(arr_ip)
    SERVER.close()
