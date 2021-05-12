import sys
import math
from socket import *
import random
import select
##what are the 
print('reading args')
# handling cmd arguments
e_s_out_p = int(sys.argv[1]) # from emul to sender 9991
e_r_out_addr= sys.argv[2] # host2
e_r_out_p  = int(sys.argv[3]) #  from emul to recv 9994
e_r_in_p = int(sys.argv[4]) # from recv to emul 9993
e_s_out_addr = sys.argv[5] # host3
e_s_in_p = int(sys.argv[6]) # from sender to emul 9992
probability = float(sys.argv[7])
verbose_mode = int(sys.argv[8])



# initialise the sockets
e_s_in = socket(AF_INET, SOCK_DGRAM)
e_s_out = socket(AF_INET, SOCK_DGRAM)
e_r_in = socket(AF_INET, SOCK_DGRAM)
e_r_out = socket(AF_INET, SOCK_DGRAM)

# binding sockets
e_s_in.bind(('', e_s_out_p))   #(e_s_in,9991)
#e_s_out.bind(e_s_out_addr)
#e_s_out.bind(('',e_s_in_p))
e_r_in.bind(('', e_r_out_p))  # from recv program  #(e_r_in,9994)
#e_r_out.bind(e_r_out_addr)

# probability function to discard packets with the specified probability
# function that is randomly deciding if the packet is lost
def drop_packet():
    randnum = random.random() % 1
    if randnum < probability:
        return True
    else:
        return False


# establishing connections of outgoing sockets to their corresponding 
# addresses at the sender and reciever 
# e_s_out.connect(e_s_in_addr) # CONNECTING THE OUTGOING SOCKETS
# e_r_out.connect(e_r_in_addr)

sender_packets = []
ACK = []
notEOT = True
listening = [e_s_in, e_r_in]  # sockets to listen on
#print('listening for packets')
# listening for the packets

if verbose_mode == 1:
    while True:
        print('listening for packets')
        # find which sockets have data waiting to be received
        ready, a, b = select.select(listening, [], [])
        print(ready)
        print(a)
        print(b)
        for socket in ready:
            
            # deadling with sender first
            if socket == e_s_in:

                # recieving packets from the sender
                packetInts = socket.recvfrom(1024)
                
                packetData = socket.recvfrom(1024)
                print("packets are sent")
                EOTCheck = packetInts[0].decode(('utf-8'))
                EOTCheck = list(map(int, EOTCheck.strip()[1:-1].split(',')))
                if(EOTCheck[0] == 2):
                    notEOT = False
                    e_r_in.sendto(packetInts[0],(e_r_out_addr,e_r_in_p))
                    e_r_in.sendto(packetData[0],(e_r_out_addr,e_r_in_p))
                print("EOT sent") # [x,x,x,x]
                #sender_packets.append(packet_recv)

                if not drop_packet() and notEOT == True:
                    temp = []
                    e_r_in.sendto(packetInts[0],(e_r_out_addr,e_r_in_p))
                    e_r_in.sendto(packetData[0],(e_r_out_addr,e_r_in_p))
                    print("packet sent")
                    for elem in packetInts[0]:
                        #sender_packets.append(elem)
                        temp.append(elem)

                    temp.append(packetData[0].decode(('utf-8')))
                    sender_packets.append(temp)
                else:
                    print("packet dropped")

                #else:
                #    sender_packets.remove(packetInts)

            elif socket == e_r_in:
                ackInts = socket.recvfrom(1024)
                ackData = socket.recvfrom(1024)
                print("receiving ACKs")
                e_s_in.sendto(ackInts[0], (e_s_out_addr, e_s_in_p))
                e_s_in.sendto(ackData[0], (e_s_out_addr, e_s_in_p))

else:            
    while True:
        #print('listening for packets')
        # find which sockets have data waiting to be received
        ready, a, b = select.select(listening, [], [])
        for socket in ready:
            
            # deadling with sender first
            if socket == e_s_in:

                # recieving packets from the sender
                packetInts = socket.recvfrom(1024)
                
                packetData = socket.recvfrom(1024)
                #print("packets are sent")
                EOTCheck = packetInts[0].decode(('utf-8'))
                EOTCheck = list(map(int, EOTCheck.strip()[1:-1].split(',')))
                if(EOTCheck[0] == 2):
                    notEOT = False
                    e_r_in.sendto(packetInts[0],(e_r_out_addr,e_r_in_p))
                    e_r_in.sendto(packetData[0],(e_r_out_addr,e_r_in_p))
                #print("EOT sent") # [x,x,x,x]
                #sender_packets.append(packet_recv)

                if not drop_packet() and notEOT == True:
                    temp = []
                    e_r_in.sendto(packetInts[0],(e_r_out_addr,e_r_in_p))
                    e_r_in.sendto(packetData[0],(e_r_out_addr,e_r_in_p))
                 #   print("packet sent")
                    for elem in packetInts[0]:
                        #sender_packets.append(elem)
                        temp.append(elem)

                    temp.append(packetData[0].decode(('utf-8')))
                    sender_packets.append(temp)

            elif socket == e_r_in:
                ackInts = socket.recvfrom(1024)
                ackData = socket.recvfrom(1024)
                #print("receiving ACKs")
                e_s_in.sendto(ackInts[0], (e_s_out_addr, e_s_in_p))
                e_s_in.sendto(ackData[0], (e_s_out_addr, e_s_in_p))
