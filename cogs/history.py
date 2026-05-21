<<<<<<< HEAD
import discord
=======
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
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
<<<<<<< HEAD
        # Sécurité : On s'assure que le dossier 'data' existe au chargement du bot
        self.assurer_dossier_existe()

    def assurer_dossier_existe(self):
        """Crée le dossier 'data' et le fichier JSON s'ils n'existent pas."""
        os.makedirs(os.path.dirname(HISTORIQUE_PATH), exist_ok=True)
        if not os.path.exists(HISTORIQUE_PATH):
            with open(HISTORIQUE_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
=======
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

    @app_commands.command(name="history", description="Voir l'historique des connexions Minecraft")
    @app_commands.describe(jour="Format : AAAA-MM-JJ (facultatif)")
    async def history(self, interaction: Interaction, jour: str = None):
        await interaction.response.defer()

<<<<<<< HEAD
        # Gestion du fuseau horaire de Paris
=======
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
        tz = pytz.timezone("Europe/Paris")
        today = datetime.now(tz).strftime("%Y-%m-%d")
        date_str = jour if jour else today

<<<<<<< HEAD
        # On revérifie si le fichier existe (au cas où il aurait été supprimé entre-temps)
=======
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
        if not os.path.exists(HISTORIQUE_PATH):
            await interaction.followup.send("❌ Aucun historique trouvé.")
            return

<<<<<<< HEAD
        # Lecture des données du fichier JSON
        with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        # Si aucune connexion n'est enregistrée pour cette date
        if date_str not in data or not data[date_str]:
=======
        with open(HISTORIQUE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if date_str not in data:
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
            await interaction.followup.send(f"📅 Aucun joueur connecté le **{date_str}**.")
            return

        contenu = ""
        for joueur, sessions in data[date_str].items():
            lignes = []
            for session in sessions:
<<<<<<< HEAD
                # Formatage sympa si la session est toujours active (en cours)
                if "/" in session and session.endswith("/"):
                    lignes.append(session.replace("/", " ➔ (en cours)"))
                else:
                    lignes.append(session)
            contenu += f"👤 **{joueur}** : {', '.join(lignes)}\n"

        # On fait attention à la limite de caractères de Discord (4096 max pour une description)
        if len(contenu) > 4000:
            contenu = contenu[:3900] + "\n\n*... Et bien d'autres (Historique trop long pour Discord) !*"
=======
                if "/" in session and session.endswith("/"):
                    lignes.append(session.replace("/", "/(en cours)"))
                else:
                    lignes.append(session)
            contenu += f"**{joueur}** : {', '.join(lignes)}\n"
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

        embed = Embed(
            title=f"🕓 Historique du {date_str}",
            description=contenu or "Aucune donnée.",
<<<<<<< HEAD
            color=0x00BFFF  # Belle couleur bleu clair
        )
        embed.set_footer(text="Format : [Connexion] ➔ [Déconnexion]")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(History(bot))
=======
            color=0x00BFFF
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(History(bot))
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
