import a2s

def grab_server(ip=None, port=None):

    if (ip == None or port == None):
        ip = "stutpip123.ddns.net"
        port = 2401

    server = (ip, port)

    try:

        server_info = a2s.info(address=server)
        server_players = a2s.players(address=server)

    except:

        server_info = False
        server_players = False

    return [server_info, server_players]

if (__name__ == "__main__"):
    server = grab_server()

    print(server[0], server[1])