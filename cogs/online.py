from discord import app_commands, Embed, Interaction
from discord.ext import commands
from mcstatus import JavaServer

class CommandOnlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="online", description="Voir les joueurs en ligne sur le serveur Minecraft")
    async def online(self, interaction: Interaction):
        await interaction.response.defer()  # pour indiquer que le bot traite la requête

        try:
            server = JavaServer.lookup("heldery.tomiix.fr")  # Remplace par l'IP de ton serveur
            status = await server.async_status()  # Appel asynchrone

            joueurs_connectes = status.players.online
            joueurs_max = status.players.max
            joueurs_noms = [player.name for player in status.players.sample or []]

            embed = Embed(
                title="📡 Serveur Heldery",
                description=f"🟢 **{joueurs_connectes}** joueur(s) en ligne sur **{joueurs_max}**",
                color=0x57F287
            )

            if joueurs_noms:
                embed.add_field(name="👥 Joueurs connectés", value="\n".join(joueurs_noms), inline=False)
            else:
                embed.add_field(name="👥 Joueurs connectés", value="Aucun joueur visible", inline=False)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send("❌ Impossible de joindre le serveur Minecraft.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CommandOnlineCog(bot))
