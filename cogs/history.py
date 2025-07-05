import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime
import pytz

HISTORIQUE_PATH = "data/historique.json"

def charger_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_heures_en_sessions(heures):
    heures = sorted(heures)
    paires = []

    # Groupement deux par deux
    for i in range(0, len(heures), 2):
        debut = heures[i]
        fin = heures[i + 1] if i + 1 < len(heures) else "?"
        paires.append(f"{debut}/{fin}")
    
    return " - ".join(paires)

class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="history", description="Historique des connexions d'un jour")
    @app_commands.describe(jour="Date au format AAAA-MM-JJ (facultatif, aujourd'hui si vide)")
    async def history(self, interaction: discord.Interaction, jour: str = None):
        await interaction.response.defer()

        # Si aucun jour n'est fourni, on prend aujourd'hui (Europe/Paris)
        if jour is None:
            now = datetime.now(pytz.timezone("Europe/Paris"))
            jour = now.strftime("%Y-%m-%d")

        try:
            data = charger_json(HISTORIQUE_PATH)

            if jour not in data:
                await interaction.followup.send(f"❌ Aucun joueur trouvé pour le {jour}.")
                return

            lignes = []
            for joueur, heures in data[jour].items():
                # Convertir les heures en HH:MM
                heures_fmt = [h[:5] for h in heures]
                sessions = format_heures_en_sessions(heures_fmt)
                lignes.append(f"**{joueur}** : {sessions}")

            embed = discord.Embed(
                title=f"📅 Connexions du {jour}",
                description="\n".join(lignes),
                color=0x3498db
            )
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ Erreur : {e}")

async def setup(bot):
    await bot.add_cog(HistoryCog(bot))
