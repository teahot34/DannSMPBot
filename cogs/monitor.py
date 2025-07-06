from mcstatus import JavaServer
from datetime import datetime
import pytz
import json
import os
import asyncio
from discord.ext import tasks, commands

HISTORIQUE_PATH = "data/historique.json"
LAST_SEEN_PATH = "data/last_seen.json"
TIMEZONE = pytz.timezone("Europe/Paris")


def charger_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def enregistrer_joueurs(joueurs_actuels):
    now = datetime.now(TIMEZONE)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    historique = charger_json(HISTORIQUE_PATH)
    last_seen = charger_json(LAST_SEEN_PATH)

    joueurs_actuels_set = set(joueurs_actuels)
    anciens_joueurs = set(last_seen.keys())

    nouveaux = joueurs_actuels_set - anciens_joueurs
    partis = anciens_joueurs - joueurs_actuels_set

    # Enregistrer les connexions
    for joueur in nouveaux:
        historique.setdefault(date_str, {}).setdefault(joueur, []).append(f"{time_str}/")  # début sans fin
        last_seen[joueur] = {
            "start": now.isoformat()
        }

    # Enregistrer les déconnexions
    for joueur in partis:
        info = last_seen.get(joueur)
        if not info or "start" not in info:
            continue

        start_dt = datetime.fromisoformat(info["start"]).astimezone(TIMEZONE)
        start_date = start_dt.strftime("%Y-%m-%d")
        start_time = start_dt.strftime("%H:%M")

        # Session complète
        session_str = f"{start_time}/{time_str}"

        # Ajouter à la date de début
        historique.setdefault(start_date, {}).setdefault(joueur, []).append(session_str)

        # Si on a changé de jour, ajouter aussi à aujourd'hui
        if start_date != date_str:
            historique.setdefault(date_str, {}).setdefault(joueur, []).append(session_str)

        # Nettoyer
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
            enregistrer_joueurs(joueurs)
        except Exception as e:
            print(f"[Monitor] Erreur de ping : {e}")

    @check_server.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
