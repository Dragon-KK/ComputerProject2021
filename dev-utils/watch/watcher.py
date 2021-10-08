from update import update
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
from os import path
print("Loading data")
dependents = {}
with open("dependents.json","r") as f:
    dependents = json.load(f)
print("Loaded data")
print(f"Currently updating [{', '.join(list(dependents.keys()))}]")
print("Starting watch : )")

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        p = path.normpath(event.src_path).split("\\")[-1]
        print(f"File {p} has been changed")
        for i in dependents.keys():
            x = dependents[i].get(p)
            if x:
                ret = update(r'../../common/' + p, i + x)
                print(ret["comment"])
                if ret["returnCode"] == -1:
                    print(ret["error"])
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='../../common', recursive=False)
observer.start()
try:
    input("Click {ENTER} to end")
except:
    pass
print("Ending watch....")
observer.stop()
observer.join()
print("Ended watch : )")