import socket
import random
import pickle
import time

#variables im gonna use(maybe)
MSS = 12
#seq,ack,syn,fin
header = [0, 0, 0, 0]

#Variables needed for socket connection
portList = [7777, 7778, 7779, 7710]
server_address = ('localhost', 7777)

#Test variables
msg = "Din beske ble modtagt TonniBob."

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Static server port
sock.bind(server_address)

def extract_header(data):
    headerR = [0]
    for x in data:
        index = 0
        if x == "!":
            for z in data:
                if z == "?":
                    break
                else:
                    if z != "!":
                        headerR = z
                        index += 1
        return headerR

def extract_payload(data):
    nekst = 0
    payload = None
    index = 0

    for z in data:
        if nekst == 1:
            payload = z
            break
        if z == "?":
            nekst = 1
    return payload

def if_syn(this_head, add):
    our_head = [0, 0, 0, 0]
    if this_head[2] == 1:
        our_head[0] = random.randint(1, 1001)
        our_head[1] = this_head[0] + 1
        our_head[2] = 1
        our_head[3] = 0
        # now send segment with no payload to listening port
        load = None
        cucumber = ["!", our_head, "?", load]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, add)
        print("sending syn-ack to client")



def if_normal(this_head, add, payload):
    our_head = [0, 0, 0, 0]
    if this_head[2] == 0 and payload is not None:
        our_head[2] = 0
        our_head[1] = this_head[0] + 1
        our_head[0] = this_head[1]
        # probably redundant
        our_head[3] = 0
        load = "This is a server response"
        cucumber = ["!", our_head, "?", load]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, add)
        print("syn ack syn complete, sending pakcet to client")

def ack_fin(this_head, address):
    our_head = [0, 0, 0, 0]
    if this_head[3] == 1:
        our_head[2] = 0
        our_head[1] = this_head[0] + 1
        our_head[0] = this_head[1]
        # probably redundant
        our_head[3] = 1
        print("Acking FIN")

        cucumber = ["!", our_head, "?"]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, address)


        our_head[2] = 0
        our_head[1] = this_head[0] + 1
        our_head[0] = this_head[1]
        # probably redundant
        our_head[3] = 0
        print("sending FIN")

        cucumber = ["!", our_head, "?"]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, address)

        data, server = sock.recvfrom(4096)
        data_arr = pickle.loads(data)
        headF = extract_header(data_arr)
        if this_head[1] == headF[0]:
            print("closing connection")
            time.sleep(30)
            sock.close()



def init_fin(address, this_head):
    our_head = [0, 0, 0, 0]

    our_head[0] = this_head[1]
    our_head[1] = this_head[0] +1
    our_head[2] = 0
    our_head[3] = 1

    # now send segment with no payload to listening port
    cucumber = ["!", our_head, "?"]
    data_string = pickle.dumps(cucumber)
    sent = sock.sendto(data_string, server_address)

    data, server = sock.recvfrom(4096)
    data_arr = pickle.loads(data)
    headF = extract_header(data_arr)
    if headF[3] == 1:
        our_head[2] = 0
        our_head[1] = headF[0] + 1
        our_head[0] = headF[1]
        # probably redundant
        our_head[3] = 0
        print("Acking FIN")

        cucumber = ["!", our_head, "?"]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, address)
        time.sleep(30)
        sock.close()







while True:
    data, address = sock.recvfrom(4096)
    data_arr = pickle.loads(data)
    this_header = extract_header(data_arr)
    payload = extract_payload(data_arr)
    #which protocol
    if_syn(this_header, address)
    if_normal(this_header, address, payload)
    ack_fin(this_header, address)

    print('received "%s"' % repr(data_arr))






