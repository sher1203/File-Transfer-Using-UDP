# File-Transfer-Using-UDP
Created a network emulator and coded sender and receiver programs to produce an unreliable file transfer network using UDP sockets in python 

1) Run the nEmulator by the command `python nEmulator.py 9991 host2 9994 9993 host 3 0.0 1`

2) Run the receiver by the command `python receiver.py host1 9993 9994 <output File>`

3)Run the sender by the command `python sender.py host1 9991 9992 5 0 <input file>`

You can run them locally with network, sender and receiver addresses as localhosts. For linux environment, use the address ending with -008 for receiver and sender and the address ending with -002 for the network emulator. 

