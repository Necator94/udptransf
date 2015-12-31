def lookForNone(dataArray):
        lostPackets = 'ACK '
        for k in range(len(dataArray)):
                if dataArray[k] == None:  lostPackets = lostPackets + str(k) + ' '
        return lostPackets

