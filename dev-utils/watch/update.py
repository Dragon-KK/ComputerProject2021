def update(main : str, dependent : str):
    data = ""
    try:
        with open(main,"r") as f:
            data = f.read()
        with open(dependent,"w") as f:
            f.write(data)
        return {"returnCode" : 0, "comment" : f"Succesfully updated : {dependent}", "error" : None}
    except Exception as e:
        return {"returnCode" : -1, "comment" : f"Failed to update : {dependent}", "error" : e}
