import pyaudio
import sys
import socket
import pyRTP as rtp
import random

HOST = sys.argv[1]
PORT = sys.argv[2]

#Allows to gather audio bytes
data = bytes()

#Variables to collect the audio bytes from PyAudio
CHUNK_SIZE = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16 #Goes by 16 bits (2 bytes)
RATE = 44100 #Rate of transmission
def sendRTP():
    frameNumber = 0
    global data
    global stream
    while True:
        if data:
            frameNumber += 1
            print("Sending frame number: %d " % frameNumber)
            try:
                rtp_packet = makeRTP(data[:CHUNK_SIZE],frameNumber)
                sendSocket.sendto(rtp_packet,(HOST,int(PORT)))
                data = data[CHUNK_SIZE:]
            except KeyboardInterrupt:
                print("\nStopping Stream and closing socket...\n")
                stream.stop_stream()
                stream.close()
                pyAudio.terminate()
                sendSocket.close()

def makeRTP(data, frameNbr):
    packet_vars = {'version': 2,
                   'padding': 0,
                   'extension': 0,
                   'csi_count': 0,
                   'marker': 0,
                   'payload_type': 97,
                   'seq_num': frameNbr,
                   'timestamp': random.randint(1, 9999),
                   'ssrc': 185755418,
                   'payload': data}
    rtp_packet = rtp.createRTP(packet_vars)  # Creates a RTP packet with the header and data
    return rtp_packet

def mainLoop():
    try:
        while True:
            sendRTP()
    except KeyboardInterrupt:
        print("Closed")

#Initiate PyAudio
pyAudio = pyaudio.PyAudio()

def pyaudio_callback(in_data,frame_count,time_info,status):
    global data
    data += in_data
    return (None,pyaudio.paContinue)

#Open the pyAudio Stream
stream = pyAudio.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK_SIZE,
                      stream_callback=pyaudio_callback)

#Start the pyAudio Steam
stream.start_stream()

#Create the socket for transmission
sendSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

try:
    mainLoop()
except KeyboardInterrupt:
    print("Stopping Program...")
    sys.exit(1)