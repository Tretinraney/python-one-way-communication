import pyaudio
import sys
import socket
import pyRTP as rtp

#Arguments to determine host address
HOST = sys.argv[1]
PORT = sys.argv[2]

data = bytes()
is_receiving = False

#Variables to collect the audio bytes from PyAudio
CHUNK_SIZE = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16 #Goes by 16 bits (2 bytes)
RATE = 44100 #Rate of transmission

#create PyAudio
pyAudio = pyaudio.PyAudio()

def mainLoop():
    global data
    global is_receiving
    try:
        while True:
            new_data = receivingSocket.recv(RATE)
            rtpPacket = rtp.decodeRTP(new_data)
            currFrameNbr = rtpPacket['seq_num']
            data += rtpPacket['payload']
            print("Current Seq Num: " + str(currFrameNbr))
            if len(data) >= CHUNK_SIZE and not is_receiving:
                is_receiving = True
                stream.start_stream()
                print(f"\nStream started and there is {str(len(data) / RATE)} seconds of latency")
    except KeyboardInterrupt:
        print("\nClosing stream...")
        receivingSocket.close()
        stream.stop_stream()
        stream.close()
        pyAudio.terminate()

#define the callback
def pyaudio_callback(in_data, frame_count, time_info, status):
    if not is_receiving:
        return (bytes([0] * frame_count * CHANNELS * 2), pyaudio.paContinue)

    global data
    try:
        avail_data_count = min(frame_count*CHANNELS*2, len(data))
        return_data = data[:avail_data_count]
        data = data[avail_data_count:]

        #If there is not enough audio, will inflate with 0s
        return_data += bytes([0] * (frame_count*CHANNELS*2-avail_data_count))

        return (return_data,pyaudio.paContinue)
    except:
        print("Exception in Callback...")

#Open a pyAudio stream
stream = pyAudio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK_SIZE,
                stream_callback=pyaudio_callback)

receivingSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receivingSocket.bind((HOST, int(PORT)))
print("Socket bind succeed")

try:
    print("Listening for packets...")
    mainLoop()
except KeyboardInterrupt:
    sys.exit(1)






