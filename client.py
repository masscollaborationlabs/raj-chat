"""

A chat application written in Python client side client.py

Copyright (C) 2024 Venky-234 and contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
import threading 
import time
from tkinter import * 


ip = input("enter link : ").strip() 
port = int(input("enter port : "))
addr = (ip, port)

name = input("enter nickname : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

send_message = ''
recv_message = ''

def get_input():
    global send_message

    def set_message(event):
        global send_message
        send_message = entry.get()
        send_message = name + " : " + send_message
        send_message += '\n'
        entry.delete(0, END)

    window = Tk()
    window.title = "Input Box"
    entry = Entry(window, fg='white',bg='#000000',font=("Consolas", 16))
    entry.configure(insertbackground='white')
    entry.pack()
    entry.bind("<Return>", set_message)
    window.mainloop()
input_thread = threading.Thread(target=get_input)
input_thread.start()

send_message = name + " has joined the chat\n"
while True:
    heartbeat = client.recv(1).decode('utf-8')
    if heartbeat == '\x00':
        if send_message == '': 
            client.send('\x00'.encode('utf-8'))

        else:
            for i in send_message:
                client.send(i.encode('utf-8'))
            send_message = ''
    else:
        if heartbeat != '\n':
            recv_message += heartbeat
        else:
            print(recv_message)
            recv_message = ''
                
