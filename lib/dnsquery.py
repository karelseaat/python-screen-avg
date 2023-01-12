import usocket as socket

class DNSQuery:

    def __init__(self, ap):
        self.ip = ap.ifconfig()[0]
        self.udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udps.setblocking(False)
        self.udps.bind(('', 53))

    def makedomain(self, data):
        self.domain = ""

        m = data[2]
        tipo = (m >> 3) & 15
        if tipo == 0:
            ini = 12
            lon = data[ini]
            while lon != 0:
                self.domain+=data[ini+1:ini+lon+1].decode("utf-8") +'.'
                ini+=lon+1
                lon=data[ini] #ord(data[ini])


    def DNSQnA(self):
        try:
            data, addr = self.udps.recvfrom(4096)
            self.makedomain(data)
            preps = self.answer(data)


            self.udps.sendto(preps, addr)
        except Exception as e:
            print("No DNS", e)

    def answer(self, data):
        if self.domain:
            packet  = data[:2] + b'\x81\x80'
            packet += data[4:6] + data[4:6] + b'\x00\x00\x00\x00'   # Questions and Answers Counts
            packet += data[12:]                                          # Original Domain Name Question
            packet += b'\xC0\x0C'                                             # Pointer to domain name
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3C\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
            packet +=  bytes(map(int, self.ip.split('.')))                         # 4bytes of IP
        return packet
