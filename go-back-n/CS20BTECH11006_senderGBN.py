import socket
import time
import signal
import os


def handler(signum, frame):
   raise Exception("Timeout occurs")

def recvAck():
	global base
	global queue
	recvMsg, recvAddr = socket_udp.recvfrom(bufferSize)
	ack = int.from_bytes(recvMsg[0:2], byteorder='big')
	if(ack == base):
			
		if(base==nextseqnum):
			signal.alarm(0)
		else:
			signal.setitimer(signal.ITIMER_REAL, timeoutTime)

		queue.pop(0)
		print("packet ", base , " acknowledged")
		base+=  1	


def timeout():
	try:
		signal.setitimer(signal.ITIMER_REAL, timeoutTime)
		for packet in queue:
			socket_udp.sendto(  packet , recieverAddressPort)

	except Exception as e: 
		print(e)
		print("Timeout time too low i.e., ",timeoutTime)
		exit(0)

 
file_name = "testFile.jpg"
file_size = os.path.getsize(file_name)/1024
senderIP = "10.0.0.1"
senderPort   = 20001

recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
f =open(file_name,"rb")


# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

base =1
N =16
timeoutTime = 0.08
nextseqnum = 1
eof = 0
queue = []
data = f.read(bufferSize-3)

signal.signal(signal.SIGALRM, handler)
start_time = time.time()
flag = True
while True:
		
	try:
		if(nextseqnum<base+N and flag):
			packet = nextseqnum.to_bytes(2, byteorder='big') + data+ eof.to_bytes(1, byteorder='big')
			socket_udp.sendto(  packet , recieverAddressPort)
			queue.append(packet)
			if(base== nextseqnum):
				signal.setitimer(signal.ITIMER_REAL, timeoutTime)
			nextseqnum += 1
			data = f.read(bufferSize-3)
			if(not data):
				flag=False

		else:
			recvAck()
			if(not flag and len(queue)==0):
				break

	except Exception as e: 
		print(e)
		print("For base : ",base)
		timeout()
		continue
			

eof=1
socket_udp.sendto(eof.to_bytes(1, byteorder='big') , recieverAddressPort)
timeTaken = time.time() - start_time
print("File sent")
print("Throughput in KB/s", file_size/timeTaken)
socket_udp.close()
f.close()

    
    #wait for reply message from reciever
    
