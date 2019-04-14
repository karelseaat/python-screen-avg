"""
The MIT License (MIT)
Copyright © 2018 Jean-Christophe Bos & HC² (www.hc2.fr)
"""

from ure import match
import socket
import gc

class MicroDNSSrv :


    def _ipV4StrToBytes(ipStr) :

        parts = ipStr.split('.')
        if len(parts) == 4 :
            return bytes( [ int(parts[0]),
                            int(parts[1]),
                            int(parts[2]),
                            int(parts[3]) ] )



    def _getAskedDomainName(packet) :
        queryType = (packet[2] >> 3) & 15
        qCount    = (packet[4] << 8) | packet[5]
        if queryType == 0 and qCount == 1 :
            pos     = 12
            domName = ''
            while True :
                domPartLen = packet[pos]
                if (domPartLen == 0) :
                    break
                domName += ('.' if len(domName) > 0 else '') \
                         + packet[ pos+1 : pos+1+domPartLen ].decode()
                pos     += 1+domPartLen
            return domName



    def _getPacketAnswerA(packet, ipV4Bytes) :
        

        queryEndPos = 12
        while True :
            domPartLen = packet[queryEndPos]
            if (domPartLen == 0) :
                break
            queryEndPos += 1 + domPartLen
        queryEndPos += 5

        return b''.join( [
            packet[:2],             # Query identifier
            b'\x85\x80',            # Flags and codes
            packet[4:6],            # Query question count
            b'\x00\x01',            # Answer record count
            b'\x00\x00',            # Authority record count
            b'\x00\x00',            # Additional record count
            packet[12:queryEndPos], # Query question
            b'\xc0\x0c',            # Answer name as pointer
            b'\x00\x01',            # Answer type A
            b'\x00\x01',            # Answer class IN
            b'\x00\x00\x00\x1E',    # Answer TTL 30 secondes
            b'\x00\x04',            # Answer data length
            ipV4Bytes ] )           # Answer data


    def __init__(self) :
        self._domList = { }


    def _serverProcess(self):

        packet, cliAddr = self._server.recvfrom(256)
        domName = MicroDNSSrv._getAskedDomainName(packet)
        if domName:
            domName = domName.lower()
            ipB = self._domList.get(domName, None)
            if not ipB:
                for domChk in self._domList.keys() :
                    if domChk.find('*') >= 0 :
                        print("whut ?")
                        r = domChk.replace('.', '\.').replace('*', '.*') + '$'
                        if match(r, domName) :
                            ipB = self._domList.get(domChk, None)
                            break
                if not ipB :
                    ipB = self._domList.get('*', None)
            if ipB:

                packet = MicroDNSSrv._getPacketAnswerA(packet, ipB)
                if packet :
                    print("send: ", packet, cliAddr)
                    self._server.sendto(packet, cliAddr)


    def Start(self) :
        self._server = socket.socket( socket.AF_INET,
                                      socket.SOCK_DGRAM )
        self._server.setsockopt( socket.SOL_SOCKET,
                                 socket.SO_REUSEADDR, 1)
        self._server.bind(('0.0.0.0', 53))
        self._server.setblocking(True)


    def Stop(self) :
        self._server.close()


    def SetDomainsList(self, domainsList) :
        if domainsList and isinstance(domainsList, dict) :
            o = { }
            for dom, ip in domainsList.items() :
                if isinstance(dom, str) and len(dom) > 0 :
                    ipB = MicroDNSSrv._ipV4StrToBytes(ip)
                    if ipB :
                        o[dom.lower()] = ipB
                        continue
                break
            if len(o) == len(domainsList) :
                self._domList = o
                return True
        return False