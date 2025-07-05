import discord
import mcstatus
from discord.ext import commands
from discord import app_commands, Embed, Interaction  # nécessaire pour les slash commands
from mcstatus import JavaServer

class commandes_slashCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
