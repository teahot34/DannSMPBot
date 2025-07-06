from discord import app_commands, Embed, Interaction
from discord.ext import commands
import json
import os
from datetime import datetime
import pytz

HISTORIQUE_PATH = "data/historique.json"

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="history", description="Voir l'historique des connexions Minecraft")
    @app_commands.describe(jour="Format : AAAA-MM-JJ (facultatif)")
    async def history(self, interaction: Interaction, jour: str = None):
        await interaction.response.defer()

        tz = pytz.timezone("Europe/Paris")
        today = datetime.now(tz).strftime("%Y-%m-%d")
        date_str = jour if jour else today

        if not os.path.exists(HISTORIQUE_PATH):
            await interaction.followup.send("❌ Aucun historique trouvé.")
            return

        with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if date_str not in data:
            await interaction.followup.send(f"📅 Aucun joueur connecté le **{date_str}**.")
            return

        contenu = ""
        for joueur, sessions in data[date_str].items():
            lignes = []
            for session in sessions:
                if "/" in session and session.endswith("/"):
                    lignes.append(session.replace("/", "/(en cours)"))
                else:
                    lignes.append(session)
            contenu += f"**{joueur}** : {', '.join(lignes)}\n"

        embed = Embed(
            title=f"🕓 Historique du {date_str}",
            description=contenu or "Aucune donnée.",
            color=0x00BFFF
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(History(bot))
