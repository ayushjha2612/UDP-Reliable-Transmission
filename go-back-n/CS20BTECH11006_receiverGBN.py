import socket

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size
recv_file = "recv.jpg"

f = open(recv_file, "wb")


# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))
numrecv=0
print("UDP socket created successfully....." )
exp_packet = 1
while True:

#wait to recieve message from the server
    data, senderAddr = socket_udp.recvfrom(bufferSize)
    eof = int.from_bytes(data[-1:], byteorder='big')
    if eof == 1 :
        break

    act_packet  = int.from_bytes(data[0:2], byteorder='big')
    if(act_packet == exp_packet ):
        f.write(data[2 :-1])
        print("Writing", act_packet)
        numrecv = numrecv+1
        socket_udp.sendto(act_packet.to_bytes(2, byteorder='big') , senderAddr)
        exp_packet = exp_packet+1
    else:
        if(act_packet < exp_packet):
            print("Duplicate packet ", act_packet)
            socket_udp.sendto((act_packet).to_bytes(2, byteorder='big') , senderAddr)

    

print(numrecv)
f.close()
socket_udp.close()
