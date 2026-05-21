from mcstatus import JavaServer
from datetime import datetime
import pytz
import json
import os
<<<<<<< HEAD
from discord.ext import tasks, commands

# ==================== CONFIGURATION DU SERVEUR ====================
IP_SERVEUR = "dann-smp.mon-ip.com"  # Mets la nouvelle IP de ton serveur ici !
# ==================================================================

=======
import asyncio
from discord.ext import tasks, commands

>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
HISTORIQUE_PATH = "data/historique.json"
LAST_SEEN_PATH = "data/last_seen.json"
TIMEZONE = pytz.timezone("Europe/Paris")


def charger_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
<<<<<<< HEAD
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
=======
        return json.load(f)
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc


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

<<<<<<< HEAD
    # Enregistrer les NOUVELLES connexions
    for joueur in nouveaux:
        # On ajoute la session "en cours" (ex: 14:30/)
        historique.setdefault(date_str, {}).setdefault(joueur, []).append(f"{time_str}/") 
=======
    # Enregistrer les connexions
    for joueur in nouveaux:
        historique.setdefault(date_str, {}).setdefault(joueur, []).append(f"{time_str}/")  # début sans fin
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
        last_seen[joueur] = {
            "start": now.isoformat()
        }

<<<<<<< HEAD
    # Enregistrer les DÉCONNEXIONS
=======
    # Enregistrer les déconnexions
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
    for joueur in partis:
        info = last_seen.get(joueur)
        if not info or "start" not in info:
            continue

        start_dt = datetime.fromisoformat(info["start"]).astimezone(TIMEZONE)
        start_date = start_dt.strftime("%Y-%m-%d")
        start_time = start_dt.strftime("%H:%M")

<<<<<<< HEAD
        # Session complète (ex: 14:30/16:45)
        session_str = f"{start_time}/{time_str}"
        session_en_cours = f"{start_time}/"

        # On cherche et on remplace la session "en cours" par la session complète
        sessions_du_jour = historique.setdefault(start_date, {}).setdefault(joueur, [])
        
        if session_en_cours in sessions_du_jour:
            index = sessions_du_jour.index(session_en_cours)
            sessions_du_jour[index] = session_str
        else:
            sessions_du_jour.append(session_str)

        # Si le joueur s'est connecté hier et a quitté aujourd'hui
        if start_date != date_str:
            historique.setdefault(date_str, {}).setdefault(joueur, []).append(f"00:00/{time_str}")
=======
        # Session complète
        session_str = f"{start_time}/{time_str}"

        # Ajouter à la date de début
        historique.setdefault(start_date, {}).setdefault(joueur, []).append(session_str)

        # Si on a changé de jour, ajouter aussi à aujourd'hui
        if start_date != date_str:
            historique.setdefault(date_str, {}).setdefault(joueur, []).append(session_str)
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

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
<<<<<<< HEAD
            # Recherche du serveur (syntaxe moderne mcstatus)
            server = JavaServer.lookup(IP_SERVEUR)
            status = await server.status()
            
=======
            server = JavaServer.lookup("heldery.tomiix.fr")
            status = await server.async_status()
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
            sample = status.players.sample or []
            joueurs = [p.name for p in sample]
            enregistrer_joueurs(joueurs)
        except Exception as e:
<<<<<<< HEAD
            # On commente l'erreur pour ne pas spammer la console si le serveur redémarre
            pass
=======
            print(f"[Monitor] Erreur de ping : {e}")
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

    @check_server.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
<<<<<<< HEAD
    await bot.add_cog(MonitorCog(bot))
=======
    await bot.add_cog(MonitorCog(bot))
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
