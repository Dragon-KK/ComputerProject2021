
from App.Core.DataManagers import FileManager

x = FileManager.ReadJson("Data/storage.json")
sa = input("Enter server address : ").split(":")
x['OnlineMultiplayer']['ServerAddress'] = [sa[0], int(sa[1])]

FileManager.WriteJson("Data/storage.json", x)