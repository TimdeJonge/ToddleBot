import cfg
from time import sleep
import socket
import converter
import handler
from time import time
def chat(sock, msg, channel):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG {} :{}\r\n".format(channel, msg).encode("utf-8"))

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("CAP REQ : twitch.tv/commands twitch.tv/membership \r\n".encode())

s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
for channel in cfg.CHAN:
    s.send("JOIN {}\r\n".format(channel).encode("utf-8"))
chat(s, "HeyGuys", "#toddle_bot")
lastChecked = time()
while True:
    response = s.recv(4096).decode("utf-8").split("\n")
    if time() - lastChecked > 60:
        lastChecked = time()
        handler.handle("DISTRIBUTE")
    for line in response:
        print(line)
        neatline = converter.convert(line)
        print(neatline)
        done = handler.handle(neatline)
        if done == "PING":
            s.send("PONG :tmi.twitch.tv \r\n".encode())
        elif done == "Success" or done == "?":
            pass
        elif "MSG" in done[0]:
            chat(s, done[0][4:], done[1])
            pass # TODO: Betere error handling.
            #s.send(("PRIVMSG #toddle_bot :" + done + "\r\n").encode())

        parts = line.split(":")
        if parts[0] == "PING ":
            s.send(("PONG :" + parts[1]).encode("utf-8"))
            print("PONGED")
    sleep(1/cfg.RATE)