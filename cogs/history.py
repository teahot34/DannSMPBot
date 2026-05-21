import discord
from discord import app_commands, Interaction
from discord.ext import commands
import json
import os
from datetime import datetime
import pytz

HISTORIQUE_PATH = "data/historique.json"
TIMEZONE = pytz.timezone("Europe/Paris")

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="history", description="Voir l'historique des connexions du serveur")
    @app_commands.describe(
        jour="Format : AAAA-MM-JJ (facultatif, par défaut aujourd'hui)",
        joueur="Nom du joueur pour filtrer (facultatif)"
    )
    async def history(self, interaction: Interaction, jour: str = None, joueur: str = None):
        if jour is None:
            jour = datetime.now(TIMEZONE).strftime("%Y-%m-%d")

        if not os.path.exists(HISTORIQUE_PATH):
            await interaction.response.send_message("❌ Aucun historique disponible pour le moment.", ephemeral=True)
            return

        with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
            try:
                historique = json.load(f)
            except json.JSONDecodeError:
                historique = {}

        # Vérifier si le jour demandé existe
        if jour not in historique or not historique[jour]:
            await interaction.response.send_message(f"❌ Aucune donnée d'historique pour le jour `{jour}`.", ephemeral=True)
            return

        donnees_du_jour = historique[jour]

        embed = discord.Embed(
            title=f"📋 Historique du {jour}",
            color=discord.Color.blue()
        )

        # CAS 1 : Si on a spécifié un joueur particulier
        if joueur is not None:
            # Recherche insensible à la casse (ex: dann ou Dann)
            joueur_trouve = None
            for k in donnees_du_jour.keys():
                if k.lower() == joueur.lower():
                    joueur_trouve = k
                    break

            if joueur_trouve is None:
                await interaction.response.send_message(f"❌ Aucune connexion trouvée pour le joueur `{joueur}` à la date du {jour}.", ephemeral=True)
                return

            sessions = donnees_du_jour[joueur_trouve]
            sessions_formatees = []
            for s in sessions:
                # Transforme "14:30/" en "14:30 ➔ (en cours)"
                if s.endswith("/"):
                    sessions_formatees.append(f"🔹 `{s.replace('/', '')}` ➔ `En cours`")
                else:
                    heures = s.split("/")
                    sessions_formatees.append(f"🔹 `{heures[0]}` ➔ `{heures[1]}`")

            # Séparateur très voyant entre chaque ligne de connexion
            texte_final = "\n".join(sessions_formatees)
            embed.add_field(name=f"👤 {joueur_trouve}", value=texte_final, inline=False)

        # CAS 2 : Pas de joueur spécifié, on montre tout le monde
        else:
            for player_name, sessions in donnees_du_jour.items():
                sessions_formatees = []
                for s in sessions:
                    if s.endswith("/"):
                        sessions_formatees.append(f"`{s.replace('/', '')}`➔`En cours`")
                    else:
                        heures = s.split("/")
                        sessions_formatees.append(f"`{heures[0]}`➔`{heures[1]}`")
                
                # Utilisation du symbole ┃ bien voyant pour séparer les sessions d'un joueur
                separateur_voyant = " ┃ "
                texte_sessions = separateur_voyant.join(sessions_formatees)
                
                embed.add_field(name=f"👤 {player_name}", value=texte_sessions, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(History(bot))