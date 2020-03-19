import socket
import random
import pickle
import time

#variables im gonna use(maybe)
#Maximum sekment size
MSS = 12
#seq,ack,syn,fin
header = [0,0,0,0]


#Variables needed for socket connection
server_address = ('localhost', 7777)
portList = [7777, 7778, 7779, 7710]



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#client contacs server host by sending first syn
def initConnection():
    our_head = [0,0,0,0]

    seqSart = random.randint(1, 1001)
    our_head[0] = seqSart
    our_head[1] = 0
    our_head[2] = 1
    our_head[3] = 0

    #now send segment with no payload to listening port
    load = None
    cucumber = ["!", our_head, "?", load]
    data_string = pickle.dumps(cucumber)
    sent = sock.sendto(data_string, server_address)
    print("sending syn to server")


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


def if_syn(this_head, address):  # send ack in response to syn-ack
    our_head = [0, 0, 0, 0]
    if this_head[2] == 1:
        our_head[2] = 0
        our_head[1] = this_head[0] + 1
        our_head[0] = this_head[1]
        #probably redundant
        our_head[3] = 0
        load = None
        cucumber = ["!", our_head, "?", load]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, address)
        print("sending ack to server")
        return True  # connection presumed to be establised
    else:
        return False


def if_normal(this_head, address, payload):  # ack normal
    our_head = [0, 0, 0, 0]
    if this_head[2] == 0 and payload is not None:
        our_head[2] = 0
        our_head[1] = this_head[0] + 1
        our_head[0] = this_head[1]
        # probably redundant
        our_head[3] = 0
        load = None
        cucumber = ["!", our_head, "?", load]
        data_string = pickle.dumps(cucumber)
        sent = sock.sendto(data_string, address)
        print("this is the server response: " + payload)





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



def init_fin(this_head, address):
    print("fin initialized")
    our_head = [0, 0, 0, 0]

    #INCREMENTERER FORDI VI SENDER ACK,FIN
    our_head[0] = this_head[1] + 1
    our_head[1] = this_head[0] + 1
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



## these methods are not part of the tcp mock, they are for testing

def user_input_p(this_head, address):
    our_head = [0, 0, 0, 0]
    our_head[2] = 0
    our_head[1] = this_head[0] + 1
    our_head[0] = this_head[1] + 1
    # probably redundant
    our_head[3] = 0
    print("conversation has begun:")

    load = input()
    cucumber = ["!", our_head, "?", load]
    data_string = pickle.dumps(cucumber)
    sent = sock.sendto(data_string, address)




#init
initConnection()

#receive
while True:
    # Buffer for packet size
    data, server = sock.recvfrom(4096)
    data_arr = pickle.loads(data)
    print('received "%s"' % repr(data_arr))

    head = extract_header(data_arr)
    payload = extract_payload(data_arr)

    zz = if_syn(head, server)
    if_normal(head, server, payload)
    ack_fin(head, server)

    while zz is True:

        user_input_p(head, server)

        data, server = sock.recvfrom(4096)
        data_arr = pickle.loads(data)
        print('received "%s"' % repr(data_arr))

        head = extract_header(data_arr)
        payload = extract_payload(data_arr)

        if_normal(head, server, payload)

















