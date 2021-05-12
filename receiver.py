import sys
import math
import time
#import sender
#import nEmulator
from socket import *
import random
import collections


hostname = sys.argv[1]   # host1
e_r_in = int(sys.argv[2])  # 9993
e_r_out = int(sys.argv[3]) # 9994
output = open( sys.argv[4], "w" )
arrival_log = open('arrival_log', 'w')
packet = []
ack = []

receiverSocket = socket(AF_INET, SOCK_DGRAM)


packetSocket = socket( AF_INET, SOCK_DGRAM )
packetSocket.bind( ('', e_r_in ) )

while True:
	#packetSocket, addr = receiverSocket.recvfrom(1024)
	packetInts = packetSocket.recvfrom(1024)
	checkEOT = packetInts 
	packetData = packetSocket.recvfrom(1024)
	packetInts = packetInts[0].decode(('utf-8'))
	packetInts = list(map(int, packetInts.strip()[1:-1].split(',')))
	if(packetInts[0] == 2):
		receiverSocket.sendto(checkEOT[0],(hostname,e_r_out))
		receiverSocket.sendto(packetData[0],(hostname,e_r_out))
		print("EOT sent")
		break

	packetData = packetData[0].decode(('utf-8'))
	sequence = packetInts[1]
	arrival_log.write(str(sequence) + '\n')
	

	packet.append(packetInts)
	#packetData = packetData[0].decode('utf-8')
	packetInts.append(packetData)

	ack.append([0,sequence,0,""])

	ACKs = str([0,sequence,0])
	ACKInts = bytes(str(ACKs), 'utf-8')
	
	
	ACKData = bytes("",('utf-8'))

	receiverSocket.sendto(ACKInts,(hostname,e_r_out))
	receiverSocket.sendto(ACKData,(hostname,e_r_out))

	




sorted_list = sorted(packet, key=lambda x: x[1])
#print(sorted_list)
for i in range(len(sorted_list)):
	output.write(str(sorted_list[i][3])+"\n" )
print("almost EOT received")

# print("EOT sent")

receiverSocket.close()
packetSocket.close()
