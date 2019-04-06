import socket
import threading
from tkinter import *


client_list = []
client_name = []
client_count = 0
threads = []
server_status = 1


def main():
    global client_count, server_status

    while client_count < 10:
        try:
            clientsocket, addr = serversocket.accept()
            client_list.append(clientsocket)
            # client_addr.append(addr)
            temp_name = "Client " + str(client_count)
            client_name.append(temp_name)

            cur = len(client_list) - 1

            lock = threading.Lock()
            threads.append(threading.Thread(target=serve, args=(client_list[cur], cur, lock,)))
            threads[cur].start()

            client_count = client_count + 1

            active_clients()
            # connect(client_list[client_count])

        except OSError:
            if server_status == 0:
                exit(0)


def serve(client, count, lock):
    global client_count, server_status
    flag = 1
    while flag == 1 and server_status == 1:
        lock.acquire()

        try:
            recv = client.recv(1024)
            print(client_name[count] + ": " + recv.decode('ascii'))

            msg = recv.decode('ascii')

            text = client_name[count] + ": " + msg

            if recv.decode('ascii') == 'bye':
                temp = "client_name[count] + ' has left'"
                text = text + '\n' + temp

            for cl in client_list:
                # if cl != client:
                cl.send(text.encode('ascii'))

            if recv.decode('ascii') == 'bye':
                print(client_name[count] + ' has left')
                client_name.remove(client_name[count])
                client_list.remove(client)
                client_count = client_count - 1
                del threads[count]
                flag = 0
                active_clients()

        # client has left :(
        except ConnectionResetError:
            print(client_name[count] + ' has left')
            client_name.remove(client_name[count])
            client_list.remove(client)
            del threads[count]
            client_count = client_count - 1
            flag = 0
            active_clients()
            pass
        lock.release()
    pass


def active_clients():
    i = 0
    print('\n\nList of all clients: ')
    buff = '\n\n---------------------List of all clients---------------------\n\n'
    for cl in client_list:
        c_host, c_port = cl.getpeername()

        buff = buff + '\n> ' + client_name[i] + ': < ' + str(c_host) + ' , ' + str(c_port) + ' >'

        txt.config(state="normal")
        txt.delete(1.0, END)
        txt.insert(END, buff + '\n')
        txt.config(state=DISABLED)

        print('> ' + client_name[i] + ': < ' + str(c_host) + ' , ' + str(c_port) + ' >')
        i = i + 1
    pass


def stop():
    global server_status, client_list
    server_status = 0
    serversocket.close()
    exit(0)
    pass


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
serversocket.bind((host, port))
serversocket.listen(10)


window = Tk()
window.title("Server")
window.geometry('1000x700')


# chat history
txt = Text(window)
txt.pack(side=LEFT, fill=Y)
txt.config(state=DISABLED)


scrl = Scrollbar(window)
scrl.pack(side=RIGHT, fill=Y)


txt.config(yscrollcommand=scrl.set)
scrl.config(command=txt.yview)

btn = Button(window, text="Stop Server!", command=stop)
btn.pack()

main_thread = threading.Thread(target=main, args=())
main_thread.start()

update_thread = threading.Thread(target=active_clients, args=())
update_thread.start()

window.configure(background='black')
window.mainloop()


exit(0)
