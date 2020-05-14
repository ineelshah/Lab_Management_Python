import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *

class client:
    def __init__(self):
        
        self.firstclick = True

        self.root = Tk()
        self.my_msg = StringVar()
        self.entry_field = Entry(self.root, textvariable=self.my_msg)
        self.client_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.BUFSIZ = 1024
        self.messages_frame = Frame(self.root)
        self.scrollbar = Scrollbar(self.messages_frame)
        self.send_button = Button(self.root, text="Send", command=self.send)
        self.msg_list = Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.receive_thread = Thread(target=self.receive)
        self.msg = ""
        self.root.title("ChatIO")
        self.my_msg.set("Type your messages here.")
        self.my_msg.get()
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()


        self.entry_field.bind('<FocusIn>', self.on_entry_click)
        self.entry_field.bind("<Return>", self.send)
        self.entry_field.pack()

        self.send_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_entry_click(self, event):     
        if self.firstclick: # if this is the first time they clicked it
            self.firstclick = False
            self.entry_field.delete(0, "end") # delete all the text in the entry


    def receive(self):
        while True:
            try:
                self.msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(END, self.msg)
            except OSError:  # Possibly client has left the chat.
                break

    """
    def send(self, event=None):  # event is passed by binders.
        
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))
        
        if msg == "{q}":
            self.client_socket.close()
            self.root.quit()
    """
    def send(self, event=None):
        
        self.msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        self.client_socket.send(bytes(self.msg, "utf8"))
        if self.msg == "{q}":
            self.client_socket.close()
            self.root.quit()
        

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{q}")
        self.send()


    def client_program(self):


        #----Socket code----
        HOST = "127.0.0.1"
        PORT = ""
        if not PORT:
            PORT = 33002
        else:
            PORT = int(PORT)


        ADDR = (HOST, PORT)

        self.client_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect(ADDR)


        self.receive_thread.start()
        self.root.mainloop()

