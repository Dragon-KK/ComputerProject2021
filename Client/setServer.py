
from App.Core.DataManagers import FileManager

x = FileManager.ReadJson("Data/Storage.json")
sa = input("Enter server address : ").split(":")
x['OnlineMultiplayer']['ServerAddress'] = [sa[0], int(sa[1])]

FileManager.WriteJson("Data/Storage.json", x)