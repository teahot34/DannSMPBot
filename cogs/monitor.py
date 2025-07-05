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

def enregistrer_connexions(joueurs_actuels):
    now = datetime.now(pytz.timezone("Europe/Paris"))
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    historique = charger_json(HISTORIQUE_PATH)
    last_seen = charger_json(LAST_SEEN_PATH)

    joueurs_actuels_set = set(joueurs_actuels)
    joueurs_précédents = set(last_seen.keys())

    # Joueurs connectés maintenant mais pas avant => connexion
    nouveaux = joueurs_actuels_set - joueurs_précédents
    # Joueurs qui étaient connectés mais plus maintenant => déconnexion
    partis = joueurs_précédents - joueurs_actuels_set

    for joueur in nouveaux:
        historique.setdefault(date_str, {}).setdefault(joueur, []).append(time_str)

    for joueur in partis:
        historique.setdefault(date_str, {}).setdefault(joueur, []).append(time_str)

    # Mise à jour des joueurs actuellement en ligne
    last_seen = {j: True for j in joueurs_actuels}

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
            enregistrer_connexions(joueurs)
        except Exception as e:
            print(f"[Monitor] Erreur de ping : {e}")

    @check_server.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
