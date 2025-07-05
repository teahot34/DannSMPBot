# 📄 cogs/monitor.py

from mcstatus import JavaServer
from datetime import datetime
import pytz
import json
import os
import asyncio
from discord.ext import tasks, commands

HISTORIQUE_PATH = "data/historique.json"
LAST_SEEN_PATH = "data/last_seen.json"

def charger_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def enregistrer_nouveaux_joueurs(joueurs_actuels):
    now = datetime.now(pytz.timezone("Europe/Paris"))
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    historique = charger_json(HISTORIQUE_PATH)
    last_seen = charger_json(LAST_SEEN_PATH)

    if date_str not in historique:
        historique[date_str] = {}

    for joueur in joueurs_actuels:
        if joueur not in last_seen:
            historique[date_str].setdefault(joueur, []).append(f"{time_str}/...")
        last_seen[joueur] = time_str

    joueurs_actuels_set = set(joueurs_actuels)
    anciens_joueurs = set(last_seen.keys()) - joueurs_actuels_set

    for joueur in anciens_joueurs:
        heure_connexion = last_seen[joueur]
        if joueur in historique[date_str]:
            for i in range(len(historique[date_str][joueur]) - 1, -1, -1):
                if historique[date_str][joueur][i].endswith("/..."):
                    historique[date_str][joueur][i] = f"{heure_connexion}/{time_str}"
                    break
        del last_seen[joueur]

    sauvegarder_json(HISTORIQUE_PATH, historique)
    sauvegarder_json(LAST_SEEN_PATH, last_seen)

class MonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_server.start()

    def cog_unload(self):
        self.check_server.cancel()

    @tasks.loop(seconds=60)
    async def check_server(self):
        try:
            server = JavaServer.lookup("heldery.tomiix.fr")
            status = await server.async_status()
            sample = status.players.sample or []
            joueurs = [p.name for p in sample]
            enregistrer_nouveaux_joueurs(joueurs)
        except Exception as e:
            print(f"[Monitor] Erreur de ping : {e}")

    @check_server.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
