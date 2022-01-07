from .Protocol import Protocol

class Helper:
    @staticmethod
    def ParseMessage(msg):
        return msg.decode("utf-8")

    @staticmethod
    def ParseHeader(header):
        return header.decode("utf-8")

    @staticmethod
    def EncodeMessage(msg):
        return msg.encode("utf-8")

    @staticmethod
    def GetHeader(msg):
        '''Gives the header for a given encoded message'''
        header = str(len(msg)).encode("utf-8")
        header += b' ' * (Protocol.HEADER_LENGTH - len(header))
        return header

    @staticmethod
    def GetAddress():
        return ("10.0.0.102", 8008)