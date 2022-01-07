class Helper:
    @staticmethod
    def ParseMessage(msg):
        return msg.decode("utf-8")

    @staticmethod
    def ParseHeader(header):
        return header.decode("utf-8")
    
    @staticmethod
    def SendMessage(msg, conn):
        pass