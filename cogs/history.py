import discord
from discord.ext import commands
from discord import app_commands
import json
import os

HISTORIQUE_PATH = "data/historique.json"

class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="history", description="Historique des connexions d'un jour")
    @app_commands.describe(jour="Date au format AAAA-MM-JJ")
    async def history(self, interaction: discord.Interaction, jour: str):
        await interaction.response.defer()
        try:
            if not os.path.exists(HISTORIQUE_PATH):
                await interaction.followup.send("Aucune donnée trouvée.")
                return

            with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            if jour not in data:
                await interaction.followup.send(f"❌ Aucun joueur trouvé pour le {jour}.")
                return

            lignes = []
            for joueur, heures in data[jour].items():
                sessions = []
                it = iter(heures)
                for debut in it:
                    try:
                        fin = next(it)
                        sessions.append(f"{debut}/{fin}")
                    except StopIteration:
                        sessions.append(f"{debut}/...")  # en attente de sortie

                lignes.append(f"**{joueur}** : {' - '.join(sessions)}")

            embed = discord.Embed(
                title=f"📅 Connexions du {jour}",
                description="\n".join(lignes),
                color=0x3498db
            )
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"Erreur : {e}")

async def setup(bot):
    await bot.add_cog(HistoryCog(bot))
