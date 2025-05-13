# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:29:15 2023

@author: AB0214
"""

import socket

def record_packets():
    # Set up the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 5300))  # Bind to the IP and port you want to listen on
    
    packets = []
    
    while True:
        data, addr = sock.recvfrom(1024)  # Receive data from the UDP socket
        packets.append(data)
    
    sock.close()
    return packets