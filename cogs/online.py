import discord
from discord import app_commands, Embed, Interaction
from discord.ext import commands
from mcstatus import JavaServer

# ==================== CONFIGURATION DU SERVEUR ====================
NOM_SERVEUR = "DannSMP" 
IP_SERVEUR = "dannstylesmp.mine.fun"  # Nouvelle IP configurée
# ==================================================================

class CommandOnlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="online", description=f"Voir les joueurs en ligne sur le serveur {NOM_SERVEUR}")
    async def online(self, interaction: Interaction):
        # Indique à l'utilisateur que le traitement est en cours
        await interaction.response.defer()

        try:
            server = JavaServer.lookup(IP_SERVEUR)
            
            # --- TEST 1 : Méthode standard (status) ---
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
                    # --- TEST 3 : Ping léger (Donne l'info si ON/OFF) ---
                    await server.ping()
                    joueurs_connectes = "?"
                    joueurs_max = "?"
                    joueurs_noms = []

            embed = Embed(
                title=f"📡 Statut de {NOM_SERVEUR}",
                description=f"🟢 Le serveur répond ! (Joueurs : **{joueurs_connectes}**/**{joueurs_max}**)",
                color=0x57F287
            )

            if joueurs_noms:
                embed.add_field(name="👥 Joueurs connectés", value="\n".join(joueurs_noms), inline=False)
            elif joueurs_connectes == "?":
                embed.add_field(name="⚠️ Note", value="Le serveur est en ligne mais masque sa liste de joueurs aux applications externes.", inline=False)
            else:
                embed.add_field(name="👥 Joueurs connectés", value="Aucun joueur connecté actuellement.", inline=False)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Erreur de connexion persistante : {e}")
            await interaction.followup.send(f"❌ Impossible de joindre le serveur `{NOM_SERVEUR}`. Vérifie si le serveur est bien allumé.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CommandOnlineCog(bot))