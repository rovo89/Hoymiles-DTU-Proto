#!/usr/bin/env python3
import socket
from protobuf_inspector.types import StandardParser
import AppGetHistPower_pb2
import time
import crcmod

# Define the server address and port
server_address = ('192.168.1.203', 10081)

crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
sequence = 1

try:
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)

    request = AppGetHistPower_pb2.AppGetHistPowerRes()
    request.oft = 28800
    request.time = int(time.time())

    header = b'\x48\x4d\xa3\x15'
    crc = crc16(request.SerializeToString())
    length = len(request.SerializeToString())+10

    # Send the data
    #print(f"Sending: {header}{sequence.to_bytes(2,byteorder='big')}{crc.to_bytes(2, byteorder='big')}{length.to_bytes(2, byteorder='big')}{request.SerializeToString()}")
    client_socket.send(header+sequence.to_bytes(2,byteorder='big')+crc.to_bytes(2, byteorder='big')+length.to_bytes(2, byteorder='big')+request.SerializeToString())

    sequence=sequence+1
    # Receive the response
    response_data = client_socket.recv(1024)
    #print(f"Response: {response_data}")
    response = AppGetHistPower_pb2.AppGetHistPowerReq()
    response.ParseFromString(response_data[10:])
    for field_descriptor, value in response.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')


except Exception as e:
    print(f'Error: {e}')

finally:
    # Close the socket
    client_socket.close()
