<<<<<<< HEAD
import discord
=======
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
from discord import app_commands, Embed, Interaction
from discord.ext import commands
from mcstatus import JavaServer

<<<<<<< HEAD
# ==================== CONFIGURATION DU SERVEUR ====================
NOM_SERVEUR = "DannSMP" 
IP_SERVEUR = "dannstylesmp.mine.fun"  # Mets la nouvelle IP de ton serveur de jeu ici !
# ==================================================================

=======
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
class CommandOnlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

<<<<<<< HEAD
    @app_commands.command(name="online", description=f"Voir les joueurs en ligne sur le serveur {NOM_SERVEUR}")
    async def online(self, interaction: Interaction):
        # On indique à l'utilisateur que le bot interroge le serveur Minecraft
        await interaction.response.defer()

        try:
            server = JavaServer.lookup(IP_SERVEUR)
            
            # --- TEST 1 : Méthode standard ---
            try:
                status = await server.status()
                joueurs_connectes = status.players.online
                joueurs_max = status.players.max
                joueurs_noms = [player.name for player in status.players.sample or []]
            except Exception:
                # --- TEST 2 : Méthode Query (si le port standard est bloqué) ---
                try:
                    query = await server.query()
                    joueurs_connectes = query.players.online
                    joueurs_max = query.players.max
                    joueurs_noms = query.players.names
                except Exception:
                    # --- TEST 3 : Ping ultra-léger (Donne juste l'info si ON/OFF) ---
                    ping_time = await server.ping()
                    # Si on arrive ici, le serveur est en ligne mais refuse de donner le nombre de joueurs
                    joueurs_connectes = "?"
                    joueurs_max = "?"
                    joueurs_noms = []

            embed = Embed(
                title=f"📡 Statut de {NOM_SERVEUR}",
                description=f"🟢 Le serveur répond ! (Joueurs : **{joueurs_connectes}**/**{joueurs_max}**)",
=======
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
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
                color=0x57F287
            )

            if joueurs_noms:
                embed.add_field(name="👥 Joueurs connectés", value="\n".join(joueurs_noms), inline=False)
<<<<<<< HEAD
            elif joueurs_connectes == "?":
                embed.add_field(name="⚠️ Note", value="Le serveur est en ligne mais masque sa liste de joueurs aux applications externes.", inline=False)
            else:
                embed.add_field(name="👥 Joueurs connectés", value="Aucun joueur connecté actuellement.", inline=False)
=======
            else:
                embed.add_field(name="👥 Joueurs connectés", value="Aucun joueur visible", inline=False)
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc

            await interaction.followup.send(embed=embed)

        except Exception as e:
<<<<<<< HEAD
            print(f"Erreur de connexion persistante : {e}")
            await interaction.followup.send(f"❌ Impossible de joindre le serveur `{NOM_SERVEUR}`. Les protections du serveur bloquent le bot.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CommandOnlineCog(bot))
=======
            await interaction.followup.send("❌ Impossible de joindre le serveur Minecraft.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CommandOnlineCog(bot))
>>>>>>> 46f4bcfd25f9430433d14b94d835a8a2b80f10bc
