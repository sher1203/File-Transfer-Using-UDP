#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import math
import time

# import nEmulator
# import receiver

from socket import *
import random




host_addr = sys.argv[1]     #host1
udp_emulator = sys.argv[2]  #9991
udp_sender_port_num = int(sys.argv[3]) #9992
timeout = sys.argv[4]
file_name = sys.argv[5]

data_log = open('seqnum.log', 'w')
ack_log = open('ack.log', 'w')

# packets

#acks = -1
packet = []
ack_list = []
packet_dup = []

max_num_of_packets = 30

# opening file and counting chars

data = open(file_name, 'r')
f = data.read()
num_of_chars = len(f)
last_packet_chars = num_of_chars % 500

if num_of_chars > 15000:
    raise Exception('File size is too large.')
else:

    num_of_packets = math.ceil(num_of_chars / 500)
    
    num_of_packets = int(num_of_packets)

    for i in range(0, num_of_packets):

        if i != num_of_packets:
            curr_data = f[500 * i:500 * (i + 1)]
            packet.append([1, i, len(curr_data), curr_data])
        else:
            curr_data = f[500 * i:last_packet_chars(i + 1)]
            packet.append([1, i, len(curr_data), curr_data])




length_packet = len(packet)
for elem in packet:
        packet_dup.append(elem)

senderPort = udp_sender_port_num
senderSocket = socket(AF_INET, SOCK_DGRAM)
senderSocket.bind(('', senderPort))  # （9992）

EOT_received = False

#senderSocket.connect((host_addr, int(udp_emulator)))
def timer():
    if(len(ack_list)==len(packet_dup)):
        return
    
    for i in range(0, len(packet)):

        # [1,0,193,"Data"]
        # # reading integers and converting to bytes

        int_list = packet[i][:3]
        #print ('int_list made')
        #print(int_list)
        
        bytelist = bytes(str(int_list),'utf-8')
        #print(bytelist)
        #print(host_addr)
        #print(int(udp_emulator))
        
        senderSocket.sendto(bytelist, (host_addr, int(udp_emulator)))
        #print ('byte sent')

        # #reading the data and converting that to bytes

        data = bytes(packet[i][3], 'utf-8')
        senderSocket.sendto(data, (host_addr, int(udp_emulator)))
        
        #print ('data sent')

        #print (str(packet[i][1]))
        data_log.write(str(packet[i][1]) + '\n')
        #print ('wrote packets')
        
        
        # connectionSocket, addr = senderSocket.recvfrom(1024)
       # print(time.time())
    t_init = t0 = time.time()

    while t0 <= (t_init + float(timeout)):
 # 

        ACKInts = senderSocket.recvfrom(1024)
        ACKData = senderSocket.recvfrom(1024)
        ACKInts = ACKInts[0].decode(('utf-8'))
        ACKInts = list(map(int, ACKInts.strip()[1:-1].split(',')))
        seq = ACKInts[1]

        ACKReceived = False
        
        
        #print ('received ACKData')
        #print (ACKData)
        ACKData = ACKData[0].decode('utf-8')
        ACKInts.append(ACKData)
        #print("ack = " + str(ACKInts))
        if ACKInts == [0,seq,0,""]:
 
            ACKReceived = True
        	
        ack_list.append(ACKInts)
        print (ack_list)
        if ACKReceived == True:
            ack_log.write(str(ACKInts[1]) + '\n')
        
        t0 = time.time()

        if (len(ack_list) != len(packet_dup)):
            for i in range(len(ack_list)):
                for j in range(0,len(packet_dup)):	
                    if ack_list[i][1] == packet_dup[j][1]:
                        if packet_dup[j] in packet:
                            packet.remove(packet_dup[j])
        
        else:
            EOTInts = bytes(str([2,0,0]),'utf-8')
            EOTData = ''
            senderSocket.sendto(EOTInts,(host_addr, int(udp_emulator)))
            senderSocket.sendto((bytes(EOTData, 'utf-8')),(host_addr, int(udp_emulator)))
            #print ('EOT sent')
            senderSocket.recvfrom(1024)
            senderSocket.recvfrom(1024)
            return                    



while EOT_received != True:
        timer()

senderSocket.close()



