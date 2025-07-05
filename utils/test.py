from mcstatus import JavaServer

server = JavaServer.lookup("heldery.tomiix.fr")
status = server.async_status()

print(status.players.online)  # nombre de joueurs en ligne
print(status.players.max)     # nombre max de joueurs
print(status.players.sample)  # échantillon (liste partielle des joueurs connectés)
