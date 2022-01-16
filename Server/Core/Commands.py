class Commands:
    # Connection management commands
    DISCONNECT = "<DC>" # Sent when the client wants to dissconnect
    CONNECT_MAIN = "<CM>" # Sent when the first socket connection is made with the server
    CONNECT_LISTENER = "<CL>" # Sent when the second socket connection is mades (the listener socket)
    VALIDATE_LISTENER = "<VL>" # Sent when the listener connection has been made succesfully
    LISTENER_REGISTERED = "<LR>" # Sent when the listener connection has been made succesfully

    # Server commands (Sent by the server to the client)
    ShowGames = "(SG)" # Sent when a new game request is made (by other clients) or previous game requests are to be given
    HideGames = "(HG)" # Sent when a game request was removed
    BeginGame = "(BG)" # Sent to both clients when a game request has been accepted by another client

    # Client commands (Sent by the client to the server)
    CancelGame = "[-G]" # Sent when a game request is to be added in the lobby
    CreateGame = "[+G]" # Sent when a game request is to be removed in the lobby
    AcceptGame = "[AG]" # Sent when a game request has been accepted
    GetGames = "[GG]" # Sent when a list of all game requests is needed


