class Console:
    @staticmethod
    def info(information):
        print(f"[Information] {information}")

    @staticmethod
    def log(msg):
        print(f"[Log] {msg}")

    @staticmethod
    def clientLog(clientAddr, msg):
        print(f"[Client {clientAddr}] {msg}")

    @staticmethod
    def serverLog(msg):
        print(f"[Server] {msg}")

    @staticmethod
    def error(errorType = "Unkown Error", errorLevel = "?",errorDesc = "An error has occured"):
        print(f"[Error ( Error level : {errorLevel} )] | type : {errorType} | {errorDesc}")