import discord
from discord.ext import commands
from discord import app_commands, Embed

# ==================== CONFIGURATION DU SERVEUR ====================
NOM_SERVEUR = "DannSMP" 
IP_SERVEUR = "dannstylesmp.mine.fun"  # Nouvelle IP configurée
# ==================================================================

class commandes_slashCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ip", description=f"Donne l'adresse IP du serveur {NOM_SERVEUR}")
    async def ip(self, interaction: discord.Interaction):
        # Création de l'Embed pour un rendu professionnel
        embed = discord.Embed(
            title=f"🌐 Connexion au serveur {NOM_SERVEUR}",
            description="Voici les informations pour nous rejoindre en jeu !",
            color=discord.Color.blue()
        )
        embed.add_field(name="📌 Adresse IP", value=f"`{IP_SERVEUR}`", inline=False)
        embed.add_field(name="🎮 Version", value="1.21.1", inline=False)
        embed.set_footer(text=f"Bon jeu sur le {NOM_SERVEUR} !")
        
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog 'commandes_slash' opérationnel pour le serveur {NOM_SERVEUR} !")

async def setup(bot: commands.Bot):
    await bot.add_cog(commandes_slashCog(bot))