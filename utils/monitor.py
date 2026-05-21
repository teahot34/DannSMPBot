# 📄 monitor.py (hors de cogs/, ex: utils/monitor.py)

from mcstatus import JavaServer
from datetime import datetime
import json
import os

HISTORIQUE_PATH = "data/historique.json"

def ping_server_et_enregistrer():
    try:
        server = JavaServer.lookup("heldery.tomiix.fr:25565")
        status = server.status()
        joueurs = [p.name for p in status.players.sample] if status.players.sample else []
        enregistrer_joueurs(joueurs)
        return joueurs
    except Exception as e:
        print(f"Erreur de ping : {e}")
        return []

def enregistrer_joueurs(joueurs):
    if not joueurs:
        return

    if not os.path.exists(HISTORIQUE_PATH):
        os.makedirs(os.path.dirname(HISTORIQUE_PATH), exist_ok=True)
        with open(HISTORIQUE_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    if date_str not in data:
        data[date_str] = {}

    for joueur in joueurs:
        data[date_str].setdefault(joueur, []).append(time_str)

    with open(HISTORIQUE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
