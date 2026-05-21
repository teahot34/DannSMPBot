import discord
<<<<<<< HEAD
from discord.ext import commands
from discord import app_commands, Embed

# ==================== CONFIGURATION DU SERVEUR ====================
# Modifie ces informations pour ton nouveau serveur de jeu !
NOM_SERVEUR = "DannSMP" 
IP_SERVEUR = "dannstylesmp.mine.fun"  # Mets la nouvelle IP ici !
# ==================================================================
=======
import mcstatus
from discord.ext import commands
from discord import app_commands, Embed, Interaction  # nécessaire pour les slash commands
from mcstatus import JavaServer
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

class commandes_slashCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

<<<<<<< HEAD
    @app_commands.command(name="ip", description=f"Donne l'adresse IP du serveur {NOM_SERVEUR}")
    async def ip(self, interaction: discord.Interaction):
        # On crée un joli Embed pour que ce soit plus pro qu'un simple texte
        embed = discord.Embed(
            title=f"🌐 Connexion au serveur {NOM_SERVEUR}",
            description="Voici les informations pour nous rejoindre en jeu !",
            color=discord.Color.blue()
        )
        embed.add_field(name="📌 Adresse IP", value=f"`{IP_SERVEUR}`", inline=False)
        embed.add_field(name="🎮 Version", value="1.21.11", inline=False) # À adapter selon ton serveur
        embed.set_footer(text=f"Bon jeu sur le {NOM_SERVEUR} !")
        
        # Envoi du message (l'embed)
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog 'commandes_slash' opérationnel pour le serveur {NOM_SERVEUR} !")
        # Note : La synchronisation globale est déjà gérée dans start.py, 
        # donc plus besoin de forcer un ID de guilde ici !

async def setup(bot: commands.Bot):
    await bot.add_cog(commandes_slashCog(bot))
=======
    @app_commands.command(name="ip", description="Donne l'adresse IP du serveur Heldéry")
    async def ip(self, interaction: discord.Interaction):
        await interaction.response.send_message("L'IP de Heldery est : heldery.tomiix.fr")

    

    # Lier les commandes au bot
    @commands.Cog.listener()
    async def on_ready(self):
        # sync seulement dans ton serveur (optionnel mais recommandé pour dev)
        guild = discord.Object(id=1386283953937186857)
        self.bot.tree.copy_global_to(guild=guild)
        await self.bot.tree.sync(guild=guild)

async def setup(bot: commands.Bot):
    await bot.add_cog(commandes_slashCog(bot))
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
