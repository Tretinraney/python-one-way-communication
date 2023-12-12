def createRTP(packet_vars):
    #First byte of the header as a binary string
    version = format(packet_vars['version'], 'b').zfill(2)
    padding = format(packet_vars['padding'], 'b')
    extension = format(packet_vars['extension'], 'b')
    csrc_cnt = format(packet_vars['csi_count'], 'b').zfill(4)
    byte1 = format(int((version + padding + extension + csrc_cnt),2),'x').zfill(2)

    #Second byte of the header as a binary string
    marker = format(packet_vars['marker'], 'b')
    payload_type = format(packet_vars['payload_type'], 'b').zfill(7)
    byte2 = format(int((marker + payload_type), 2), 'x').zfill(2)

    #Next sections of RTP header
    seq_num = format(packet_vars['seq_num'],'x').zfill(4) #16 bits = 4 hex
    timestamp = format(packet_vars['timestamp'],'x').zfill(8) #32 bits = 8 hex
    ssrc = format(packet_vars['ssrc'],'x').zfill(8)

    #Format payload
    payload = packet_vars['payload'].hex()

    #Create the RTP packet
    packet = byte1 + byte2 + seq_num + timestamp + payload

    #return the packet
    return packet.encode()

def decodeRTP(packet_bytes):
    #Get the variables from the packet (Byte 1)
    packet_vars = {}
    byte1 = packet_bytes[0:2] #Grab 0-2 bytes
    byte1 = int(byte1,16) #Convert to Hex
    byte1 = format(byte1, 'b').zfill(8) #Convert to binary and fill with 0s if needed
    packet_vars['version'] = int(byte1[0:2],2) #Gather version (0 and 1 bit) in binary
    packet_vars['padding'] = int(byte1[2:3], 2)
    packet_vars['extension'] = int(byte1[3:4])
    packet_vars['csi_count'] = int(byte1[4:8], 2)

    #Do the same for the second byte
    byte2 = packet_bytes[2:4]
    byte2 = int(byte2, 16)
    byte2 = format(byte2, 'b').zfill(8)
    packet_vars['marker'] = int(byte2[0:1])
    packet_vars['payload_type'] = int(byte2[1:8], 2)

    #Gather the bigger variables from the packet in hex
    packet_vars['seq_num'] = int(packet_bytes[4:8], 16)
    packet_vars['timestamp'] = int(packet_bytes[8:16], 16)
    packet_vars['ssrc'] = int(packet_bytes[16:24], 16)

    #Grab the payload
    payload = packet_bytes[24:]
    packet_vars['payload'] = bytes.fromhex(payload.decode())

    return packet_vars




