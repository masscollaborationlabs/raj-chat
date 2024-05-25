import threading
import socket
import time

port = 5050
ip = 'localhost'
addr = (ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)

print("Server is starting ...")

total_threads = threading.active_count()

def count_threads():
    global total_threads
    while True:
        if threading.active_count() != total_threads:
            total_threads = threading.active_count()
            print("total threads : ", total_threads)
        time.sleep(0.4)

thread_count = threading.Thread(target=count_threads)
thread_count.start()

clients = []
def handle_client(conn : socket, addr):
    message = '' 
    first_message = False
    global clients
    try:
        conn.send('\x00'.encode('utf-8'))
        while True:
            heartbeat = conn.recv(1).decode('utf-8')
            if heartbeat == '\x00':
                time.sleep(0.5)
            else:
                if heartbeat != '\n':
                    char = heartbeat 
                    message += char

                else:
                    print(message)
                    message += '\n'
                    for client in clients:
                        for i in message:
                            try:
                                client.send(i.encode('utf-8'))
                            except:
                                print("Could not send message to ", client)
                                
                    message = ''
                    conn.send('\x00'.encode('utf-8'))
                continue
    
            conn.send('\x00'.encode('utf-8'))
    except:
        print("client", addr, "disconnected")
        clients.remove(conn)

def start_server():
    server.listen(1)
    while True: 
        conn, addr = server.accept() 



