from Connection.Worker import Worker
from Connection.Protocol import Protocol
app = Worker()

app.SendMessage("Hello world")
input("Hello")
app.SendMessage(Protocol.Commands.DISCONNECT)