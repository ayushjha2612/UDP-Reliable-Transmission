import socket
import time
import signal
import os


def handler(signum, frame):
   raise Exception("Timout occurs")

file_name = "testFile.jpg"
file_size = os.path.getsize(file_name)/1024
senderIP = "10.0.0.1"
senderPort   = 20001

num_transmissions = 0
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
f =open(file_name,"rb")
timeoutTime = 0.01

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

seq_num = 1
eof = 0

data = f.read(bufferSize-3)

# print(int.from_bytes(data[-1:], byteorder='big'))
# print(sys.getsizeof(data))
signal.signal(signal.SIGALRM, handler)
start_time = time.time()
while data:
		
	try:
		socket_udp.sendto(  seq_num.to_bytes(2, byteorder='big') + data+ eof.to_bytes(1, byteorder='big') , recieverAddressPort) 
		signal.setitimer(signal.ITIMER_REAL, timeoutTime)
		recvMsg, recvAddr = socket_udp.recvfrom(bufferSize)
		ack = int.from_bytes(recvMsg[0:2], byteorder='big')
		while True:
			if(ack == seq_num):
				signal.alarm(0)
				data = f.read(bufferSize-3)
				print("packet ", seq_num , " acknowledged")
				seq_num += 1	
				break

	except Exception as e: 
		print(e)
		num_transmissions+=1
		continue

    #socket_udp.sendto(data, recieverAddressPort)
    #print("Sending")

eof=1
socket_udp.sendto(eof.to_bytes(1, byteorder='big') , recieverAddressPort)
timeTaken = time.time() - start_time
print("File sent")
print("Throughput in KB/s", file_size/timeTaken)
print("Number of retransmissions : ", num_transmissions)
socket_udp.close()
f.close()

    
    #wait for reply message from reciever
    
