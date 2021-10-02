class console:
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