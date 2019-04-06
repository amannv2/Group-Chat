import socket
import threading
from tkinter import *


def send_message():
    # old_message = self.chat_history.toPlainText()
    message = ent.get()

    if len(message) > 0:
        s.send(message.encode('ascii'))
        if message == 'bye':
            exit(0)
    ent.delete(0, END)
    ent.insert(0, "")


def read_message():
    while True:
        try:
            received_text = (s.recv(1024)).decode('ascii')
            old_message = '\nYou: ' + ent.get() + '\n'

            # get_data.put(old_message + received_text + '\n')

            txt.config(state="normal")

            txt.insert(END, received_text + '\n')
            print('>>>' + old_message + received_text)

            txt.config(state=DISABLED)

        except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError, ConnectionError):
            print('Server Not Available, Shutting Down..')
            # get_data.put('Server Not Available, Shutting Down..')
            exit(0)

        except RuntimeError:
            print('Bye, Shutting Down')
            exit(0)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
s.connect((host, port))


window = Tk()
window.title("Client")
window.geometry('700x500')

chat_history = Label(window, text="Chat History")
chat_history.grid(row=0, column=0)

# chat history
txt = Text(window, width=50)
txt.grid(row=1, column=0, sticky=N+E+W+S)
txt.config(state=DISABLED)


scrl = Scrollbar(window)
scrl.grid(row=1, column=1, sticky=N+S)


txt.config(yscrollcommand=scrl.set)
scrl.config(command=txt.yview)

enter_message = Label(window, text="Enter Your Message")
enter_message.grid(row=0, column=2)

# send message
ent = Entry(window, width=30)
ent.grid(row=1, column=2)


btn = Button(window, text="Send", command=send_message)
btn.grid(row=1, column=3)


ent.focus()


read_thread = threading.Thread(target=read_message, args=())
read_thread.start()


window.configure(background='black')
window.mainloop()

exit(0)
